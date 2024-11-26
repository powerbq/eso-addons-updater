#!/usr/bin/python3

import hashlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile

import requests

release_tag = 'current'
updater_url = 'https://github.com/powerbq/eso-addons-updater/releases/download/%s/' % release_tag
manager_url = 'https://github.com/powerbq/eso-addons-manager/releases/download/%s/' % release_tag

if sys.platform == 'win32':
    updater_asset = 'app.exe'
    manager_exe = 'app.exe'
    manager_asset = 'eso-addons-manager-windows-amd64.zip'
else:
    updater_asset = 'app'
    manager_exe = 'app'
    manager_asset = 'eso-addons-manager-linux-amd64.zip'


def download(url):
    response = requests.get(url, timeout=(10, 60))
    response.raise_for_status()
    return response.content


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while data := f.read(512 * 1024):
            h.update(data)
    return h.hexdigest()


def remote_sha256(url):
    return download(url + '.sha256').decode('utf-8').strip()


def update_self(updater_path):
    url = updater_url + updater_asset
    remote = remote_sha256(url)
    if sha256_file(updater_path) == remote:
        return False

    print('Updating updater...')
    body = download(url)
    if hashlib.sha256(body).hexdigest() != remote:
        print('Updater checksum mismatch, skipping.')
        return False

    bak = updater_path + '.bak'
    if os.path.exists(bak):
        os.unlink(bak)
    os.rename(updater_path, bak)
    with open(updater_path, 'wb') as f:
        f.write(body)
    if sys.platform != 'win32':
        os.chmod(updater_path, 0o755)
    return True


def prompt_restart():
    print('Updater updated. Please run it again to continue.')
    print('Press Enter to exit...')
    waiter = threading.Thread(target=input, daemon=True)
    waiter.start()
    waiter.join(30)


def update_manager(manager_dir):
    url = manager_url + manager_asset
    remote = remote_sha256(url)

    local = None
    sha_path = os.path.join(manager_dir, manager_asset + '.sha256')
    if os.path.isfile(sha_path):
        with open(sha_path) as f:
            local = f.read().strip()

    if local == remote and os.path.isdir(manager_dir):
        return

    print('Downloading manager...')
    body = download(url)
    if hashlib.sha256(body).hexdigest() != remote:
        print('Manager checksum mismatch, skipping.')
        return

    parent = os.path.dirname(manager_dir)
    os.makedirs(parent, exist_ok=True)
    staging = tempfile.mkdtemp(dir=parent)
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as z:
            for info in z.infolist():
                path = z.extract(info, staging)
                mode = info.external_attr >> 16
                if mode and sys.platform != 'win32':
                    os.chmod(path, mode)
        with open(os.path.join(staging, manager_asset + '.sha256'), 'w') as f:
            f.write(remote)

        backup = manager_dir + '.old'
        if os.path.isdir(manager_dir):
            shutil.rmtree(backup, ignore_errors=True)
            os.rename(manager_dir, backup)
        os.rename(staging, manager_dir)
        shutil.rmtree(backup, ignore_errors=True)
        staging = None
        print('Manager updated.')
    finally:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)


def launch(manager_dir, updater_dir):
    exe = os.path.join(manager_dir, manager_exe)
    if sys.platform == 'win32':
        subprocess.Popen(
            [exe],
            cwd=updater_dir,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    else:
        subprocess.Popen([exe], cwd=updater_dir, start_new_session=True)


def main():
    updater_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
    updater_dir = os.path.dirname(updater_path)
    manager_dir = os.path.join(updater_dir, 'manager')

    print('Checking for updates...')
    try:
        if update_self(updater_path):
            prompt_restart()
            return
    except Exception as e:
        print('Updater update skipped: %s' % e)

    try:
        update_manager(manager_dir)
    except Exception as e:
        print('Manager update skipped: %s' % e)

    exe = os.path.join(manager_dir, manager_exe)
    if not os.path.isfile(exe):
        print('Manager not found and could not be downloaded.')
        sys.exit(1)

    launch(manager_dir, updater_dir)


if __name__ == '__main__':
    main()

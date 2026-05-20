#!/usr/bin/python3

import json
import os
import re
import sys
import threading

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QUrl

from app import addon_exclusions
from app import api_prefix
from app import c
from app import execute
from app import favourites
from app import get_exclusions
from app import get_sync_on_launch
from app import get_target_directory
from app import get_version
from app import save
from app import set_exclusions
from app import set_sync_on_launch
from app import set_target_directory
from app import set_version
from func import download


class Backend(QObject):
    addonListReady = pyqtSignal('QVariantList')
    addonDetailsReady = pyqtSignal(str)
    installedAddonsChanged = pyqtSignal()
    updateStarted = pyqtSignal()
    updateFinished = pyqtSignal()
    logCleared = pyqtSignal()
    logMessage = pyqtSignal(str)
    appUpdateStatus = pyqtSignal(str)
    targetDirectoryChanged = pyqtSignal(str)
    exclusionsChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def checkForUpdate(self):
        def _run():
            try:
                file_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)

                old_version = get_version()

                self.appUpdateStatus.emit('Checking for updates...')
                new_version = (
                    download('https://github.com/powerbq/eso-addons-updater/releases/download/current/version.txt')
                    .decode('utf-8')
                    .strip()
                )

                if old_version != new_version and file_path != __file__:
                    self.appUpdateStatus.emit('Downloading update...')
                    update = download(
                        'https://github.com/powerbq/eso-addons-updater/releases/download/current/'
                        + os.path.basename(file_path)
                    )

                    bak = file_path + '.bak'
                    if os.path.exists(bak):
                        os.unlink(bak)

                    os.rename(file_path, bak)

                    with open(file_path, 'wb') as f:
                        f.write(update)

                    set_version(new_version)
                    save()

                    self.appUpdateStatus.emit('Update complete. Please relaunch the application.')
                else:
                    self.appUpdateStatus.emit('')
            except Exception:
                self.appUpdateStatus.emit('')

        threading.Thread(target=_run, daemon=True).start()

    @pyqtSlot()
    def fetchAddonList(self):
        def _run():
            try:
                data = json.loads(download(api_prefix + '/filelist.json'))
                simplified = [
                    {
                        'UID': obj['UID'],
                        'UIName': obj['UIName'],
                        'UIAuthorName': obj.get('UIAuthorName') or '',
                        'UIVersion': obj.get('UIVersion') or '',
                        'UIFileInfoURL': obj.get('UIFileInfoURL') or '',
                        'UIDownloadTotal': int(obj.get('UIDownloadTotal') or 0),
                        'UIDownloadMonthly': int(obj.get('UIDownloadMonthly') or 0),
                        'UIFavoriteTotal': int(obj.get('UIFavoriteTotal') or 0),
                        'UIDate': int(obj.get('UIDate') or 0),
                    }
                    for obj in data
                ]
                self.addonListReady.emit(simplified)
            except Exception as e:
                self.logMessage.emit('Error fetching addon list: %s' % e)

        threading.Thread(target=_run, daemon=True).start()

    @pyqtSlot(str)
    def fetchAddonDetails(self, uid):
        def _run():
            try:
                import bbcode

                data = json.loads(download(api_prefix + '/filedetails/' + uid + '.json'))
                obj = data[0]

                parser = bbcode.Parser(escape_html=False, drop_unrecognized=True)

                def _bb(text):
                    text = re.sub(r'\[(\w+)="([^"]+)"\]', r'[\1=\2]', text)
                    return parser.format(text)

                parts = []
                desc = (obj.get('UIDescription') or '').strip()
                if desc:
                    parts.append('<h3>Description</h3>' + _bb(desc))
                log = (obj.get('UIChangeLog') or '').strip()
                if log:
                    parts.append('<h3>Changelog</h3>' + _bb(log))

                self.addonDetailsReady.emit('<br>'.join(parts))
            except Exception as e:
                self.addonDetailsReady.emit('Failed to load details: %s' % e)

        threading.Thread(target=_run, daemon=True).start()

    @pyqtSlot(result=str)
    def getTargetDirectory(self):
        return get_target_directory()

    @pyqtSlot(str)
    def setTargetDirectory(self, path):
        if path.startswith('file://'):
            path = QUrl(path).toLocalFile()
        set_target_directory(path)
        save()
        self.targetDirectoryChanged.emit(path)

    @pyqtSlot()
    def browseTargetDirectory(self):
        from PyQt6.QtWidgets import QFileDialog

        path = QFileDialog.getExistingDirectory(
            None,
            'Select AddOns folder',
            get_target_directory(),
        )
        if path:
            set_target_directory(path)
            save()
            self.targetDirectoryChanged.emit(path)

    @pyqtSlot(result=bool)
    def hasTtcClient(self):
        path = os.path.join(get_target_directory(), 'TamrielTradeCentre', 'Client', 'Client.exe')
        return os.path.isfile(path)

    @pyqtSlot()
    def launchTtcClient(self):
        path = os.path.join(get_target_directory(), 'TamrielTradeCentre', 'Client', 'Client.exe')
        if sys.platform == 'win32':
            os.startfile(path)
        else:
            import subprocess

            subprocess.Popen([path], start_new_session=True)

    @pyqtSlot(result=str)
    def getExclusionsText(self):
        return '\n'.join(get_exclusions())

    @pyqtSlot(str)
    def setExclusionsText(self, text):
        patterns = [line for line in text.splitlines() if line.strip()]
        set_exclusions(patterns)
        save()

    @pyqtSlot(result=str)
    def getAddonExclusionsText(self):
        result = []
        for uid, patterns in addon_exclusions.items():
            if uid in c['AddOns']:
                result.extend(patterns)
        return '\n'.join(result)

    @pyqtSlot(result=bool)
    def getSyncOnLaunch(self):
        return get_sync_on_launch()

    @pyqtSlot(bool)
    def setSyncOnLaunch(self, value):
        set_sync_on_launch(value)
        save()

    @pyqtSlot()
    def runUpdate(self):
        self.logCleared.emit()
        self.updateStarted.emit()

        def _run():
            try:
                execute(log_callback=self.logMessage.emit)
            except Exception as e:
                self.logMessage.emit('Update failed: %s' % e)
            finally:
                self.installedAddonsChanged.emit()
                self.updateFinished.emit()

        threading.Thread(target=_run, daemon=True).start()

    @pyqtSlot(str, str)
    def toggleFavourite(self, uid, name):
        if uid in favourites:
            c.remove_option('Favourites', uid)
        else:
            favourites[uid] = name
        save()

    @pyqtSlot(result='QVariantList')
    def getFavourites(self):
        return list(favourites.keys())

    @pyqtSlot(str, str)
    def installAddon(self, uid, name):
        c['AddOns'][uid] = name
        save()
        self.runUpdate()

    @pyqtSlot(str)
    def removeAddon(self, uid):
        c.remove_option('AddOns', uid)
        save()
        self.runUpdate()

    @pyqtSlot(result='QVariantList')
    def getInstalledAddons(self):
        result = []
        for uid, name in c['AddOns'].items():
            result.append({'uid': uid, 'name': name if name else uid})
        return result

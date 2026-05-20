#!/usr/bin/python3

import configparser
import json
import os
import re
import shutil
import zipfile

from func import download
from func import md5
from rsync import Logger as RsyncLogger
from rsync import sync


class AddOn:
    def __init__(self):
        self.name = None
        self.version = None


class SortedDict(dict):
    def items(self):
        return sorted(super().items(), key=key)


class Logger:
    write = print


def get_target_directory():
    return c['General']['TargetDirectory']


def set_target_directory(path):
    c['General']['TargetDirectory'] = path


def get_version():
    return c.get('General', 'Version', fallback='')


def set_version(value):
    c['General']['Version'] = value


def get_sync_on_launch():
    return c.getboolean('General', 'SyncOnLaunch', fallback=False)


def set_sync_on_launch(value):
    c['General']['SyncOnLaunch'] = 'true' if value else 'false'


def get_exclusions():
    return list(c['Exclusions'].values())


def set_exclusions(patterns):
    for opt in list(c['Exclusions']):
        c.remove_option('Exclusions', opt)
    for i, pattern in enumerate(patterns):
        c['Exclusions'][str(i)] = pattern


def key(item):
    return item[1] if item[0].isnumeric() and type(item[1]) is str else item[0]


def log(status, kind, uid, message):
    Logger.write('\t%s\t%s\t%s\t%s' % (status, kind, uid, message))


def dependencies(path):
    z = zipfile.ZipFile(path)

    for name in z.namelist():
        info = z.getinfo(name)

        if info.is_dir() or (not name.lower().endswith('.txt') and not name.lower().endswith('.addon')):
            continue

        with z.open(name) as f:
            lines = f.readlines()

        for line in lines:
            text = line.decode('utf-8-sig', errors='ignore')

            if text.startswith('## Title:'):
                satisfied.add('.'.join(os.path.basename(name).split('.')[:-1]))

            if text.startswith('## DependsOn:') or text.startswith('## PCDependsOn:'):
                for directory in re.sub(r'[=<>][^ ]+', '', text).strip().split()[2:]:
                    if directory in candidates:
                        if directory not in satisfied:
                            satisfied.add(directory)

                            if len(candidates[directory]) < 2:
                                process(candidates[directory][0])

                            else:
                                if (
                                    directory not in c['SelectedLibraries']
                                    or c['SelectedLibraries'][directory] not in candidates
                                ):
                                    c['SelectedLibraries'][directory] = candidates[directory][0]

                                process(c['SelectedLibraries'][directory])

                        continue

                    if directory in satisfied:
                        continue

                    unsatisfied.add(directory)


def process(uid):
    name = database[uid].name
    version = database[uid].version

    identifier = re.sub(r'\W', '', name) + '_' + uid
    path = 'addons/' + identifier + '.zip'

    invalid = (
        not os.path.exists(path)
        or not c.has_section(uid)
        or c[uid].get('UIVersion') != version
        or c[uid].get('UIMD5') != md5(path)
    )
    if invalid:
        obj_list = json.loads(download(api_prefix + '/filedetails/' + uid + '.json'))
        obj = obj_list[0]

        if not c.has_section(uid):
            c.add_section(uid)

        c[uid]['UIVersion'] = obj['UIVersion']
        c[uid]['UIMD5'] = obj['UIMD5']

        body = download(obj['UIDownload'])
        with open(path, 'wb') as f:
            f.write(body)

    status = 'upd' if invalid else '-'
    kind = 'lib' if uid not in addons else '-'
    log(status, kind, uid, name)

    sources.add(path)

    dependencies(path)


def run():
    obj_list = json.loads(download(api_prefix + '/filelist.json'))
    for obj in obj_list:
        uid = obj['UID']
        name = obj['UIName']
        version = obj['UIVersion']

        database[uid] = AddOn()
        database[uid].name = name
        database[uid].version = version

        for directory in obj['UIDir']:
            if directory not in candidates:
                candidates[directory] = []

            candidates[directory].append(uid)

    for uid in addons.keys():
        if uid in database:
            if not c.has_section(uid):
                c.add_section(uid)

            addons[uid] = database[uid].name

            process(uid)

        else:
            name = addons[uid]
            if name:
                log('err', '-', uid, '%s (Not found in database)' % name)

            else:
                log('err', '-', uid, 'Not found in database')

    for path in sorted(os.listdir('custom')):
        if path.endswith('.zip'):
            path = 'custom/' + path
            if os.path.isfile(path):
                name = path.removeprefix('custom/').removesuffix('.zip')
                log('-', '-', '-', 'Custom (%s)' % name)

                sources.add(path)

                dependencies(path)

    errors = unsatisfied - satisfied
    for directory in errors:
        log('err', 'lib', '-', 'No candidates found for %s' % directory)

    effective_exclusions = list(get_exclusions())
    for uid, patterns in addon_exclusions.items():
        if uid in addons:
            effective_exclusions.extend(patterns)

    sync(sources, get_target_directory(), exclude_patterns=effective_exclusions)


def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def cleanup():
    for path in os.listdir('addons'):
        if 'addons/' + path not in sources:
            delete('addons/' + path)

    for path in os.listdir('custom'):
        if not path.endswith('.zip'):
            delete('custom/' + path)

    for section in c.sections():
        if section == 'General':
            for option in list(c[section].keys()):
                if option not in {'TargetDirectory', 'Version', 'SyncOnLaunch'}:
                    c.remove_option(section, option)

        elif section == 'Exclusions':
            pass  # user-defined, keep as-is

        elif section == 'AddOns':
            for option in list(c[section].keys()):
                if not option.isnumeric() or option not in database:
                    c.remove_option(section, option)

        elif section == 'Favourites':
            for option in list(c[section].keys()):
                if not option.isnumeric() or option not in database:
                    c.remove_option(section, option)

        elif section == 'SelectedLibraries':
            for option in list(c[section].keys()):
                value = c[section][option]
                if value not in database or len(candidates[option]) < 2:
                    c.remove_option(section, option)

        else:
            if not any(s.endswith('_' + section + '.zip') for s in sources):
                c.remove_section(section)

            else:
                for option in list(c[section].keys()):
                    if option not in {'UIVersion', 'UIMD5'}:
                        c.remove_option(section, option)


def save():
    with open('app.ini', 'w') as f:
        c.write(f)


def execute(log_callback=None):
    Logger.write = log_callback or print
    RsyncLogger.write = Logger.write

    os.makedirs(get_target_directory(), exist_ok=True)

    os.makedirs('addons', exist_ok=True)
    os.makedirs('custom', exist_ok=True)

    database.clear()
    candidates.clear()

    satisfied.clear()
    unsatisfied.clear()
    sources.clear()

    run()
    cleanup()
    save()

    Logger.write = print
    RsyncLogger.write = print


api_prefix = 'https://api.mmoui.com/v3/game/ESO'

harvest_map_exclusions = [
    r'^HarvestMapData/$',
    r'^HarvestMapData/Modules/$',
]

for loc in ['AD', 'DC', 'EP', 'NF', 'DLC']:
    harvest_map_exclusions.append(r'^HarvestMapData/Modules/HarvestMap%s/$' % loc)
    harvest_map_exclusions.append(r'^HarvestMapData/Modules/HarvestMap%s/HarvestMap%s\.lua$' % (loc, loc))

ttc_exclusions = [
    r'^TamrielTradeCentre/$',
    r'^TamrielTradeCentre/Client/$',
    r'^TamrielTradeCentre/Client/TTC_Lock$',
    r'^TamrielTradeCentre/PriceTableEU\.lua$',
    r'^TamrielTradeCentre/PriceTableNA\.lua$',
]

for lang in ['DE', 'EN', 'ES', 'FR', 'JP', 'RU', 'ZH']:
    ttc_exclusions.append(r'^TamrielTradeCentre/ItemLookUpTable_%s\.lua$' % lang)

addon_exclusions = {
    '1245': ttc_exclusions,
    '3034': harvest_map_exclusions,
}

c = configparser.ConfigParser(dict_type=SortedDict)
c.optionxform = str
c.add_section('General')
c.add_section('AddOns')
c.add_section('Favourites')
c.add_section('SelectedLibraries')
set_target_directory('target/AddOns')
set_version('')
set_sync_on_launch(False)

if os.path.exists('app.ini'):
    c.read('app.ini')

if not c.has_section('Exclusions'):
    c.add_section('Exclusions')
    save()

addons = c['AddOns']
favourites = c['Favourites']

database = {}
candidates = {}

satisfied = set()
unsatisfied = set()
sources = set()

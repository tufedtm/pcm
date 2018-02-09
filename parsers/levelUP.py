import configparser
import json
import os
import shutil


def parse(number, folder, res):
    def get_all():
        files1, directories = [], []

        for walk_root, folders, walk_files in os.walk(folder):
            for name in walk_files:
                if walk_root in (folder, f'{folder}\engine', f'{folder}\commercial', f'{folder}\!_Playlists'):
                    continue
                files1.append(f'{walk_root}/{name}'.replace('\\', '/').lower())
            for name in folders:
                if walk_root == folder:
                    continue
                directories.append(f'{walk_root}/{name}'.replace('\\', '/').lower())

        return files1, directories

    all_files, all_dirs = get_all()

    general_config = configparser.ConfigParser()
    general_config.read(f'{folder}/engine/general.ini')

    result = {}
    for section in general_config.sections():
        result[section] = {}
        result[section]['PCM_node'] = []

        for item in list(general_config[section].items()):
            result[section][item[0]] = item[1]

        path = f'{folder}/{general_config[section]["dir"]}'
        config = configparser.ConfigParser()
        config.read(f'{path}/config.ini')
        if path.lower() in all_dirs:
            all_dirs.remove(path.lower())
        if f'{path}/config.ini'.lower() in all_files:
            all_files.remove(f'{path}/config.ini'.lower())

        if sorted(list(config['folders'].values())) != sorted(config.sections()[1:]):
            print(
                len(list(config['folders'].values())),
                general_config[section]['dir'],
                sorted(list(config['folders'].values()))
            )
            print(
                len(config.sections()[1:]),
                general_config[section]['dir'],
                sorted(config.sections()[1:])
            )

        for section1 in config.sections()[1:]:
            result1 = {}
            if section1 not in list(config['folders'].values()):
                print(section, section1)
                result1['PCM_info'] = ['на диске было только описание, и оно игнорировась']
            for item1 in list(config[section1].items()):
                result1['PCM_images'] = []
                result1[item1[0]] = item1[1]

            section_folder = f'{general_config[section]["dir"]}/{section1}'
            if f'{folder}/{section_folder}'.lower() in all_dirs:
                all_dirs.remove(f'{folder}/{section_folder}'.lower())
            for root, dirs, files in os.walk(f'{path}/{section1}'):
                for file in files:
                    if os.path.splitext(file)[1].lower() in ('.jpg', '.png'):
                        shutil.copy(
                            f'{folder}/{section_folder}/{file}',
                            f'images/{number}.{general_config[section]["dir"]}.{section1}.{file}'
                        )
                        result1['PCM_images'].append(f'{number}.{general_config[section]["dir"]}.{section1}.{file}')

                        if f'{root}/{file}'.lower() in all_files:
                            all_files.remove(f'{root}/{file}'.lower())
                        else:
                            print(f'{root}/{file}')

            result1['file'] = f'{section_folder}/{config[section1]["file"]}'

            if f'{folder}/{result1["file"]}'.lower() in all_files:
                all_files.remove(f'{folder}/{result1["file"]}'.lower())
            else:
                print('404', f'{folder}/{result1["file"]}')

            result[section]['PCM_node'].append(result1)
    print(number)
    print(all_files)
    print(all_dirs)
    print()
    print()

    res[number] = result


if __name__ == '__main':
    lu = {}
    for directory in os.listdir('d:/magazines/level up/lu 2010'):
        parse(directory, f'd:/magazines/level up/lu 2010/{directory}', lu)

    # directory = 'lu 2011.10.06'
    # parse(directory, f'd:/magazines/level up/lu 2010/{directory}', res)

    with open(f'levelUP.json', 'w', encoding='utf8') as json_file:
        json_file.write(json.dumps(lu, ensure_ascii=False, indent=2, sort_keys=True))

'на диске было только описание'
'на диске было только описание, и оно игнорировась'

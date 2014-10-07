__author__ = 'D503'

import re
import pprint
from os.path import curdir, join, exists, isfile, splitext, split, sep
from os import walk, mkdir, remove
from pickle import dump, load
from sys import platform


def main():
    pass


def check_create_directory(path):
    if exists(path) and isfile(path):
        remove(path)
    if not exists(path):
        mkdir(path)


def read_mod_material(mapname):
    """
    Читаем названия файлов из исходника карты
    :param mapname: исходный файл карты
    :return: множество (set) имён файлов
    """
    try:
        data = open(mapname)
    except IOError:
        print('Happens')
        raise
    else:
        re_material = re.compile(r'".*?"')
        map_material = set()
        for material in data:
            groups = re_material.findall(material)
            # location of file is defined on second field
            filename = groups[1]
            typefile = groups[0]
            map_material.add((filename[1:-1], typefile[1:-1]))
        pprint.pprint(map_material, open("map_material.txt", "w"))
        return map_material


def find_all_material(dir=curdir):
    """
    Легковестно 'индексируем' доступные матераиалы (текстуры, модели, и т.д.)
    :param dir: расположение всех материалов
    :return:
    """
    if exists("all_material.pickle") and isfile("all_material.pickle"):
        all_mat = open("all_material.pickle", "rb")
        all_files = load(all_mat)
    else:
        all_files = dict()
        num_dir = 0

        for obs_dir, sub_dirs, sub_files in walk(dir):
            for filename in sub_files:
                # if platform[:3] == "win":
                # obs_dir.replace("\\", "/")
                complete_filename = join(obs_dir, filename)
                filename = splitext(filename)[0].lower()
                if filename in all_files:
                    all_files[filename].append((obs_dir, complete_filename))
                else:
                    all_files[filename] = [(obs_dir, complete_filename)]
            num_dir += 1
            print(num_dir)
        output = open("all_material.pickle", "wb")
        dump(all_files, output)

        pprint.pprint(all_files, open("all_material.txt", "w"))
    return all_files


def create_mod_material(mod_material, accessible_material, new_path):
    for material in mod_material:
        """
        material_name = material[0].lower()
        type_material = material[1].lower()
        material_list = list()
        if type_material == "material":
            material_list.append(material_name + ".vmt")
            material_list.append(material_name + ".vtf")
        elif type_material == "model":
            material_ext = splitext(material_name)
            if material_ext[1] == ".mdl":
                material_list.append(material_ext[0] + ".mdl")
                material_list.append(material_ext[0] + ".dx80.vtx")
                material_list.append(material_ext[0] + ".dx90.vtx")
                material_list.append(material_ext[0] + ".phy")
                material_list.append(material_ext[0] + ".sw.vtx")
                material_list.append(material_ext[0] + ".vvd")
        else:
            material_list.append(material_name)
        """

        only_name = splitext((material[0]).split('/')[-1].lower())[0]
        if only_name in accessible_material:  # and \
            #len(accessible_material[only_name]) == 1:

            for material_id in accessible_material[only_name]:
                material_old_location = material_id[1]

                #if platform[:3] == "win":
                #    re.sub(material_old_location, "/", "\\")
                splitted_location = material_old_location.split(sep)

                path = new_path
                for sub_path in splitted_location[:-1]:
                    if sub_path != ".":
                        path = join(path, sub_path)
                        check_create_directory(path)

                old_file = open(material_old_location, "rb")
                new_file = open(join(path, splitted_location[-1]), "wb")

                for bytes_str in old_file:
                    new_file.write(bytes_str)
        elif not only_name in accessible_material:
            print("File not found: {}".format(only_name))
        else:
            print("Heh: {}".format(only_name))


if __name__ == '__main__':
    mod_material = read_mod_material("input")
    all_material = find_all_material()
    create_mod_material(mod_material, all_material, ".\\cube")
import os
from os import walk

# Specify the directory path
directory_path = r"C:\\Users\\Xiiao\\Documents\\Github\\tomimi-chan\\src\\lib\\images\\skill_icons"

# Get the absolute path of the directory
abs_path = os.path.abspath(directory_path)

list = []

for (root, dirs, files) in walk(directory_path):
    list.extend(files)
    break

with open("temp.txt", "w") as file:   
    # for icon in list: #!MODULE
    #     icon_name = icon.split(".")[0].replace("-","_")
    #     file.write(f"import {icon_name} from '$lib/images/equip_icons/{icon}';\n")
    # file.write("export const uniequips = {\n")
    # for icon in list:
    #     icon_name = icon.split(".")[0]
    #     replaced_name = icon_name.replace("-","_")
    #     file.write(f"'{icon_name}': {replaced_name},\n")
    # file.write("}")

    for icon in list: #!SKILL
        if not '#' in icon:
            icon_name = icon.split(".")[0].replace("[","").replace("]","")
            file.write(f"import {icon_name} from '$lib/images/skill_icons/{icon}';\n")
    file.write("export const uniequips = {\n")
    for icon in list:
        if not '#' in icon:
            icon_name = icon.split(".")[0]
            replaced_name = icon_name.replace("[","").replace("]","")
            file.write(f"'{icon_name}': {replaced_name},\n")
    file.write("}")



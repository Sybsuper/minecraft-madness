# Minecraft Madness, by Sybsuper

# You can only run this program if you have python 3 installed
# run the program by opening the command prompt and browse to the directory this file is placed in, then type: "python randomize.py <seed> <world>"
# make sure the <seed> and <world> options are optional, but when you use them make sure the world exists, or the zip file will be created in the directory this file is in.

# Have fun playing!

import os
import random
import io
import zipfile
import json
import sys

# Thanks to SethBling's loot table randomizer
# Recipe randomizer by Sybsuper

if len(sys.argv) >= 2:
	seed = sys.argv[1]
	random.seed(seed)
	datapack_name = 'minecraft_madness'
	datapack_desc = 'Minecraft madness, by Sybsuper, randomize all loot tables and recipes, Seed: {}'.format(seed)
else:
	print('If you want to use a specific randomizer seed integer, use: "python randomize.py <seed> <world>"')
	datapack_name = 'minecraft_madness'
	datapack_desc = 'Minecraft madness, by Sybsuper, randomize all loot tables and recipes'

folder = os.getcwd()
if len(sys.argv) >= 3:
	world_name = sys.argv[2]
	if os.path.exists(os.getenv("APPDATA")+"\\.minecraft\\saves\\{}\\datapacks".format(world_name)):
		folder = os.getenv("APPDATA")+"\\.minecraft\\saves\\{}\\datapacks".format(world_name)
		print("Folder set to: '{}'".format(os.getenv("APPDATA")+"\\.minecraft\\saves\\{}".format(world_name)))
	else:
		print("World with name '{}' not found ".format(world_name) + "at '{}'".format(os.getenv("APPDATA") + "\\.minecraft\\saves\\{}\\datapacks".format(world_name)))
datapack_filename = datapack_name + '.zip'

print('Generating datapack...')
	
file_list = []
remaining = []

for dirpath, dirnames, filenames in os.walk('loot_tables'):
	for filename in filenames:
		file_list.append(os.path.join(dirpath, filename))
		remaining.append(os.path.join(dirpath, filename))
		
file_dict = {}

for file in file_list:
	i = random.randint(0, len(remaining)-1)
	file_dict[file] = remaining[i]
	del remaining[i]
	
zipbytes = io.BytesIO()
zip = zipfile.ZipFile(zipbytes, 'w', zipfile.ZIP_DEFLATED, False)

for from_file in file_dict:
	with open(from_file) as file:
		contents = file.read()
		
	zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

file_list = []
results = []

for dirpath, dirnames, filenames in os.walk('recipes'):
	for filename in filenames:
		file_list.append(os.path.join(dirpath, filename))
		with open(os.path.join(dirpath, filename)) as file:
			res = json.loads(file.read())
			if "result" in res:
				results.append(res["result"])


file_dict = {}
for file in file_list:
	if len(results) > 0:
		i = random.randint(0, len(results)-1)
		file_dict[file] = results[i]
		del results[i]

for from_file in file_dict:
	with open(from_file) as file:
		contents = json.loads(file.read())
	contents["result"] = file_dict[from_file]
	if contents["type"] == "minecraft:smelting" or contents["type"] == "minecraft:blasting" or contents["type"] == "minecraft:campfire_cooking" or contents["type"] == "minecraft:smoking" or contents["type"] == "minecraft:stonecutting":
		if  str(type(file_dict[from_file]))=="<class 'dict'>":
			if contents["type"] == "minecraft:stonecutting" and "count" in contents["result"]:
				contents["count"] = contents["result"]["count"]
			contents["result"] = contents["result"]["item"]
	elif contents["type"]=="minecraft:crafting_shapeless" or contents["type"]=="minecraft:crafting_shaped":
		if str(type(file_dict[from_file])) == "<class 'str'>":
			contents["result"] = {"item": file_dict[from_file], "count": 1}
	zip.writestr(os.path.join('data/minecraft/', from_file), json.dumps(contents))

zip.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':datapack_desc}}, indent=4))
zip.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))
zip.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Minecraft madness by Sybsuper","color":"gold"}]')
	
zip.close()
with open(folder  + "\\" + datapack_filename, 'wb') as file:
	file.write(zipbytes.getvalue())
	
print('Created datapack "{}"'.format(datapack_filename))
import sys
import os, shutil
import tools

def restore():
	tools.empty_folder('restored_file')

	chapters = 0
	
	meta_data = open('raw_data/meta_data.txt','r')
	meta_info = []
	for row in meta_data:
		temp = row.split('\n')
		temp = temp[0]
		temp = temp.split('=')
		meta_info.append(temp[1])
	address = 'restored_file/' + meta_info[0]
	
	list_of_files = sorted(tools.list_dir('files'))

	with open(address,'wb') as writer:
		for file in list_of_files:
			path = 'files/' + file
			with open(path,'rb') as reader:
				for line in reader:
					writer.write(line)
				reader.close()
		writer.close()

	tools.empty_folder('files')
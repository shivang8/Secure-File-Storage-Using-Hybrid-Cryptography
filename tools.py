import os
import shutil

def empty_folder(directory_name):
	if not os.path.isdir(directory_name):
		os.makedirs(directory_name)
	else:
		folder = directory_name
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path): shutil.rmtree(file_path)
			except Exception as e:
				print(e)

def list_dir(path):
	return os.listdir(path)


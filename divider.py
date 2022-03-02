import sys
import tools

def divide():
	tools.empty_folder('files')
	tools.empty_folder('raw_data')
	FILE = tools.list_dir('uploads')
	FILE = './uploads/'+FILE[0]

	MAX  = 1024*32						# 1	MB	-	max chapter size
	BUF  = 50*1024*1024*1024  			# 50GB	-	memory buffer size

	chapters = 0
	uglybuf  = ''
	meta_data = open('raw_data/meta_data.txt','w')
	file__name = FILE.split('/')
	file__name = file__name[-1]
	print (file__name)
	meta_data.write("File_Name=%s\n" % (file__name))
	with open(FILE, 'rb') as src:
		while True:
			target_file = open('files/SECRET' + '%07d' % chapters, 'wb')
			written = 0
			while written < MAX:
				if len(uglybuf) > 0:
					target_file.write(uglybuf)
				target_file.write(src.read(min(BUF, MAX - written)))
				written += min(BUF, MAX - written)
				uglybuf = src.read(1)
				if len(uglybuf) == 0:
					break
			target_file.close()
			if len(uglybuf) == 0:
				break
			chapters += 1
	meta_data.write("chapters=%d" % (chapters+1))
	meta_data.close()
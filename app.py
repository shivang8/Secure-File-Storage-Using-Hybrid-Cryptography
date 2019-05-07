import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import tools
import divider as dv
import encrypter as enc
import decrypter as dec
import restore as rst

UPLOAD_FOLDER = './uploads/'
UPLOAD_KEY = './key/'
ALLOWED_EXTENSIONS = set(['pem'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_KEY'] = UPLOAD_KEY

#port = int(os.getenv('PORT', 8000))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_encryption():
	dv.divide()
	tools.empty_folder('uploads')
	enc.encrypter()
	return render_template('success.html')

def start_decryption():
	dec.decrypter()
	tools.empty_folder('key')
	rst.restore()
	return render_template('restore_success.html')

@app.route('/return-key/My_Key.pem')
def return_key():
	list_directory = tools.list_dir('key')
	filename = './key/' + list_directory[0]
	return send_file(filename, attachment_filename='My_Key.pem')

@app.route('/return-file/')
def return_file():
	list_directory = tools.list_dir('restored_file')
	filename = './restored_file/' + list_directory[0]
	print "****************************************"
	print list_directory[0]
	print "****************************************"
	return send_file(filename, attachment_filename=list_directory[0], as_attachment=True)

@app.route('/download/')
def downloads():
	return render_template('download.html')

@app.route('/upload')
def call_page_upload():
	return render_template('upload.html')

@app.route('/home')
def back_home():
	tools.empty_folder('key')
	tools.empty_folder('restored_file')
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def upload_file():
	tools.empty_folder('uploads')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			return start_encryption()
		return 'Invalid File Format !'
	
@app.route('/download_data', methods=['GET', 'POST'])
def upload_key():
	tools.empty_folder('key')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_KEY'], file.filename))
			return start_decryption()
		return 'Invalid File Format !'

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)
	#app.run()
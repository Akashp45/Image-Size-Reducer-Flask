import atexit
import os
from flask import Flask, redirect, url_for, request,render_template,send_file
import image_score
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

image_q=list()

@app.route('/',defaults={'filename': None})
@app.route('/upload/<filename>')
def uploadImage(filename):
	if(filename==None):
		return render_template("upload.html")
	if(filename in image_q):
		image_q.remove(filename)
	if(os.path.exists("uploads/"+filename)):
		return send_file("uploads/"+filename, mimetype='image/gif',as_attachment=True)
	return "File may get removed from server or incorrect file name"

@app.route('/loading',methods = ['GET', 'POST'])
def laoding():
	if(request.method=='GET'):
		return render_template('upload.html')
	try:
		if(not os.path.exists(os.getcwd()+"/uploads")):
			os.mkdir('uploads')
		f=request.files['image']
		f.save("uploads/"+f.filename)
		image_q.append(f.filename)
		return render_template("loading.html",filename=f.filename)
	except Exception:
		return str(Exception)

@app.route('/reducesize/<filename>',methods=['GET','POST'])
def reduceSize(filename):
	if(request.method=='POST'):
		return "Error"
	returnfile=image_score.reduce_size(filename)
	return render_template("upload.html",filename=returnfile)

def cleaner(image_q):
	print("Cleaning upload directory...")
	for image in os.listdir('uploads/'):
		if(not image in image_q):
			os.remove('uploads/'+image)

scheduler = BackgroundScheduler()
scheduler.add_job(func=lambda:cleaner(image_q), trigger="interval", minutes=10)
scheduler.start()

# main driver function
# if __name__ == '__main__':
# 	if(not os.path.exists(os.getcwd()+"/uploads")):
# 		os.mkdir('uploads')
# 	app.run(debug=True)
# 	atexit.register(lambda:scheduler.shutdown())

# main driver function
if __name__ == '__main__':
    if not os.path.exists(os.getcwd() + "/uploads"):
        os.mkdir('uploads')
    app.run(host='0.0.0.0', port=5000, debug=True)
    atexit.register(lambda: scheduler.shutdown())


from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import cv2

# UPLOAD_FOLDER ='static'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.secret_key = "amit verma"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def processImage(filename, operation):
    print(f"file name is {filename} and operation is {operation}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgrays":
             imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             newFile = f"static/{filename}"
             cv2.imwrite(newFile, imgProcessed)
             return newFile

        case "cpng":
            newFile = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFile, img)
            return newFile

        case "cjpg":
            newFile = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFile, img)
            return newFile

        case "cwebp":
            newFile = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFile, img)
            return newFile





    pass

@app.route("/")
def home():
    # return "<p>amit verma</p>"
    return render_template("index.html")


@app.route("/about")
def about():
    # return "<p>amit verma</p>"
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


@app.route("/edit", methods=["GET", "POST"])
def edit_image():
    if request.method == "POST":
        operation = request.form.get('operation')
        # return "Post request is here"
        # check if request has the file part
        if 'file' not in request.files:

            return render_template("fileNotSelect.html")
        file = request.files['file']

        # if the user doesn't select a file, the browser submits an empty file without a file name
        if file.filename == '':

            return render_template("fileNotFound.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            latestFile = processImage(filename, operation)
           # flash(f"Your image is being processed and available  <a href = '/static/{filename}' target='_blank' >here.</a> ")
            flash(f"Your image is being processed and available  <a href = '/{latestFile}' target='_blank' >here.</a> ")
            return render_template('index.html')

    return render_template('index.html')


app.run(debug=True, port=5001)

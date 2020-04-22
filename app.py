import os
from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from get_prediction import *

basedir = os.path.abspath(os.path.dirname(__file__))

static_foder = os.path.join('static', 'img')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads
app.config['UPLOAD_FOLDER'] = static_foder

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')

@app.route('/')
def home():
    model_image=os.path.join(app.config['UPLOAD_FOLDER'], 'autoende.png')
    return render_template('index.html',model_image=model_image)

@app.route('/index')
def index():
    model_image=os.path.join(app.config['UPLOAD_FOLDER'], 'autoende.png')
    return render_template('index.html',model_image=model_image)

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    img_files = {
        "img1":  os.path.join(app.config['UPLOAD_FOLDER'], 'a.png'),
        "img2":  os.path.join(app.config['UPLOAD_FOLDER'], 'b.png'),
        "img3":  os.path.join(app.config['UPLOAD_FOLDER'], 'c.png'),
        "img4":  os.path.join(app.config['UPLOAD_FOLDER'], 'd.png'),
        "img5":  os.path.join(app.config['UPLOAD_FOLDER'], 'e.png'),
    }
    

    #pred_image=None
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        
        print("this is file Name",filename)
        predict_result = get_img_predict("uploads/"+filename)
        pred_image = file_url
    else:
        predict_result = None
        pred_image=None
    return render_template('prediction.html', form=form,img_files=img_files,pred_image=pred_image, predict_result=predict_result)

@app.route('/team')
def team():
    img_files = {
        "fuhad":  os.path.join(app.config['UPLOAD_FOLDER'], 'ff.jpg'),
        #"shipar":  os.path.join(app.config['UPLOAD_FOLDER'], 'shipar.jpg'),
        #"shithi":  os.path.join(app.config['UPLOAD_FOLDER'], 'shithi.jpg'),
        #"ragib":  os.path.join(app.config['UPLOAD_FOLDER'], 'ragib.jpg'),
    }
    return render_template('team.html',img_files=img_files)

@app.route('/samples')
def samples():
    img_files = {
        "img1":  os.path.join(app.config['UPLOAD_FOLDER'], 'img_1.png'),
        "img2":  os.path.join(app.config['UPLOAD_FOLDER'], 'image_6.png'),
        "img3":  os.path.join(app.config['UPLOAD_FOLDER'], 'img_4.png'),
        "img4":  os.path.join(app.config['UPLOAD_FOLDER'], 'image_7.png')
    }
    return render_template('samples.html',img_files=img_files)


if __name__ == '__main__':
    app.run()

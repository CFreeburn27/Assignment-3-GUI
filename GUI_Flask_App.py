from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_navigation import Navigation
import os
from booksDatabase import db, BooksPredictions, BooksInformation
from genre_model import GenreModel
from googleAPI import get_book_details_from_google

model = GenreModel()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = './static/'

# example info for homepage
exampleBookGenrePredictions = {}
exampleBookGenrePredictions['Confidence'] = '0.6679179'
exampleBookGenrePredictions['FileName'] = 'why_nations_fail.jpg'
exampleBookGenrePredictions['Genre'] = 'Business & Money'

exampleBookInfoPredictions = {}
exampleBookInfoPredictions['Title'] = 'Why Nations Fail'
exampleBookInfoPredictions['Author'] = ' Daron Acemoglu and James Robinson'
exampleBookInfoPredictions['Genre'] = 'Economics'
exampleBookInfoPredictions['Publisher'] = 'Crown Business'
exampleBookInfoPredictions['FileName'] = 'example_image_homepage.jpg'

# configure the app
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BooksPredictions.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'the random string'    
db.init_app(app)
nav = Navigation(app)
with app.app_context():
    db.create_all()
    
# nav bar configure
nav.Bar('top', [
    nav.Item('Home', 'home_page'),
    nav.Item('Upload Book Cover', 'upload_cover'),
    nav.Item('Show Books Genre Pred Database', 'show_all_genre_pred', {'page': 1}),
    nav.Item('Show Books Info Pred Database', 'show_all_book_info', {'page': 1}),
    nav.Item('About Us', 'about_us'),
])

#function to check file type
def allowed_file(filename):     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('homepage.html', image = 'static/example_image_homepage.jpg', exampleBookGenrePredictions=exampleBookGenrePredictions,
                           exampleBookInfoPredictions = exampleBookInfoPredictions)
    
@app.route('/uploadImage', methods=['POST', 'GET'])
def upload_cover():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('upload_cover'))
        file = request.files['file']
        if file and not allowed_file(file.filename):
            flash('Not a Valid File, must be a png, jpg or jpeg', 'error')
            return redirect(url_for('upload_cover'))
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # genre predict model
            genre, confidence = model.predict_genre('static/' + filename)
            session['book_genre_predictions'] = {'Genre': genre, 'Confidence':str(confidence), 'File Name':filename}
            print(session['book_genre_predictions'])
            
            # add ocr model
            
            
            
            
        return redirect(url_for('book_details'))
    return render_template('uploadCover.html')

@app.route('/bookDetails')
def book_details():
    book_genre_predictions=session['book_genre_predictions']
    # book_info_predictions = session['book_info_predictions']
    book_info_predictions = exampleBookInfoPredictions
    commitBookGenrePred = BooksPredictions(book_genre_predictions['Genre'], book_genre_predictions['Confidence'], book_genre_predictions['File Name'])
    db.session.add(commitBookGenrePred)
    db.session.commit()
    return render_template('book_details.html', book_genre_predictions = book_genre_predictions, image = 'static/' + book_genre_predictions['File Name'], book_info_predictions = book_info_predictions)

@app.route('/show_all_genre_pred')
def show_all_genre_pred():
   return render_template('show_all_genre_pred.html', GenreBookPredictions = BooksPredictions.query.all())

@app.route('/show_all_book_info')
def show_all_book_info():
   return render_template('show_all_book_info.html', GenreInfoPredictions = BooksInformation.query.all())

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/hello')
def hello():
    print(exampleBookInfoPredictions['FileName'])
    me = BooksInformation(exampleBookInfoPredictions['Title'], exampleBookInfoPredictions['Author'], exampleBookInfoPredictions['Genre'], exampleBookInfoPredictions['Publisher'],exampleBookInfoPredictions['FileName'])
    db.session.add(me)
    db.session.commit()
    return 'done'

if __name__ == '__main__':
    app.run(debug=True)
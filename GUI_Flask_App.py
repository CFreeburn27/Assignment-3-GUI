from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_navigation import Navigation
import os
from booksDatabase import db, Books

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = './static/'

exampleBookDetails = {}
exampleBookDetails['Title'] = 'Why Nations Fail'
exampleBookDetails['Author'] = ' Daron Acemoglu and James Robinson'
exampleBookDetails['Genre'] = 'Economics'
exampleBookDetails['Publisher'] = 'Crown Business'

app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'the random string'    
db.init_app(app)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'home_page'),
    nav.Item('Upload Book Cover', 'upload_cover'),
    nav.Item('Show Books Database', 'show_database', {'page': 1}),
    nav.Item('About Us', 'about_us'),
])

def allowed_file(filename):     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('homepage.html', image = 'static/why_nations_fail.jpg', exampleBookDetails=exampleBookDetails)
    

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
            print(file)
        return redirect(url_for('book_details'))
    return render_template('uploadCover.html')

@app.route('/bookDetails', methods=["POST", 'GET'])
def book_details():
    if request.method == "POST":
        bookid = request.form["booktitle"]
        print(bookid)
    return render_template('book_details.html', bookDetails=exampleBookDetails, image = 'static/why_nations_fail.jpg')

@app.route('/show_all')
def show_database():
   return render_template('show_all.html', Books = Books.query.all())

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    app.run(debug=True)
    
#           <th> Author </th>>
#       <td name="bookauthor">{{  bookDetails['Author']}}</td>
#    </tr>

#       <th> Genre </th>>
#       <td name="bookgenre">{{  bookDetails['Genre']}}</td>
# </tr>
# </tr>
#       <th> Publisher </th>>
#       <td name="bookpublisher">{{  bookDetails['Publisher']}}</td>
# </tr>
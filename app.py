from flask import *
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyrebase
from forms import TodoForm, SignUpForm, LoginForm, ResetPass
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = 'sievny'
hashedpass = bcrypt.generate_password_hash(password)
print(hashedpass)

config = {
    'apiKey': "AIzaSyAYMqdrzuf10KiK8lbCTPddWT-gjVe2wOM",
    'authDomain': "pythonproject-81103.firebaseapp.com",
    'databaseURL': "https://pythonproject-81103.firebaseio.com",
    'projectId': "pythonproject-81103",
    'storageBucket': "pythonproject-81103.appspot.com",
    'messagingSenderId': "62312623081",
    'appId': "1:62312623081:web:0acc4d47500c9a384df978",
    'measurementId': "G-QTQC0KL73W"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


auth = firebase.auth()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

######SET DATABASE##########

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    complete = db.Column(db.Boolean)

    def __init__(self,title,description,complete=False):
        self.title = title
        self.description = description
        self.complete = complete
        

    # def __repr__(self):
    #     if self.complete:
    #         return f'Todo {self.id} \n {self.description} \n completed'
    #     else:
    #         return f'Todo {self.id} \n {self.description} \n Not completed'

@app.route('/',methods=['POST', 'GET'])
def index():
    todos = TodoList.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add',methods=['POST', 'GET'])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = TodoList(title,description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html',form=form)

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    delete_todo = TodoList.query.filter_by(id=todo_id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/update/<init:todo_id>')
# def update(todo_id):
#     update_todo = TodoList.query.filter_by(id=todo_id).first()
#     update_todo.complete = not update_todo.complete
#     db.session.commit()
#     return redirect(url_for('index'))
@app.route('/update/<int:todo_id>')
def update(todo_id):
    update_todo = TodoList.query.filter_by(id=todo_id).first()
    update_todo.complete = not update_todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/signup',methods=['POST', 'GET'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            auth.create_user_with_email_and_password(email,password)
            return redirect(url_for('index'))
        except:
            return redirect(url_for('signup'))
    return render_template('signup.html',form=form)

@app.route('/signin',methods=['POST', 'GET'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('index'))
        except:
            return redirect(url_for('signup'))
    return render_template('signin.html',form=form)
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'this is a secret key'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, username, email, password=None):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class QuizAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    quiz_name = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('answers', lazy=True))


with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            return render_template('register.html', error="All fields are required.")
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            return render_template('register.html', error='Email already registered')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect('/select_quiz')

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('login.html', error="Please fill in all fields.")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('select_quiz'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/select_quiz')
@login_required
def select_quiz():
    return  render_template('select_quiz.html', username=current_user.username)

@app.route('/food_quiz')
@login_required
def food_quiz():
    return render_template('food_quiz.html')

@app.route('/music_quiz')
@login_required
def music_quiz():
    return render_template('music_quiz.html')

@app.route('/history_quiz')
@login_required
def history_quiz():
    return render_template('history_quiz.html')

@app.route('/travel_quiz')
@login_required
def travel_quiz():
    return render_template('travel_quiz.html')

@app.route('/psychology_quiz')
@login_required
def psychology_quiz():
    return render_template('psychology_quiz.html')

@app.route('/special_quiz')
@login_required
def special_quiz():
    return render_template('special_quiz.html')

if __name__ == "__main__":
    app.run(debug=True)


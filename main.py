import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin, login_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm,HotelForm
from flask_bootstrap import Bootstrap5

app=Flask(__name__)
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY')
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DB_URI',"sqlite:///hotmess.db")
db=SQLAlchemy(model_class=Base)
db.init_app(app)

class Form(db.Model):
    __tablename__="form"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String)
    ratings:Mapped[float]=mapped_column(Float)
    service:Mapped[float]=mapped_column(Float)
    map_url:Mapped[str]=mapped_column(String)

class User(UserMixin,db.Model):
    __tablename__='users'
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String)
    password:Mapped[str]=mapped_column(String)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hotels')
def hotel():
    result=db.session.execute(db.select(Form))
    posts=result.scalars().all()
    return render_template('hotels.html',all_posts=posts,current_user=current_user)

@app.route('/signup',methods=["GET", "POST"])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.name == form.name.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login_in'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template('Signup.html',form=form)

@app.route('/login',methods=["GET", "POST"])
def login_in():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.name == form.name.data))
        user = result.scalar()
        if not user:
            flash("You are not registered with us sign up instead")
            return redirect(url_for('sign_up'))
        elif not check_password_hash(user.password, form.password.data):
            flash("Uh-Oh,Password you entered is incorrect.")
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html',form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add',methods=["GET", "POST"])
def add():
    h_form=HotelForm()
    if h_form.validate_on_submit():
        new_hotel=Form(
            name=h_form.h_name.data,
            ratings=h_form.ratings.data,
            service=h_form.service.data,
            map_url=h_form.map_url.data,
        )
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for('hotel'))
    return render_template('add.html',form=h_form)

if __name__=="__main__":
    app.run(debug=True)
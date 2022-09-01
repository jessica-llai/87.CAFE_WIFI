from flask import Flask, render_template, flash,request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, delete
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager



app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.secret_key='my secret key'
db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url=db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



class CafeForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    location = StringField('location',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    map = StringField('map_url', validators=[DataRequired()])
    img = StringField('img_url', validators=[DataRequired()])
    submit=SubmitField('Done')

class UserForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Done')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Done')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cafe')
def show_cafe():
    cafes=Cafe.query.all()
    return render_template('cafe.html',cafes=cafes)

@app.route('/add_cafe', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        new_cafe = Cafe(
            name=form.name.data,
            location=form.location.data,
            coffee_price=form.price.data,
            map_url=form.map.data,
            img_url=form.img.data
        )
        print(new_cafe)

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('new_cafe.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            name = request.form['name'],
            email = request.form['email'],
            password=request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logged in successfully.')
        return redirect(url_for('home'))

    return render_template('login.html', form=form)
# Press the green button in the gutter to run the script.



if __name__ == '__main__':
    app.run(debug=True)


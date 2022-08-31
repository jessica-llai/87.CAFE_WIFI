from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, delete
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.secret_key='my secret key'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url=db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

db.create_all()

class CafeForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    location = StringField('location',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    map = StringField('map_url', validators=[DataRequired()])
    img = StringField('img_url', validators=[DataRequired()])
    submit=SubmitField('Done')


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
            name = request.form['name'],
            location = request.form['location'],
            prices = request.form['price'],
            map_url=request.form['map'],
            img_url=request.form['img']
        )
        db.session.add(new_cafe)
        db.session.commit()

    return render_template('new_cafe.html', form=form)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask , render_template , flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


#create flask intance

app=Flask(__name__)
#create a db
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY'] = "MYSUPERDUPERKEY"

#initilalize the db
db = SQLAlchemy(app)


#create model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False , unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image = db.Column(db.String(20), nullable=False , default='default.jpeg')
    password = db.Column(db.String(60), nullable=False )
    posts = db.relationship('Post', backref='author' , lazy=True)

#create a string 

def __repr__(self):
    return  f"Users('{self.name}' , '{self.email}' , '{self.image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    content= db.Column(db.Text , nullable=False)
    user_id=db.Column(db.Integer , db.ForeignKey('Users.id') , nullable=False)
    user =db.relationship('User', primaryjoin='Post.user_id == User.id', back_populates='posts')

def __repr__(self):
    return  f"Post('{self.title}' , '{self.date_added}' ,)"


# create a form class


class userform(FlaskForm):
    name=StringField(" name", validators=[DataRequired()])
    email=StringField(" email", validators=[DataRequired()])
    submit=SubmitField("Submit")

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form=userform()
   
    if form.validate_on_submit():
        user= Users.query.filter_by(email=form.email.data).first()
        if user is None:
          user=Users(name=form.name.data , email = form.email.data)
          db.session.add(user)
          db.session.commit()
          name = form .name.data 
          form.email.data='' 
          form.name.data = ''
          flash("User added successfully ")
        flash("form submitted successfully")
    our_users= Users.query.order_by(Users.date_added)
    return render_template("add_user.html" , form=form ,name=name  , our_users=our_users)

# create a form class
class nameform(FlaskForm):
    name=StringField("Your name", validators=[DataRequired()])
    submit=SubmitField("Submit")




#local host:5000/user/john
app.route('/user/<name>')

def user(name):
    return "<h1> Hello {} </h1>".format(name)




@app.route('/')

def index():
    return "<h1> Hello WORLD !! </h1>"

@app.route("/index")
def index1():
   first_name="Mumo"
   stuff="This is  <strong> Bold </strong>Text"
   favourite_pizza=[23,234,5,45,6,536,]
   return render_template("index2.html", first_name=first_name,stuff=stuff,favourite_pizza=favourite_pizza)

@app.route('/user/<name>')
def user(name):
   return render_template("user.html", user_name=name) 
 

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found500(e):
    return render_template("500.html" ), 500

#create name page
@app.route("/name", methods=["GET", "POST"])
def get_name():
    user_name = None
    form = nameform()  # Ensure that your form class is named NameForm, not nameform

    if form.validate_on_submit():
        user_name = form.name.data
        form.name.data = ''
        flash("form submitted successfully")

    return render_template("name.html", name=user_name, form=form)



app.debug = True
app.run()
app.run(debug = True)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
   app.run()
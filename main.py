from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

email_id = "dineshshah960@gmail.com"
email_pass = "SelenaGomez"


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    posts = BlogPost.query.get(index)
    requested_post = posts.to_dict()
    return render_template("post.html", post=requested_post)


@app.route("/edit_post<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    if request.method == 'GET':
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        return render_template("make-post.html", form=edit_form, msg="Edit Post")
    elif request.method == "POST":
        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.author = request.form['author']
        post.img_url = request.form['img_url']
        post.body = request.form['body']
        db.session.commit()
        return redirect(url_for('show_post', index=post_id))


@app.route("/new-post", methods=['GET', 'POST'])
def add_post():
    today = date.today().strftime("%B %d, %Y")
    form = CreatePostForm()
    if request.method == "POST":
        new_blog = BlogPost(title=request.form['title'], subtitle=request.form['subtitle'], date=today,
                            author=request.form['author'], img_url=request.form['img_url'],
                            body=request.form['body'])
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form, msg="New Post")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/delete/<int:post_id>")
def delete_blog(post_id):
    del_blog = BlogPost.query.get(post_id)
    db.session.delete(del_blog)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(message)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(email_id, email_pass)
            connection.sendmail(from_addr=email_id, to_addrs="dineshtamang7263@gmail.com",
                                                                msg="subject: customer feedback \n\n"
                                                                            f"Name: {name} \n"
                                                                            f"Email: {email} \n "
                                                                            f"Phone: {phone} \n "
                                                                            f"message: {message}")
        return redirect(url_for('contact'))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Session
from sqlalchemy.inspection import inspect
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts", lazy='subquery')
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # ***************Parent Relationship*************#
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # ***************Child Relationship*************#
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()
    post = BlogPost.query.get(2)
    for comment in post.comments:
        print(comment.comment_author.name)







# with app.app_context():
#     # new_user = User(
#     #     name="Sameer Ansari",
#     #     email="sameeransari663@gmail.com",
#     #     password=generate_password_hash(
#     #         "123",
#     #         method="pbkdf2:sha256",
#     #         salt_length=8
#     #     )
#     # )
#     # db.session.add(new_user)

# with app.app_context():
#     new_blog = BlogPost(
#         author_id=1,
#         title="The life of a cactus",
#         subtitle="Cacti are succulent perennial plants.",
#         date=date.today().strftime("%B %d, %Y"),
#         body="cactus, (family Cactaceae), plural cacti or cactuses, flowering plant family (order Caryophyllales) with nearly 2,000 species and 139 genera. Cacti are native through most of the length of North and South America, from British Columbia and Alberta southward; the southernmost limit of their range extends far into Chile and Argentina. Mexico has the greatest number and variety of species. The only cacti possibly native to the Old World are members of the genus Rhipsalis, occurring in East Africa, Madagascar, and Sri Lanka. Although a few cactus species inhabit tropical or subtropical areas, most live in and are well adapted to dry regions. See also list of plants in the family Cactaceae.",
#         img_url="https://cdn.britannica.com/08/100608-050-684264CB/Saguaro-cactus-Arizona.jpg?w=400&h=300&c=crop"
#     )
#     db.session.add(new_blog)
#     db.session.commit()


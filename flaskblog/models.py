from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    cover_photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text(), nullable=True)
    dob = db.Column(db.DateTime(), nullable=True)
    location = db.Column(db.String(64),nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.now(),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('PostMetadata', backref='author_comment', lazy=True)


    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.cover_photo}','{self.bio}', '{self.dob}','{self.location}','{self.member_since}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_img = db.Column(db.String(20), nullable=True)
    comments = db.relationship('PostMetadata', backref='posts', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PostMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # emotion = db.Column(db.Boolean(), nullable=True)
    emotion = db.Column(db.Integer(), nullable=False, default=-1)
    post_comment = db.Column(db.Text(), nullable=True)
    comment_img = db.Column(db.String(20), nullable=True)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"PostMetadata('{self.id}','{self.emotion}', '{self.post_comment}', '{self.post_id}','{self.user_id}', '{self.date_commented}')"


    
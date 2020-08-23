import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog.posts.forms import CommentForm
from flaskblog.models import PostMetadata
from flask_login import current_user
from flaskblog import db



def save_postimg(form_postimg):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_postimg.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pictures', picture_fn)
    print("save post image")
    output_size = (300, 300)
    i = Image.open(form_postimg)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_commentimg(form_commentimg):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_commentimg.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/comment_pictures', picture_fn)
    print("save comment image")
    output_size = (300, 300)
    i = Image.open(form_commentimg)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_comment(post):
    form = CommentForm()
    if form.commentimg.data:
        commentimg_file = save_commentimg(form.commentimg.data)
    else:
        commentimg_file = None
    postcomment = PostMetadata(post_comment=form.comment.data, comment_img=commentimg_file, author_comment=current_user, posts=post)
    db.session.add(postcomment)
    db.session.commit()

def getEmotionCount(comments):
    countLike = 0
    countDislike=0
    for comment in comments:
        if comment.emotion == 1:
            countLike = countLike + 1
        elif comment.emotion == 0:
            countDislike = countDislike + 1
    return countLike, countDislike
            
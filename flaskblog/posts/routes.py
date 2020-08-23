from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post,PostMetadata
from flaskblog.posts.forms import PostForm,CommentForm
from datetime import datetime
from flaskblog.posts.utils import save_postimg, save_commentimg,save_comment,getEmotionCount


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.postimg.data:
            postimg_file = save_postimg(form.postimg.data)
        else:
            postimg_file = None
            # current_user.postimg_file = postimg_file
        post = Post(title=form.title.data, content=form.content.data, post_img=postimg_file, author=current_user)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    form = CommentForm()
    post_selected = Post.query.get_or_404(post_id)   
    if request.method == 'GET':
        comments = PostMetadata.query.filter(post_id == post_id).all()
        like_count, dislike_count=getEmotionCount(comments)
        return render_template('comments.html', form=form, title=post_selected.title, post=post_selected,
                                comments=comments, like_count=like_count, dislike_count=dislike_count ,today=datetime.now())
    else:
        save_comment(post_selected)
        return redirect(url_for('posts.post', post_id=post_id))




@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.postimg.data:
            postimg_file = save_postimg(form.postimg.data)
        else:
            if post.post_img:
                postimg_file=post.post_img
            else:
                postimg_file = None
          
        post.post_img=postimg_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.postimg.data= post.post_img 

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post', postimg=post.post_img)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = PostMetadata.query.get_or_404(comment_id)
    post_id=comment.post_id
    if comment.author_comment != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))
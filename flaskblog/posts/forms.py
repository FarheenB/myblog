from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Optional


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    postimg = FileField('Add Image', validators=[FileAllowed(['jpg', 'png', 'jpeg']),Optional(strip_whitespace=True)])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('', validators=[DataRequired(),Optional(strip_whitespace=True)])
    commentimg = FileField('Add Image', validators=[FileAllowed(['jpg', 'png', 'jpeg']),Optional(strip_whitespace=True)])
    submit = SubmitField('Comment')
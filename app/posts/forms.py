from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = StringField('Content',validators=[DataRequired()])
	video = StringField('Video Link	',validators=[Length(min=0,max=80)])
	photo1 = FileField('Add photo',validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Submit')

class UpdatePostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = StringField('Content',validators=[DataRequired()])
	video = StringField('Video Link',validators=[Length(min=0,max=80)])
	photo1 = FileField('Add photo',validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

class StartForm(FlaskForm):
	submit = SubmitField('Get Started')	
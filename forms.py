from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class ReviewForm(FlaskForm):
    author = StringField('Имя', validators=[DataRequired(), Length(max=80)])
    rating = IntegerField('Оценка (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    content = TextAreaField('Отзыв', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Отправить')


class ReplyForm(FlaskForm):
    author = StringField('Имя', validators=[DataRequired(), Length(max=80)])
    content = TextAreaField('Ответ', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Ответить')
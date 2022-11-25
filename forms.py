from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField,\
    PasswordField, BooleanField, SubmitField
import os


class SelectForm(FlaskForm):
    lista = ['merge_pdf', 'jpeg_to_pdf']
    choices = SelectField(u'', choices = [
        (i,i) for i in lista])
    submit = SubmitField(u'submit')
    clear = SubmitField(u'clear')
    download = SubmitField(u'Download')

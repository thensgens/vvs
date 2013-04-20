"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators


class ExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField('Description', validators=[validators.Required()])


class ChatForm(wtf.Form):
    user_name = wtf.TextField('name', validators=[validators.Required()])
    chat_msg = wtf.TextAreaField('msg', validators=[validators.Required()])
    submit = wtf.SubmitField('Send Message')

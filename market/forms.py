from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired


class RegisterForm(FlaskForm):
    username=StringField(label='User Name',validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label='Email Address',validators=[Email(),DataRequired()])
    pass1=PasswordField(label='Password1',validators=[Length(min=6),DataRequired()])
    pass2=PasswordField(label='password2',validators=[EqualTo('pass1')])

    submit=SubmitField(label='submit')
                   
    
class LoginForm(FlaskForm):
    username=StringField(label='User Name',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='submit')



class PurchaseForm(FlaskForm):
    submit=SubmitField('Purchase')
class SellItemForm(FlaskForm):
    submit=SubmitField('Sell Item Form')
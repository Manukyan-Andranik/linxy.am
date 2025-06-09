# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from models import User  # This is now safe

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    account_type = SelectField('Account Type', choices=[('brand', 'Brand/Company'), ('influencer', 'Influencer')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class InfluencerProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    website = StringField('Website')
    instagram = StringField('Instagram Handle')
    youtube = StringField('YouTube Channel')
    tiktok = StringField('TikTok Handle')
    categories = StringField('Categories (comma separated)')
    location = StringField('Location')
    followers = IntegerField('Total Followers')
    engagement = StringField('Average Engagement Rate')
    submit = SubmitField('Update Profile')

class CampaignForm(FlaskForm):
    title = StringField('Campaign Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    budget = IntegerField('Budget (AMD)', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    requirements = TextAreaField('Requirements')
    target_gender = SelectField('Target Gender', choices=[
        ('any', 'Any'), 
        ('male', 'Male'), 
        ('female', 'Female'),
        ('other', 'Other')
    ])
    target_age_min = IntegerField('Minimum Age')
    target_age_max = IntegerField('Maximum Age')
    target_location = StringField('Target Location')
    submit = SubmitField('Create Campaign')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    card_expiry = StringField('Expiry Date (MM/YY)', validators=[DataRequired(), Length(min=5, max=5)])
    card_cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Complete Payment')
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, 
    SelectField, IntegerField, DecimalField,
    BooleanField, DateField, DateTimeField
)
from wtforms.validators import DataRequired, Email, Length, Optional
from models import User

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', choices=[
        ('user', 'User'), 
        ('influencer', 'Influencer'), 
        ('admin', 'Admin')
    ])
    is_active = BooleanField('Active', default=True)

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Length(max=100)])
    bio = TextAreaField('Bio')
    website = StringField('Website', validators=[Length(max=200)])
    social_media = TextAreaField('Social Media (format: platform: username)')
    categories = StringField('Categories (comma separated)')
    location = StringField('Location', validators=[Length(max=100)])
    profile_pic = StringField('Profile Picture URL', validators=[Length(max=200)])
    stats = TextAreaField('Stats (format: metric: value)')
    is_verified = BooleanField('Verified')

class CampaignForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    budget = IntegerField('Budget (AMD)')
    status = SelectField('Status', choices=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])
    start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeField('End Date', format='%Y-%m-%d %H:%M:%S')
    requirements = TextAreaField('Requirements')
    # Target audience fields
    target_audience_gender = StringField('Target Gender')
    target_audience_age_min = IntegerField('Target Min Age')
    target_audience_age_max = IntegerField('Target Max Age')
    target_audience_location = StringField('Target Location')

class CollaborationForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ])
    offer_amount = IntegerField('Offer Amount (AMD)')
    influencer_notes = TextAreaField('Influencer Notes')
    brand_notes = TextAreaField('Brand Notes')

class DeliverableForm(FlaskForm):   
    type = StringField('Type', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M:%S')
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])

class PaymentForm(FlaskForm):
    amount = IntegerField('Amount (AMD)', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ])
    payment_method = StringField('Payment Method', validators=[Length(max=50)])
    transaction_id = StringField('Transaction ID', validators=[Length(max=100)])


class SubscriptionForm(FlaskForm):
    plan = SelectField('Plan', choices=[
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise')
    ])
    period = SelectField('Period', choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ])
    status = SelectField('Status', choices=[
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired')
    ])
    start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeField('End Date', format='%Y-%m-%d %H:%M:%S')
    stripe_subscription_id = StringField('Stripe Subscription ID', validators=[Length(max=100)])
    payment_method = StringField('Payment Method', validators=[Length(max=50)])
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from sqlalchemy import or_
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from models import (
    User, Profile, Subscription, Campaign, 
    Collaboration, Deliverable, Payment, Message
)
from . import admin_bp
from .forms import (
    UserForm, ProfileForm, CampaignForm, 
    CollaborationForm, DeliverableForm, PaymentForm
)

@admin_bp.route('/')
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_influencers': User.query.filter_by(role='influencer').count(),
        'total_campaigns': Campaign.query.count(),
        'active_campaigns': Campaign.query.filter_by(status='active').count(),
        'pending_collaborations': Collaboration.query.filter_by(status='pending').count(),
        'pending_payments': Payment.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# User Management
@admin_bp.route('/users')
def user_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(
            User.username.ilike(f'%{search}%'),
            User.email.ilike(f'%{search}%')
        )
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/users/list.html', users=users, search=search)

@admin_bp.route('/users/<int:user_id>')
def user_view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/users/view.html', user=user)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.user_view', user_id=user.id))
    
    return render_template('admin/users/edit.html', form=form, user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.user_list'))

# Profile Management
@admin_bp.route('/profiles/<int:profile_id>/edit', methods=['GET', 'POST'])
def profile_edit(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    form = ProfileForm(obj=profile)
    
    if form.validate_on_submit():
        form.populate_obj(profile)
        
        # Handle JSON fields
        if form.social_media.data:
            profile.social_media = {
                line.split(':')[0].strip(): line.split(':')[1].strip()
                for line in form.social_media.data.split('\n')
                if ':' in line
            }
        
        if form.categories.data:
            profile.categories = [cat.strip() for cat in form.categories.data.split(',')]
        
        if form.stats.data:
            profile.stats = {
                line.split(':')[0].strip(): float(line.split(':')[1].strip())
                for line in form.stats.data.split('\n')
                if ':' in line
            }
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('admin.user_view', user_id=profile.user_id))
    
    # Pre-populate JSON fields as strings
    if profile.social_media:
        form.social_media.data = '\n'.join(
            f"{k}: {v}" for k, v in profile.social_media.items()
        )
    
    if profile.categories:
        form.categories.data = ', '.join(profile.categories)
    
    if profile.stats:
        form.stats.data = '\n'.join(
            f"{k}: {v}" for k, v in profile.stats.items()
        )
    
    return render_template('admin/profiles/edit.html', form=form, profile=profile)

# Campaign Management
@admin_bp.route('/campaigns')
def campaign_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Campaign.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    campaigns = query.order_by(Campaign.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/campaigns/list.html', campaigns=campaigns, status=status)

@admin_bp.route('/campaigns/<int:campaign_id>')
def campaign_view(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    collaborations = Collaboration.query.filter_by(campaign_id=campaign_id).all()
    return render_template('admin/campaigns/view.html', campaign=campaign, collaborations=collaborations)

@admin_bp.route('/campaigns/<int:campaign_id>/edit', methods=['GET', 'POST'])
def campaign_edit(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm(obj=campaign)
    
    if form.validate_on_submit():
        form.populate_obj(campaign)
        
        # Handle JSON fields
        if form.target_audience_gender.data or form.target_audience_age_min.data or form.target_audience_age_max.data or form.target_audience_location.data:
            campaign.target_audience = {
                'gender': form.target_audience_gender.data,
                'age_min': form.target_audience_age_min.data,
                'age_max': form.target_audience_age_max.data,
                'location': form.target_audience_location.data
            }
        
        db.session.commit()
        flash('Campaign updated successfully', 'success')
        return redirect(url_for('admin.campaign_view', campaign_id=campaign.id))
    
    # Pre-populate JSON fields
    if campaign.target_audience:
        form.target_audience_gender.data = campaign.target_audience.get('gender', '')
        form.target_audience_age_min.data = campaign.target_audience.get('age_min', '')
        form.target_audience_age_max.data = campaign.target_audience.get('age_max', '')
        form.target_audience_location.data = campaign.target_audience.get('location', '')
    
    return render_template('admin/campaigns/edit.html', form=form, campaign=campaign)

# Similar views for Collaboration, Deliverable, Payment, etc.
# Implementation would follow the same pattern as above
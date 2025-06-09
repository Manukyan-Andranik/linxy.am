import os
import json
from datetime import datetime, timedelta

import stripe
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from sqlalchemy import or_, and_
from sqlalchemy import cast, Integer

from flask_migrate import Migrate
from flask_mail import Mail
from werkzeug.utils import secure_filename

from config import Config
from extensions import db, login_manager, migrate, mail
from forms import (
    LoginForm, RegistrationForm, InfluencerProfileForm, CampaignForm,
    MessageForm, PaymentForm
)
from models import (
    User, Profile, Subscription, Campaign, Collaboration,
    Deliverable, Payment, Message, Influencer
)

from data_manager import DataManager, get_recommendation_reason, recommend_influencers

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions properly
db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)

# Initialize LoginManager and set login view
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

data_manager = DataManager(
        dbname="linxy",
        user="linxy_admin",
        password="securepassword123.",
        host="localhost",
        port="5432"
    )

# Initialize Stripe with secret key
stripe.api_key = app.config.get('STRIPE_SECRET_KEY')

@app.template_filter('float_format')
def float_format_filter(value, format_str='%.2f', skip_none=False):
    if skip_none and (value is None or value == ''):
        return ''
    try:
        return format_str % float(value)
    except (ValueError, TypeError):
        return value

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='influencer' if form.account_type.data == 'influencer' else 'user'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Create profile if influencer
        if form.account_type.data == 'influencer':
            profile = Profile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()

        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    # Get the user profile data
    user = User.query.filter_by(username=username).first_or_404()
    profile = Profile.query.filter_by(user_id=user.id).first()
    subscription = Subscription.query.filter_by(user_id=user.id).first()
    
    # Get campaigns created by this user (if they're a brand)
    campaigns = Campaign.query.filter_by(creator_id=user.id).order_by(Campaign.created_at.desc()).limit(5).all()
    
    # Get collaborations (if they're an influencer)
    collaborations = Collaboration.query.filter_by(influencer_id=user.id).order_by(Collaboration.created_at.desc()).limit(5).all()
    
    # Get stats for influencers
    if user.is_influencer():
        completed_collabs = Collaboration.query.filter_by(
            influencer_id=user.id, 
            status='completed'
        ).count()
        
        total_earnings = db.session.query(
            db.func.sum(Payment.amount)
            .filter(
                Payment.collaboration_id == Collaboration.id,
                Collaboration.influencer_id == user.id,
                Payment.status == 'paid'
            ).scalar() or 0)
    else:
        completed_collabs = None
        total_earnings = None
    
    return render_template(
        'profile.html',
        user=user,
        profile=profile,
        subscription=subscription,
        campaigns=campaigns,
        collaborations=collaborations,
        completed_collabs=completed_collabs,
        total_earnings=total_earnings
    )

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(
            user_id=current_user.id,
            full_name=form.full_name.data,
            bio=form.bio.data,
            website=form.website.data,
            social_media={
                'instagram': form.instagram.data,
                'youtube': form.youtube.data,
                'tiktok': form.tiktok.data,
                'twitter': form.twitter.data
            },
            categories=form.categories.data,
            location=form.location.data,
            profile_pic=form.profile_pic.data,
            stats={
                'followers': form.followers.data,
                'engagement': form.engagement.data
            }
        )
        db.session.add(profile)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('profile/edit.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    campaigns = Campaign.query.filter_by(creator_id=current_user.id).order_by(Campaign.created_at.desc()).limit(5).all()
    collaborations = Collaboration.query.filter_by(influencer_id=current_user.id).order_by(Collaboration.created_at.desc()).limit(5).all()
    # Get AI recommendations
    recommended_influencers = recommend_influencers()
    # Calculate stats
    active_campaigns = Campaign.query.filter_by(creator_id=current_user.id, status='active').count()
    total_influencers = Collaboration.query.filter(Collaboration.campaign_id.in_(
        [c.id for c in Campaign.query.filter_by(creator_id=current_user.id).all()]
    )).count()

    return render_template('dashboard.html',
                           recommended_influencers=recommended_influencers,
                           campaigns=campaigns,
                           collaborations=collaborations,
                           active_campaigns=active_campaigns,
                           total_influencers=total_influencers)

@app.route("/influencers")   # LIST Influencers
@login_required
def browse_influencers():
    with DataManager(
        dbname="linxy",
        user="linxy_admin",
        password="securepassword123.",
        host="localhost",
        port="5432"
    ) as dm:
        all_influencers = dm.get_all_influencers(limit=100)
        for influencer in all_influencers:
            influencer_data = dm.get_influencer_data_points(influencer['id'])
            influencer['data_points'] = influencer_data
        return render_template('influencers.html', influencers=all_influencers)

@app.route('/influencer/<int:influencer_id>')    # VIEW Influencer Profile TODO
@login_required
def influencer_profile(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    # if influencer.role != 'influencer':
    #     flash('This user is not an influencer', 'warning')
    #     return redirect(url_for('browse_influencers'))

    profile = Profile.query.filter_by(user_id=influencer_id).first()
    return render_template('influencers/profile.html', influencer=influencer, profile=profile)

@app.route('/campaigns')    # LIST Campaigns
@login_required
def list_campaigns():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if current_user.role == 'influencer':
        collaborations = Collaboration.query.filter_by(influencer_id=current_user.id).all()
        campaign_ids = [c.campaign_id for c in collaborations]
        campaigns_pagination = Campaign.query.filter(Campaign.id.in_(campaign_ids)).order_by(Campaign.created_at.desc()).paginate(page=page, per_page=per_page)
    else:
        campaigns_pagination = Campaign.query.filter_by(creator_id=current_user.id).order_by(Campaign.created_at.desc()).paginate(page=page, per_page=per_page)

    # Manually add computed fields if necessary
    for campaign in campaigns_pagination.items:
        campaign.influencer_count = len(campaign.collaborations)
        campaign.brand = current_user.company_name if hasattr(current_user, 'company_name') else "N/A"

    return render_template('campaigns/list.html', campaigns=campaigns_pagination)


@app.route('/campaigns/<int:campaign_id>/view')    # VIEW Campaign
@login_required
def view_campaign(campaign_id):
    campaigns = Campaign.query.filter_by(creator_id=current_user.id).order_by(Campaign.created_at.desc()).limit(5).all()
    collaborations = Collaboration.query.filter_by(influencer_id=current_user.id).order_by(Collaboration.created_at.desc()).limit(5).all()
    # Get AI recommendations
    recommended_influencers = recommend_influencers()
    # Calculate stats
    active_campaigns = Campaign.query.filter_by(creator_id=current_user.id, status='active').count()
    total_influencers = Collaboration.query.filter(Collaboration.campaign_id.in_(
        [c.id for c in Campaign.query.filter_by(creator_id=current_user.id).all()]
    )).count()
    campaign = Campaign.query.get_or_404(campaign_id)

    return render_template('campaigns/view.html',
                            campaign=campaign,
                           
                           recommended_influencers=recommended_influencers,
                           campaigns=campaigns,
                           collaborations=collaborations,
                           active_campaigns=active_campaigns,
                           total_influencers=total_influencers)
    
    
    # Get existing collaborations
    collaborations = ''
    # = Collaboration.query.filter_by(campaign_id=campaign_id)\
    #     .options(db.joinedload(Collaboration.influencer))\
    #     .all()
    
    # Get recommended influencers
    campaign_prefs = campaign.get_influencer_preferences()
    recommended_influencers = Influencer.recommend_influencers(campaign_prefs)
    
    # Filter out influencers already in campaign
    existing_influencer_ids = {c.influencer_id for c in collaborations}
    influencers = [inf for inf in recommended_influencers 
                  if inf['id'] not in existing_influencer_ids]
    
    return render_template(
        'campaigns/view.html',
        campaign=campaign,
        collaborations=collaborations,
        influencers=influencers
    )

@app.route('/campaign/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role == 'influencer':
        flash('Influencers cannot create campaigns', 'warning')
        return redirect(url_for('dashboard'))

    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            title=form.title.data,
            description=form.description.data,
            creator_id=current_user.id,
            budget=form.budget.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            requirements=form.requirements.data,
            target_audience={
                'gender': form.target_gender.data,
                'age_min': form.target_age_min.data,
                'age_max': form.target_age_max.data,
                'location': form.target_location.data
            }
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Your campaign has been created!', 'success')
        return redirect(url_for('view_campaign', campaign_id=campaign.id))
    return render_template('campaigns/create.html', form=form)

@app.route('/collaboration/<int:collaboration_id>')
@login_required
def view_collaboration(collaboration_id):
    collaboration = Collaboration.query.get_or_404(collaboration_id)

    if current_user.id not in [collaboration.campaign.creator_id, collaboration.influencer_id]:
        flash('You do not have access to this collaboration', 'danger')
        return redirect(url_for('dashboard'))

    deliverables = Deliverable.query.filter_by(collaboration_id=collaboration_id).all()
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == collaboration.influencer_id)) |
        ((Message.sender_id == collaboration.influencer_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    form = MessageForm()
    return render_template('collaboration/view.html',
                           collaboration=collaboration,
                           deliverables=deliverables,
                           messages=messages,
                           form=form)

@app.route('/send_message/<int:recipient_id>', methods=['POST'])
@login_required
def send_message(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            recipient_id=recipient.id,
            body=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'success')
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/pricing')
def pricing():
    return render_template('payments/plans.html', plans=app.config.get('PRICING_PLANS', {}))

@app.route('/checkout/<plan>/<period>', methods=['GET', 'POST'])
@login_required
def checkout(plan, period):
    plans = app.config.get('PRICING_PLANS', {})
    if plan not in plans or period not in ['monthly', 'yearly']:
        flash('Invalid plan selected', 'danger')
        return redirect(url_for('pricing'))

    price = plans[plan].get(f'{period}_price')
    form = PaymentForm()

    if form.validate_on_submit():
        try:
            # Create Stripe customer if needed
            if not current_user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=current_user.email,
                    source=form.stripe_token.data
                )
                current_user.stripe_customer_id = customer.id
                db.session.commit()

            # Create subscription with Stripe price object ID
            # NOTE: You must have Stripe price IDs stored, product id is not sufficient
            # For demo, assuming price IDs stored in config as well:
            price_id = plans[plan].get(f'{period}_price_id')
            if not price_id:
                flash('Payment configuration error.', 'danger')
                return redirect(url_for('pricing'))

            subscription = stripe.Subscription.create(
                customer=current_user.stripe_customer_id,
                items=[{'price': price_id}],
                expand=['latest_invoice.payment_intent'],
            )

            # Save subscription info in DB
            new_subscription = Subscription(
                user_id=current_user.id,
                plan=plan,
                period=period,
                stripe_subscription_id=subscription.id,
                status=subscription.status,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30 if period == 'monthly' else 365)
            )
            db.session.add(new_subscription)
            db.session.commit()

            flash('Subscription successful! Thank you.', 'success')
            return redirect(url_for('dashboard'))

        except stripe.error.StripeError as e:
            flash(f'Payment error: {e.user_message}', 'danger')

    return render_template('payments/checkout.html', form=form, plan=plan, period=period, price=price)



@app.route('/payment/<plan_id>')
def payment(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Define your plans (in a real app, these would come from your database)
    plans = {
        'starter_monthly': {
            'id': 'starter_monthly',
            'name': 'Starter',
            'price': 20000,  # in smallest currency unit (cents, pence, etc.)
            'currency': 'amd',
            'interval': 'month',
            'features': [
                'Up to 5 active campaigns',
                'Basic influencer search',
                'Standard analytics dashboard',
                'Email support',
                'Up to 3 team members'
            ]
        },
        'starter_yearly': {
            'id': 'starter_yearly',
            'name': 'Starter',
            'price': 16000,
            'currency': 'amd',
            'interval': 'year',
            'features': [
                'Up to 5 active campaigns',
                'Basic influencer search',
                'Standard analytics dashboard',
                'Email support',
                'Up to 3 team members'
            ]
        },
        # Add other plans similarly
    }
    
    plan = plans.get(plan_id)
    if not plan:
        return redirect(url_for('pricing'))
    
    return render_template('payment.html', 
                         plan=plan, 
                         stripe_public_key=stripe_public_key,
                         current_user=current_user)

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    payment_method_id = data.get('payment_method_id')
    plan_id = data.get('plan_id')
    
    try:
        # Attach payment method to customer
        customer = stripe.Customer.create(
            payment_method=payment_method_id,
            email=data.get('email'),
            name=data.get('name'),
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                'price': get_stripe_price_id(plan_id),
            }],
            expand=['latest_invoice.payment_intent']
        )
        
        # Update user in your database
        current_user.stripe_customer_id = customer.id
        current_user.subscription_plan = plan_id
        db.session.commit()
        
        return jsonify({
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        })
        
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/payment/success')
def payment_success():
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect(url_for('pricing'))
    
    try:
        # Retrieve the Checkout Session
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Here you would typically update your database with the subscription details
        # For example:
        # current_user.subscription_active = True
        # current_user.subscription_id = session.subscription
        # db.session.commit()
        
        return render_template('payment_success.html', session=session)
    except Exception as e:
        return redirect(url_for('pricing'))

def get_stripe_price_id(plan_id):
    # Map your plan IDs to Stripe Price IDs
    price_map = {
        'starter_monthly': 'price_123',  # Your actual Stripe price IDs
        'starter_yearly': 'price_456',
        # Add other plans
    }
    return price_map.get(plan_id)

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = app.config.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return jsonify(success=False), 400

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        # Update subscription/payment status in DB if needed

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Update subscription status to canceled

    # Add more event types as needed

    return jsonify(success=True), 200

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) 
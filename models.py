import os
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from data_manager import DataManager  
from extensions import db, login_manager

Base = declarative_base()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(200), default='default_profile_pic.jpg')  # 👈 Added this line
    subscription = db.relationship('Subscription', backref='user', lazy=True, uselist=False)
    campaigns = db.relationship('Campaign', backref='creator', lazy=True)
    profile = db.relationship('Profile', backref='user', lazy=True, uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_influencer(self):
        return self.role == 'influencer'

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.Text, default='client_default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    data_points = db.relationship('InfluencerDataPoint', backref='influencer', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def recommend_influencers(cls, campaign_preferences=None):
        # Get all influencers with their data points
        all_influencers = Influencer.query.options(
            db.joinedload(Influencer.data_points)
        ).all()
        
        # Convert to dict format for compatibility
        influencers_data = []
        for inf in all_influencers:
            if not inf.data_points:
                continue
                
            dp = inf.data_points[0]
            inf_dict = {
                'id': inf.id,
                'full_name': inf.full_name,
                'photo': inf.photo,
                'data_points': [{
                    'subs': dp.subs or 0,
                    'engagement_rate': float(dp.engagement_rate or 0),
                    'price_reels_creative': dp.price_reels_creative or 0,
                    'men': float(dp.men or 0),
                    'women': float(dp.women or 0),
                    'age_13_17': float(dp.age_13_17 or 0),
                    'age_18_24': float(dp.age_18_24 or 0),
                    'age_25_34': float(dp.age_25_34 or 0),
                    'age_35_44': float(dp.age_35_44 or 0),
                    'armenia': float(dp.armenia or 0),
                    'russia': float(dp.russia or 0),
                    'usa': float(dp.usa or 0),
                    'category': dp.category or 'general'
                }]
            }
            influencers_data.append(inf_dict)

        # Prepare features for recommendation
        features = []
        for inf in influencers_data:
            dp = inf["data_points"][0]
            features.append([
                dp.get("subs", 0),
                dp.get("engagement_rate", 0),
                dp.get("price_reels_creative", 0),
                dp.get("men", 0),
                dp.get("women", 0),
                dp.get("age_18_24", 0),
                dp.get("age_25_34", 0),
                dp.get("age_35_44", 0),
                dp.get("armenia", 0),
                dp.get("russia", 0),
                dp.get("usa", 0)
            ])

        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        if campaign_preferences:
            query = scaler.transform([campaign_preferences])
            nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X)
            distances, indices = nbrs.kneighbors(query)
            recommended = [influencers_data[i] for i in indices[0]]
        else:
            # Default recommendation based on general quality score
            scores = []
            for i, inf in enumerate(influencers_data):
                dp = inf["data_points"][0]
                score = (
                    0.4 * X[i][1] +  # Engagement rate
                    0.3 * (1 - X[i][2]) +  # Inverse of price (lower price = better)
                    0.2 * X[i][0] +  # Followers
                    0.1 * np.mean(X[i][3:])  # Audience match
                )
                scores.append((score, i))
                
            scores.sort(reverse=True)
            recommended = [influencers_data[i] for score, i in scores[:10]]

        # Add AI metrics for display
        for i, inf in enumerate(recommended):
            dp = inf["data_points"][0]
            inf["ai_metrics"] = {
                'score': (0.4 * (float(dp.get("engagement_rate") or 0)) +
                         0.3 * (1 - (dp.get("price_reels_creative") or 0) / 1_000_000) +
                         0.2 * (dp.get("subs") or 0) / 1_000_000),
                'audience_match': cls.calculate_audience_match(dp, campaign_preferences),
                'campaign_match': 0.7,  # Placeholder for campaign fit
                'reason': cls.get_recommendation_reason(inf, i + 1)
            }

        return recommended

    @staticmethod
    def calculate_audience_match(influencer_dp, campaign_prefs):
        """Calculate how well influencer audience matches campaign target"""
        if not campaign_prefs:
            return 0.5  # Neutral score if no preferences
            
        # Calculate match for each demographic factor
        gender_match = min(
            influencer_dp.get('women', 0) / 100,
            campaign_prefs[3]  # Women target
        ) + min(
            influencer_dp.get('men', 0) / 100,
            campaign_prefs[4]  # Men target
        )
        
        age_match = (
            min(influencer_dp.get('age_18_24', 0) / 100, campaign_prefs[5]) +
            min(influencer_dp.get('age_25_34', 0) / 100, campaign_prefs[6]) +
            min(influencer_dp.get('age_35_44', 0) / 100, campaign_prefs[7])
        ) / 3
        
        location_match = (
            min(influencer_dp.get('armenia', 0) / 100, campaign_prefs[8]) +
            min(influencer_dp.get('russia', 0) / 100, campaign_prefs[9]) +
            min(influencer_dp.get('usa', 0) / 100, campaign_prefs[10])
        ) / 3
        
        return (gender_match + age_match + location_match) / 3

    @staticmethod
    def get_recommendation_reason(influencer, rank):
        dp = influencer["data_points"][0]
        reasons = [
            f"Top {rank} for engagement ({(dp.get('engagement_rate') or 0):.2f}%) in {dp.get('category', 'N/A')}",
            f"Great value with {dp.get('subs', 0):,} followers at {dp.get('price_reels_creative', 0):,} AMD",
            f"Strong match with your target audience ({(dp.get('women') or 0):.0f}% female)",
            f"High-performing in {dp.get('category', 'N/A')} with {(dp.get('avg_views_reels') or 0):,} avg views",
            f"Optimal price-performance ratio at {dp.get('price_reels_creative', 0):,} AMD"
        ]
        return reasons[rank % len(reasons)]

class InfluencerDataPoint(db.Model):
    __tablename__ = 'influencer_data_points'
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id', ondelete='CASCADE'), nullable=False)
    social_net = db.Column(db.String(100))
    link = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    price_stories = db.Column(db.Integer)
    story_with_travel_to_location = db.Column(db.Integer)
    price_reels_creative = db.Column(db.Integer)
    price_photo_post = db.Column(db.Integer)
    collaboration = db.Column(db.Boolean)
    youtube_integration = db.Column(db.Integer)
    youtube_dedicated_video = db.Column(db.Integer)

    subs = db.Column(db.Integer)
    avg_views_reels = db.Column(db.Integer)
    cpv_reels_creative = db.Column(db.Numeric(10, 4))
    engagement_rate = db.Column(db.Numeric(5, 2))

    men = db.Column(db.Numeric(5, 2))
    women = db.Column(db.Numeric(5, 2))

    age_13_17 = db.Column(db.Numeric(5, 2))
    age_18_24 = db.Column(db.Numeric(5, 2))
    age_25_34 = db.Column(db.Numeric(5, 2))
    age_35_44 = db.Column(db.Numeric(5, 2))

    armenia = db.Column(db.Numeric(5, 2))
    russia = db.Column(db.Numeric(5, 2))
    usa = db.Column(db.Numeric(5, 2))
    georgia = db.Column(db.Numeric(5, 2))

    yerevan = db.Column(db.Numeric(5, 2))
    gyumri = db.Column(db.Numeric(5, 2))
    vanadzor = db.Column(db.Numeric(5, 2))
    moscow = db.Column(db.Numeric(5, 2))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    website = db.Column(db.String(200))
    social_media = db.Column(db.JSON)  # {'instagram': '@username', 'youtube': 'channel'}
    categories = db.Column(db.JSON)  # ['fashion', 'beauty']
    location = db.Column(db.String(100))
    profile_pic = db.Column(db.String(200))
    stats = db.Column(db.JSON)  # {'followers': 10000, 'engagement': 4.5}
    is_verified = db.Column(db.Boolean, default=False)

class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan = db.Column(db.String(20))  # starter, professional, enterprise
    period = db.Column(db.String(10))  # monthly, yearly
    status = db.Column(db.String(20), default='active')  # active, canceled, expired
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    stripe_subscription_id = db.Column(db.String(100))
    payment_method = db.Column(db.String(50))

class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    brand = db.Column(db.String(100))  
    logo = db.Column(db.String(100), default='default_campaign_logo.jpg')  # Default logo
    
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    budget = db.Column(db.Integer)  # in AMD
    status = db.Column(db.String(20), default='draft')  # draft, active, completed, canceled
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    requirements = db.Column(db.Text)
    target_audience = db.Column(db.JSON)
    influencer_requirements = db.Column(db.JSON)
    collaborations = db.relationship('Collaboration', backref='campaign', lazy=True)

    def get_influencer_preferences(self):
        """Extract influencer matching preferences from campaign data"""
        if not self.influencer_requirements:
            return None
            
        preferences = []
        req = self.influencer_requirements
        
        # Normalize the preferences for the recommendation algorithm
        return [
            req.get('min_followers', 0) / 1000000,  # Normalize to millions
            req.get('min_engagement', 0) / 100,       # Convert % to decimal
            req.get('max_price', 1000000) / 1000000,  # Normalize to millions
            req.get('target_gender_women', 50) / 100, # Convert % to decimal
            req.get('target_gender_men', 50) / 100,   # Convert % to decimal
            req.get('target_age_18_24', 0) / 100,
            req.get('target_age_25_34', 0) / 100,
            req.get('target_age_35_44', 0) / 100,
            req.get('target_location_armenia', 0) / 100,
            req.get('target_location_russia', 0) / 100,
            req.get('target_location_usa', 0) / 100
        ]

class Collaboration(db.Model):
    __tablename__ = 'collaboration'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    offer_amount = db.Column(db.Integer)  # in AMD
    influencer_notes = db.Column(db.Text)
    brand_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deliverables = db.relationship('Deliverable', backref='collaboration', lazy=True)
    payments = db.relationship('Payment', backref='collaboration', lazy=True)

class Deliverable(db.Model):
    __tablename__ = 'deliverable'
    id = db.Column(db.Integer, primary_key=True)
    collaboration_id = db.Column(db.Integer, db.ForeignKey('collaboration.id'))
    type = db.Column(db.String(50))  # instagram_post, youtube_video, etc.
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, submitted, approved, rejected
    submission = db.Column(db.JSON)  # {'url': '...', 'text': '...'}
    submitted_at = db.Column(db.DateTime)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    collaboration_id = db.Column(db.Integer, db.ForeignKey('collaboration.id'))
    amount = db.Column(db.Integer)  # in AMD
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')


# Connect to your PostgreSQL database
engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///linxy.db'))

# Create the table(s)
Base.metadata.create_all(engine)
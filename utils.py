from flask import current_app
from models import User, Profile
import stripe

def create_stripe_customer(user):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    customer = stripe.Customer.create(
        email=user.email,
        name=user.username
    )
    return customer.id

def get_influencer_stats(influencer_id):
    influencer = User.query.get(influencer_id)
    if not influencer or influencer.role != 'influencer':
        return None
    
    profile = Profile.query.filter_by(user_id=influencer_id).first()
    if not profile:
        return None
    
    stats = {
        'followers': profile.stats.get('followers', 0),
        'engagement': profile.stats.get('engagement', 0),
        'completed_campaigns': Collaboration.query.filter_by(
            influencer_id=influencer_id,
            status='completed'
        ).count(),
        'active_campaigns': Collaboration.query.filter_by(
            influencer_id=influencer_id,
            status='accepted'
        ).count()
    }
    
    return stats

def match_influencers_to_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return []
    
    target = campaign.target_audience
    influencers = User.query.filter_by(role='influencer').join(Profile).all()
    
    matched = []
    for influencer in influencers:
        profile = influencer.profile
        if not profile.stats:
            continue
        
        # Simple matching algorithm (can be enhanced)
        score = 0
        
        # Location match
        if target.get('location') and profile.location:
            if target['location'].lower() in profile.location.lower():
                score += 20
        
        # Audience match (simplified)
        if profile.stats.get('audience'):
            if target.get('gender') and profile.stats['audience'].get('gender'):
                if target['gender'] == 'any' or target['gender'] == profile.stats['audience']['gender']:
                    score += 15
            
            if target.get('age_min') and profile.stats['audience'].get('age_avg'):
                if profile.stats['audience']['age_avg'] >= target['age_min']:
                    score += 10
            
            if target.get('age_max') and profile.stats['audience'].get('age_avg'):
                if profile.stats['audience']['age_avg'] <= target['age_max']:
                    score += 10
        
        # Category match
        if profile.categories and campaign.categories:
            common_categories = set(profile.categories) & set(campaign.categories)
            score += len(common_categories) * 5
        
        # Engagement score
        if profile.stats.get('engagement'):
            engagement = float(profile.stats['engagement'].strip('%'))
            score += engagement * 0.5
        
        if score > 30:  # Threshold for matching
            matched.append({
                'influencer': influencer,
                'profile': profile,
                'score': min(100, score)  # Cap at 100
            })
    
    # Sort by score
    matched.sort(key=lambda x: x['score'], reverse=True)
    return matched

def send_notification(user_id, message, link=None):
    # In a real app, this would send an email or push notification
    # For now, we'll just print to console
    user = User.query.get(user_id)
    print(f"Notification to {user.email}: {message}")
    if link:
        print(f"Link: {link}")
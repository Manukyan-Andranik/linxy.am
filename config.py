import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///linxy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Stripe configuration
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    
    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # AWS S3 configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_REGION = os.getenv('S3_REGION')
    
    # Pricing plans
    PRICING_PLANS = {
        'starter': {
            'monthly_price': 20000,  # in AMD
            'yearly_price': 200000,
            'features': [
                'Up to 5 campaigns',
                'Basic influencer search',
                'Standard analytics',
                'Email support'
            ]
        },
        'professional': {
            'monthly_price': 35000,
            'yearly_price': 350000,
            'features': [
                'Up to 20 campaigns',
                'Advanced influencer search',
                'AI matching',
                'Detailed analytics',
                'Priority support'
            ]
        },
        'enterprise': {
            'monthly_price': 150000,
            'yearly_price': 1500000,
            'features': [
                'Unlimited campaigns',
                'Premium influencer search',
                'Advanced AI matching',
                'Custom reporting',
                'Dedicated account manager',
                'API access'
            ]
        }
    }
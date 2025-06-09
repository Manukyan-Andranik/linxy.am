import csv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from typing import List, Dict, Optional, Union

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def recommend_influencers(campaign_preferences=None):
    # Get all influencers from your database
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
    
    # Prepare feature matrix
    features = []
    for inf in all_influencers:
        dp = inf["data_points"][0]  # Assuming one data point per influencer
        features.append([
            dp["subs"] or 0,
            dp["engagement_rate"] or 0,
            dp["price_reels_creative"] or 0,
            dp["men"] or 0,
            dp["women"] or 0,
            dp["age_13_17"] or 0,
            dp["age_18_24"] or 0,
            dp["age_25_34"] or 0,
            dp["age_35_44"] or 0,
            dp["armenia"] or 0,
            dp["russia"] or 0,
            dp["usa"] or 0
        ])
    
    # Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    
    # If we have campaign preferences, use them as query
    if campaign_preferences:
        query = scaler.transform([campaign_preferences])
        nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(query)
        recommended = [all_influencers[i] for i in indices[0]]
    else:
        # Default recommendation based on best overall scores
        scores = []
        for i, inf in enumerate(all_influencers):
            # Score formula (adjust weights as needed)
            score = (0.4 * X[i][1] +  # engagement
                    0.3 * (1 - X[i][2]) +  # inverse of price (lower is better)
                    0.2 * X[i][0] +  # followers
                    0.1 * np.mean(X[i][3:]))  # audience diversity
            
            scores.append((score, i))
        
        # Sort by score and take top 10
        scores.sort(reverse=True)
        recommended = [all_influencers[i] for score, i in scores[:10]]
    
    # Add AI metrics to each recommended influencer
    for i, inf in enumerate(recommended):
        dp = inf["data_points"][0]
        inf["ai_metrics"] = {
            'score': (0.4 * (float(dp["engagement_rate"]) or 0) + 
                     0.3 * (1 - (dp["price_reels_creative"] or 0)/1000000) +
                     0.2 * (dp["subs"] or 0)/1000000),
            'audience_match': 0.8,  # Calculate based on your target audience
            'campaign_match': 0.7,  # Calculate based on past campaigns
            'reason': get_recommendation_reason(inf, i+1)
        }
    
    return recommended

def get_recommendation_reason(influencer, rank):
    dp = influencer["data_points"][0]
    reasons = [
        f"Top {rank} for engagement ({(dp['engagement_rate'] or 0):.2f}%) in {dp['category']}",
        f"Great value with {dp['subs']:,} followers at {dp['price_reels_creative']:,} AMD",
        f"Strong match with your target audience ({(dp['women'] or 0)*100:.0f}% female)",
        f"High-performing in {dp['category']} with {(dp['avg_views_reels'] or 0):,} avg views",
        f"Optimal price-performance ratio at {dp['price_reels_creative']:,} AMD"
    ]
    return reasons[rank % len(reasons)]


class DataManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """
        Initialize the DataManager with database connection parameters.
        
        Args:
            dbname: Database name
            user: Database username
            password: Database password
            host: Database host (default: localhost)
            port: Database port (default: 5432)
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def __enter__(self):
        """Support for context manager protocol (with statement)"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager protocol (with statement)"""
        self.close_connection()

    def connect(self):
        """Establish a database connection"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                cursor_factory=DictCursor
            )
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def close_connection(self):
        """Close the database connection if it exists"""
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def get_influencer_by_name(self, full_name: str, exact_match: bool = False, 
                             case_sensitive: bool = False) -> Optional[Union[Dict, List[Dict]]]:
        """
        Fetch influencer(s) by name
        
        Args:
            full_name: Name to search for
            exact_match: Whether to search for exact match
            case_sensitive: Whether the search should be case sensitive
            
        Returns:
            Single dict for exact match, list of dicts for partial match, or None if not found
        """
        try:
            with self.conn.cursor() as cur:
                if exact_match:
                    if case_sensitive:
                        query = "SELECT * FROM influencers WHERE full_name = %s"
                    else:
                        query = "SELECT * FROM influencers WHERE full_name ILIKE %s"
                    params = (full_name,)
                else:
                    if case_sensitive:
                        query = "SELECT * FROM influencers WHERE full_name LIKE %s"
                    else:
                        query = "SELECT * FROM influencers WHERE full_name ILIKE %s"
                    params = (f"%{full_name}%",)
                
                cur.execute(query, params)
                
                if exact_match:
                    result = cur.fetchone()
                    return dict(result) if result else None
                else:
                    results = cur.fetchall()
                    return [dict(row) for row in results] if results else None
                    
        except Exception as e:
            print(f"Error fetching influencer: {e}")
            return None

    def get_all_influencers(self, limit: int = None) -> List[Dict]:
        """
        Fetch all influencers with optional limit
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of influencer dictionaries
        """
        try:
            with self.conn.cursor() as cur:
                query = "SELECT * FROM influencers"
                if limit:
                    query += f" LIMIT {limit}"
                cur.execute(query)
                results = cur.fetchall()
                return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"Error fetching all influencers: {e}")
            return []


    def get_influencer_data_points(self, influencer_id: int) -> Optional[List[Dict]]:
        """
        Fetch all data points for a specific influencer.

        Args:
            influencer_id: ID of the influencer

        Returns:
            List of dictionaries containing data points, or None if not found
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM influencer_data_points WHERE influencer_id = %s", (influencer_id,))
                rows = cur.fetchall()
                if not rows:
                    return None

                # Get column names
                colnames = [desc[0] for desc in cur.description]

                # Convert each row to a dictionary
                data_points = [dict(zip(colnames, row)) for row in rows]

                return data_points

        except Exception as e:
            print(f"Error fetching data points: {e}")
            return None

    def update_influencer(self, influencer_id: int, update_data: Dict) -> bool:
        """
        Update influencer data
        
        Args:
            influencer_id: ID of the influencer to update
            update_data: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.conn.cursor() as cur:
                set_clauses = []
                values = []
                for key, value in update_data.items():
                    set_clauses.append(sql.Identifier(key))
                    values.append(value)
                values.append(influencer_id)
                
                update_query = sql.SQL("UPDATE influencers SET {} = %s WHERE id = %s").format(
                    sql.SQL(', ').join(set_clauses))
                
                cur.execute(update_query, values)
                self.conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating influencer: {e}")
            self.conn.rollback()
            return False

    def delete_influencer(self, influencer_id: int) -> bool:
        """
        Delete an influencer by ID
        
        Args:
            influencer_id: ID of the influencer to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM influencers WHERE id = %s", (influencer_id,))
                self.conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting influencer: {e}")
            self.conn.rollback()
            return False

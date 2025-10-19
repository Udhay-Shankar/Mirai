"""
Data processing module for social listening data.
Computes metrics, identifies trends, and processes raw API data.
"""
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import re
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes and analyzes social listening data."""
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Text to extract hashtags from
            
        Returns:
            List of hashtags (without # symbol)
        """
        if not text:
            return []
        return re.findall(r'#(\w+)', text.lower())
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """
        Extract @mentions from text.
        
        Args:
            text: Text to extract mentions from
            
        Returns:
            List of mentions (without @ symbol)
        """
        if not text:
            return []
        return re.findall(r'@(\w+)', text.lower())
    
    @staticmethod
    def calculate_engagement_rate(mention: Dict) -> float:
        """
        Calculate engagement rate for a mention.
        
        Args:
            mention: Mention data dictionary
            
        Returns:
            Engagement rate as percentage
        """
        followers = mention.get('author_followers', 0)
        if followers == 0:
            return 0.0
        
        likes = mention.get('likes', 0)
        comments = mention.get('comments', 0)
        shares = mention.get('shares', 0)
        
        total_engagement = likes + comments + shares
        return (total_engagement / followers) * 100 if followers > 0 else 0.0
    
    def process_mentions(self, mentions: List[Dict]) -> Dict[str, Any]:
        """
        Process raw mentions data and compute basic metrics.
        
        Args:
            mentions: List of mention dictionaries
            
        Returns:
            Processed metrics dictionary
        """
        if not mentions:
            return {
                "total_mentions": 0,
                "unique_authors": 0,
                "total_reach": 0,
                "average_sentiment": 0,
                "sentiment_breakdown": {"positive": 0, "negative": 0, "neutral": 0},
                "top_hashtags": [],
                "top_mentions": [],
                "sources": {},
                "languages": {}
            }
        
        # Basic counts
        total_mentions = len(mentions)
        unique_authors = len(set(m.get('author_id') for m in mentions if m.get('author_id')))
        
        # Reach calculation
        total_reach = sum(m.get('author_followers', 0) for m in mentions)
        
        # Sentiment analysis
        sentiment_counts = Counter(m.get('sentiment', 'neutral') for m in mentions)
        sentiment_breakdown = {
            "positive": sentiment_counts.get('positive', 0),
            "negative": sentiment_counts.get('negative', 0),
            "neutral": sentiment_counts.get('neutral', 0)
        }
        
        # Average sentiment score
        sentiment_scores = {
            'positive': 1,
            'neutral': 0,
            'negative': -1
        }
        total_score = sum(
            sentiment_scores.get(m.get('sentiment', 'neutral'), 0)
            for m in mentions
        )
        average_sentiment = total_score / total_mentions if total_mentions > 0 else 0
        
        # Extract hashtags and mentions
        all_hashtags = []
        all_user_mentions = []
        
        for mention in mentions:
            text = mention.get('text', '')
            all_hashtags.extend(self.extract_hashtags(text))
            all_user_mentions.extend(self.extract_mentions(text))
        
        # Top hashtags
        hashtag_counter = Counter(all_hashtags)
        top_hashtags = [
            {"tag": tag, "count": count}
            for tag, count in hashtag_counter.most_common(20)
        ]
        
        # Top user mentions
        mention_counter = Counter(all_user_mentions)
        top_mentions = [
            {"username": user, "count": count}
            for user, count in mention_counter.most_common(20)
        ]
        
        # Source breakdown
        source_counts = Counter(m.get('source', 'unknown') for m in mentions)
        sources = dict(source_counts)
        
        # Language breakdown
        language_counts = Counter(m.get('language', 'unknown') for m in mentions)
        languages = dict(language_counts)
        
        return {
            "total_mentions": total_mentions,
            "unique_authors": unique_authors,
            "total_reach": total_reach,
            "average_sentiment": round(average_sentiment, 2),
            "sentiment_breakdown": sentiment_breakdown,
            "top_hashtags": top_hashtags,
            "top_mentions": top_mentions,
            "sources": sources,
            "languages": languages
        }
    
    def identify_influencers(
        self,
        mentions: List[Dict],
        min_followers: int = 1000,
        min_engagement: float = 0.1
    ) -> List[Dict]:
        """
        Identify influential accounts from mentions.
        
        Args:
            mentions: List of mention dictionaries
            keyword: Keyword being tracked
            min_followers: Minimum follower count
            min_engagement: Minimum engagement rate
            
        Returns:
            List of influencer profiles
        """
        # Group mentions by author
        author_data = defaultdict(lambda: {
            'mention_count': 0,
            'total_reach': 0,
            'total_engagement': 0,
            'mentions': []
        })
        
        for mention in mentions:
            author_id = mention.get('author_id')
            if not author_id:
                continue
            
            author_data[author_id]['mention_count'] += 1
            author_data[author_id]['mentions'].append(mention)
            author_data[author_id]['total_reach'] += mention.get('author_followers', 0)
            
            # Calculate engagement
            likes = mention.get('likes', 0)
            comments = mention.get('comments', 0)
            shares = mention.get('shares', 0)
            author_data[author_id]['total_engagement'] += likes + comments + shares
        
        # Build influencer list
        influencers = []
        
        for author_id, data in author_data.items():
            # Get author info from first mention
            first_mention = data['mentions'][0]
            followers = first_mention.get('author_followers', 0)
            
            if followers < min_followers:
                continue
            
            # Calculate average engagement rate
            avg_engagement_rate = self.calculate_engagement_rate(first_mention)
            
            if avg_engagement_rate < min_engagement:
                continue
            
            influencers.append({
                'author_id': author_id,
                'author_name': first_mention.get('author_name', 'Unknown'),
                'author_username': first_mention.get('author_username', ''),
                'followers': followers,
                'mention_count': data['mention_count'],
                'total_engagement': data['total_engagement'],
                'avg_engagement_rate': round(avg_engagement_rate, 2),
                'profile_url': first_mention.get('author_url', ''),
                'profile_image': first_mention.get('author_image', ''),
                'verified': first_mention.get('author_verified', False)
            })
        
        # Sort by followers
        influencers.sort(key=lambda x: x['followers'], reverse=True)
        
        return influencers
    
    def calculate_trends(
        self,
        mentions: List[Dict],
        time_buckets: str = 'daily'
    ) -> List[Dict]:
        """
        Calculate mention trends over time.
        
        Args:
            mentions: List of mention dictionaries
            time_buckets: Time bucket size ('hourly', 'daily', 'weekly')
            
        Returns:
            List of time series data points
        """
        if not mentions:
            return []
        
        # Group mentions by time bucket
        time_groups = defaultdict(lambda: {
            'count': 0,
            'reach': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0
        })
        
        for mention in mentions:
            created_at = mention.get('created_at')
            if not created_at:
                continue
            
            # Parse date
            if isinstance(created_at, str):
                try:
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            else:
                date_obj = created_at
            
            # Determine bucket
            if time_buckets == 'hourly':
                bucket = date_obj.replace(minute=0, second=0, microsecond=0)
            elif time_buckets == 'daily':
                bucket = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            else:  # weekly
                days_since_monday = date_obj.weekday()
                bucket = (date_obj - timedelta(days=days_since_monday)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            
            bucket_key = bucket.isoformat()
            
            # Update counts
            time_groups[bucket_key]['count'] += 1
            time_groups[bucket_key]['reach'] += mention.get('author_followers', 0)
            
            sentiment = mention.get('sentiment', 'neutral')
            time_groups[bucket_key][sentiment] += 1
        
        # Convert to list and sort
        trends = [
            {
                'timestamp': timestamp,
                'count': data['count'],
                'reach': data['reach'],
                'sentiment': {
                    'positive': data['positive'],
                    'negative': data['negative'],
                    'neutral': data['neutral']
                }
            }
            for timestamp, data in time_groups.items()
        ]
        
        trends.sort(key=lambda x: x['timestamp'])
        
        return trends
    
    def find_similar_creators(
        self,
        mentions: List[Dict],
        target_keyword: str,
        min_co_occurrence: int = 3
    ) -> List[Dict]:
        """
        Find similar or rising content creators based on co-occurrence.
        
        Args:
            mentions: List of mention dictionaries
            target_keyword: Primary keyword being tracked
            min_co_occurrence: Minimum co-occurrences to consider
            
        Returns:
            List of similar creators
        """
        # Track which authors mention which topics together
        author_topics = defaultdict(Counter)
        author_info = {}
        
        for mention in mentions:
            author_id = mention.get('author_id')
            if not author_id:
                continue
            
            # Store author info
            if author_id not in author_info:
                author_info[author_id] = {
                    'name': mention.get('author_name', 'Unknown'),
                    'username': mention.get('author_username', ''),
                    'followers': mention.get('author_followers', 0),
                    'mention_count': 0
                }
            
            author_info[author_id]['mention_count'] += 1
            
            # Extract topics from text
            text = mention.get('text', '').lower()
            hashtags = self.extract_hashtags(text)
            
            for tag in hashtags:
                if tag != target_keyword.lower():
                    author_topics[author_id][tag] += 1
        
        # Find creators with overlapping topics
        similar_creators = []
        
        for author_id, topics in author_topics.items():
            # Find most common co-occurring topics
            common_topics = topics.most_common(5)
            
            if not common_topics or common_topics[0][1] < min_co_occurrence:
                continue
            
            info = author_info[author_id]
            
            similar_creators.append({
                'author_id': author_id,
                'author_name': info['name'],
                'author_username': info['username'],
                'followers': info['followers'],
                'mention_count': info['mention_count'],
                'common_topics': [
                    {'topic': topic, 'count': count}
                    for topic, count in common_topics
                ]
            })
        
        # Sort by followers
        similar_creators.sort(key=lambda x: x['followers'], reverse=True)
        
        return similar_creators
    
    def detect_rising_creators(
        self,
        mentions: List[Dict],
        lookback_days: int = 30
    ) -> List[Dict]:
        """
        Detect accounts with rapidly increasing mention activity.
        
        Args:
            mentions: List of mention dictionaries
            lookback_days: Days to look back for trend analysis
            
        Returns:
            List of rising creators
        """
        cutoff_date = datetime.now() - timedelta(days=lookback_days)
        midpoint_date = datetime.now() - timedelta(days=lookback_days // 2)
        
        # Split mentions into two periods
        early_period = defaultdict(int)
        recent_period = defaultdict(int)
        author_info = {}
        
        for mention in mentions:
            author_id = mention.get('author_id')
            if not author_id:
                continue
            
            created_at = mention.get('created_at')
            if isinstance(created_at, str):
                try:
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            else:
                date_obj = created_at
            
            # Store author info
            if author_id not in author_info:
                author_info[author_id] = {
                    'name': mention.get('author_name', 'Unknown'),
                    'username': mention.get('author_username', ''),
                    'followers': mention.get('author_followers', 0)
                }
            
            # Count mentions in each period
            if cutoff_date <= date_obj < midpoint_date:
                early_period[author_id] += 1
            elif date_obj >= midpoint_date:
                recent_period[author_id] += 1
        
        # Calculate growth rates
        rising_creators = []
        
        for author_id, recent_count in recent_period.items():
            early_count = early_period.get(author_id, 0)
            
            # Skip if no baseline
            if early_count == 0:
                if recent_count >= 3:  # New but active
                    growth_rate = float('inf')
                else:
                    continue
            else:
                growth_rate = ((recent_count - early_count) / early_count) * 100
            
            # Only include if significant growth
            if growth_rate > 50 or growth_rate == float('inf'):
                info = author_info[author_id]
                
                rising_creators.append({
                    'author_id': author_id,
                    'author_name': info['name'],
                    'author_username': info['username'],
                    'followers': info['followers'],
                    'early_mentions': early_count,
                    'recent_mentions': recent_count,
                    'growth_rate': round(growth_rate, 1) if growth_rate != float('inf') else 'New',
                    'is_new': early_count == 0
                })
        
        # Sort by growth rate
        rising_creators.sort(
            key=lambda x: x['recent_mentions'] if x['is_new'] else x['growth_rate'],
            reverse=True
        )
        
        return rising_creators


# Global processor instance
data_processor = DataProcessor()

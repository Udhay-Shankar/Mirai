"""
Metrics calculation module for advanced analytics.
"""
from typing import Dict, List, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculate advanced metrics for social listening data."""
    
    @staticmethod
    def calculate_engagement_metrics(mentions: List[Dict]) -> Dict[str, Any]:
        """
        Calculate detailed engagement metrics.
        
        Args:
            mentions: List of mention dictionaries
            
        Returns:
            Engagement metrics dictionary
        """
        if not mentions:
            return {
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0,
                "total_engagement": 0,
                "avg_engagement_per_mention": 0,
                "engagement_rate": 0
            }
        
        total_likes = sum(m.get('likes', 0) for m in mentions)
        total_comments = sum(m.get('comments', 0) for m in mentions)
        total_shares = sum(m.get('shares', 0) for m in mentions)
        total_engagement = total_likes + total_comments + total_shares
        
        total_reach = sum(m.get('author_followers', 0) for m in mentions)
        engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0
        
        return {
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_engagement": total_engagement,
            "avg_engagement_per_mention": round(total_engagement / len(mentions), 2),
            "engagement_rate": round(engagement_rate, 2)
        }
    
    @staticmethod
    def calculate_viral_score(mention: Dict) -> float:
        """
        Calculate virality score for a mention.
        
        Args:
            mention: Mention dictionary
            
        Returns:
            Viral score (0-100)
        """
        followers = mention.get('author_followers', 0)
        likes = mention.get('likes', 0)
        comments = mention.get('comments', 0)
        shares = mention.get('shares', 0)
        
        # Weighted engagement score
        engagement_score = likes + (comments * 2) + (shares * 3)
        
        # Virality = engagement relative to followers
        if followers == 0:
            return 0
        
        viral_score = min((engagement_score / followers) * 1000, 100)
        return round(viral_score, 2)
    
    @staticmethod
    def get_top_posts(mentions: List[Dict], limit: int = 10) -> List[Dict]:
        """
        Get top performing posts by engagement.
        
        Args:
            mentions: List of mention dictionaries
            limit: Number of top posts to return
            
        Returns:
            List of top posts with metrics
        """
        calculator = MetricsCalculator()
        
        # Calculate viral score for each mention
        posts_with_scores = []
        
        for mention in mentions:
            viral_score = calculator.calculate_viral_score(mention)
            total_engagement = (
                mention.get('likes', 0) +
                mention.get('comments', 0) +
                mention.get('shares', 0)
            )
            
            posts_with_scores.append({
                'id': mention.get('id'),
                'text': mention.get('text', '')[:200],  # Truncate
                'author': mention.get('author_name', 'Unknown'),
                'author_followers': mention.get('author_followers', 0),
                'likes': mention.get('likes', 0),
                'comments': mention.get('comments', 0),
                'shares': mention.get('shares', 0),
                'total_engagement': total_engagement,
                'viral_score': viral_score,
                'source': mention.get('source', 'unknown'),
                'url': mention.get('url', ''),
                'created_at': mention.get('created_at')
            })
        
        # Sort by viral score
        posts_with_scores.sort(key=lambda x: x['viral_score'], reverse=True)
        
        return posts_with_scores[:limit]
    
    @staticmethod
    def calculate_demographic_breakdown(mentions: List[Dict]) -> Dict[str, Any]:
        """
        Calculate demographic breakdown from mentions.
        
        Args:
            mentions: List of mention dictionaries
            
        Returns:
            Demographic data
        """
        gender_counts = defaultdict(int)
        age_groups = defaultdict(int)
        location_counts = defaultdict(int)
        
        for mention in mentions:
            # Gender
            gender = mention.get('author_gender', 'unknown')
            gender_counts[gender] += 1
            
            # Age group
            age = mention.get('author_age')
            if age:
                if age < 18:
                    age_group = 'under_18'
                elif age < 25:
                    age_group = '18-24'
                elif age < 35:
                    age_group = '25-34'
                elif age < 45:
                    age_group = '35-44'
                elif age < 55:
                    age_group = '45-54'
                else:
                    age_group = '55+'
                age_groups[age_group] += 1
            
            # Location
            location = mention.get('author_location', 'unknown')
            if location and location != 'unknown':
                location_counts[location] += 1
        
        # Convert to percentages
        total = len(mentions)
        
        return {
            "gender": {
                gender: round((count / total) * 100, 1)
                for gender, count in gender_counts.items()
            },
            "age_groups": {
                group: round((count / total) * 100, 1)
                for group, count in age_groups.items()
            },
            "top_locations": dict(
                sorted(
                    location_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            )
        }
    
    @staticmethod
    def compare_competitors(
        primary_mentions: List[Dict],
        competitor_mentions: Dict[str, List[Dict]]
    ) -> Dict[str, Any]:
        """
        Compare primary keyword against competitors.
        
        Args:
            primary_mentions: Mentions for primary keyword
            competitor_mentions: Dict of competitor names to their mentions
            
        Returns:
            Comparison data
        """
        from app.analytics.processor import data_processor
        
        # Process primary keyword
        primary_metrics = data_processor.process_mentions(primary_mentions)
        primary_metrics['keyword'] = 'Primary'
        
        # Process competitors
        competitor_metrics = []
        
        for competitor_name, mentions in competitor_mentions.items():
            metrics = data_processor.process_mentions(mentions)
            metrics['keyword'] = competitor_name
            competitor_metrics.append(metrics)
        
        # Calculate share of voice
        all_mentions = [primary_metrics] + competitor_metrics
        total_mentions = sum(m['total_mentions'] for m in all_mentions)
        
        for metrics in all_mentions:
            metrics['share_of_voice'] = round(
                (metrics['total_mentions'] / total_mentions * 100) if total_mentions > 0 else 0,
                1
            )
        
        return {
            "primary": primary_metrics,
            "competitors": competitor_metrics,
            "summary": {
                "total_tracked_mentions": total_mentions,
                "primary_rank": sorted(
                    all_mentions,
                    key=lambda x: x['total_mentions'],
                    reverse=True
                ).index(primary_metrics) + 1
            }
        }


# Global metrics calculator instance
metrics_calculator = MetricsCalculator()

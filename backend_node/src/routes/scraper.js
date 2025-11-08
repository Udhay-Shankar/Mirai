import express from 'express';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import Mention from '../models/Mention.js';
import { authMiddleware } from '../middleware/auth.js';

const router = express.Router();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// POST /api/scrape/search - Trigger scraping for a keyword
router.post('/search', authMiddleware, async (req, res) => {
  try {
    const { keyword } = req.body;
    
    if (!keyword) {
      return res.status(400).json({ error: 'Keyword is required' });
    }
    
    // Path to Python scraper - USING SCRAPE.DO FOR UNLIMITED SCRAPING!
    const scraperPath = path.resolve(__dirname, '../../../scrapers/main_scraper_scrape_do.py');
    
    // Spawn Python process with UNLIMITED scraping (pass no limit for truly unlimited)
    const python = spawn('python', [scraperPath, keyword]);
    
    let dataString = '';
    let errorString = '';
    
    python.stdout.on('data', (data) => {
      dataString += data.toString();
      console.log(`Python: ${data}`);
    });
    
    python.stderr.on('data', (data) => {
      errorString += data.toString();
      console.error(`Python Error: ${data}`);
    });
    
    python.on('close', async (code) => {
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`);
        console.error(errorString);
        if (!res.headersSent) {
          return res.status(500).json({ 
            error: 'Scraping failed', 
            details: errorString 
          });
        }
      }
      
      // Get results from MongoDB (increased to 1000 for UNLIMITED data)
      const mentions = await Mention.find({ keyword }).sort({ timestamp: -1 }).limit(1000);
      
      // Calculate analytics - NOW INCLUDING INSTAGRAM, FACEBOOK, BLOGS!
      const analytics = {
        total_mentions: mentions.length,
        by_platform: {
          twitter: mentions.filter(m => m.platform === 'twitter').length,
          reddit: mentions.filter(m => m.platform === 'reddit').length,
          youtube: mentions.filter(m => m.platform === 'youtube').length,
          instagram: mentions.filter(m => m.platform === 'instagram').length,
          facebook: mentions.filter(m => m.platform === 'facebook').length,
          medium: mentions.filter(m => m.platform === 'medium').length,
          blog: mentions.filter(m => m.platform === 'blog').length,
          substack: mentions.filter(m => m.platform === 'substack').length
        },
        sentiment: {
          positive: mentions.filter(m => m.sentiment === 'positive').length,
          negative: mentions.filter(m => m.sentiment === 'negative').length,
          neutral: mentions.filter(m => m.sentiment === 'neutral').length
        },
        total_reach: mentions.reduce((sum, m) => sum + (m.reach || 0), 0),
        total_engagement: mentions.reduce((sum, m) => sum + (m.engagement || 0), 0)
      };
      
      if (!res.headersSent) {
        return res.status(200).json({
          message: 'Scraping completed successfully',
          keyword,
          analytics,
          mentions: mentions.slice(0, 20) // Return top 20
        });
      }
    });
    
  } catch (error) {
    console.error('Scrape error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scrape/mentions/:keyword - Get mentions for a keyword with advanced analytics
router.get('/mentions/:keyword', authMiddleware, async (req, res) => {
  try {
    const { keyword } = req.params;
    const { platform, sentiment, limit = 100, skip = 0, source_quality } = req.query;
    
    // Build query
    const query = { keyword };
    if (platform) query.platform = platform;
    if (sentiment) query.sentiment = sentiment;
    if (source_quality) query.source_quality = source_quality;
    
    // Get mentions
    const mentions = await Mention.find(query)
      .sort({ timestamp: -1 })
      .limit(parseInt(limit))
      .skip(parseInt(skip));
    
    // Get all mentions for analytics (not limited)
    const all_mentions = await Mention.find({ keyword });
    
    // Advanced Analytics - Awario style
    const analytics = {
      total_mentions: all_mentions.length,
      
      // Platform breakdown - ALL PLATFORMS!
      by_platform: {
        twitter: all_mentions.filter(m => m.platform === 'twitter').length,
        reddit: all_mentions.filter(m => m.platform === 'reddit').length,
        youtube: all_mentions.filter(m => m.platform === 'youtube').length,
        instagram: all_mentions.filter(m => m.platform === 'instagram').length,
        facebook: all_mentions.filter(m => m.platform === 'facebook').length,
        medium: all_mentions.filter(m => m.platform === 'medium').length,
        blog: all_mentions.filter(m => m.platform === 'blog').length,
        substack: all_mentions.filter(m => m.platform === 'substack').length
      },
      
      // Sentiment breakdown
      sentiment: {
        positive: all_mentions.filter(m => m.sentiment === 'positive').length,
        negative: all_mentions.filter(m => m.sentiment === 'negative').length,
        neutral: all_mentions.filter(m => m.sentiment === 'neutral').length
      },
      
      // Total reach and engagement
      total_reach: all_mentions.reduce((sum, m) => sum + (m.reach || 0), 0),
      total_engagement: all_mentions.reduce((sum, m) => sum + (m.engagement || 0), 0),
      avg_engagement: all_mentions.length > 0 
        ? Math.round(all_mentions.reduce((sum, m) => sum + (m.engagement || 0), 0) / all_mentions.length)
        : 0,
      
      // Source quality breakdown
      by_quality: {
        high: all_mentions.filter(m => m.source_quality === 'high').length,
        medium: all_mentions.filter(m => m.source_quality === 'medium').length,
        low: all_mentions.filter(m => m.source_quality === 'low').length
      },
      
      // Top authors/influencers
      top_authors: getTopAuthors(all_mentions, 10),
      
      // Top hashtags (from Twitter)
      top_hashtags: getTopHashtags(all_mentions, 10),
      
      // Top subreddits (from Reddit)
      top_subreddits: getTopSubreddits(all_mentions, 10),
      
      // Geographic data
      top_locations: getTopLocations(all_mentions, 10),
      
      // Verified vs non-verified ratio
      verified_ratio: {
        verified: all_mentions.filter(m => m.author_verified).length,
        not_verified: all_mentions.filter(m => !m.author_verified).length
      },
      
      // Engagement metrics
      total_likes: all_mentions.reduce((sum, m) => sum + (m.likes || 0), 0),
      total_comments: all_mentions.reduce((sum, m) => sum + (m.comments || 0), 0),
      total_retweets: all_mentions.reduce((sum, m) => sum + (m.retweets || 0), 0),
      total_views: all_mentions.reduce((sum, m) => sum + (m.views || 0), 0),
      
      // Time series data (last 7 days)
      timeline: getTimeline(all_mentions),
      
      // Influence score statistics
      avg_influence_score: all_mentions.length > 0
        ? Math.round(all_mentions.reduce((sum, m) => sum + (m.influence_score || 0), 0) / all_mentions.length)
        : 0,
      
      // Most influential mentions
      top_influential: all_mentions
        .sort((a, b) => (b.influence_score || 0) - (a.influence_score || 0))
        .slice(0, 5)
        .map(m => ({
          platform: m.platform,
          author: m.author,
          text: m.text.substring(0, 100),
          influence_score: m.influence_score,
          reach: m.reach,
          url: m.url
        }))
    };
    
    return res.status(200).json({
      keyword,
      analytics,
      mentions,
      pagination: {
        limit: parseInt(limit),
        skip: parseInt(skip),
        total: all_mentions.length
      }
    });
    
  } catch (error) {
    console.error('Get mentions error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Helper function to get top authors
function getTopAuthors(mentions, limit) {
  const authorMap = {};
  
  mentions.forEach(m => {
    if (!m.author || m.author === 'Unknown') return;
    
    if (!authorMap[m.author]) {
      authorMap[m.author] = {
        author: m.author,
        author_name: m.author_name,
        followers: m.author_followers || 0,
        verified: m.author_verified || false,
        mention_count: 0,
        total_engagement: 0,
        total_reach: 0,
        platforms: new Set(),
        avg_influence: 0
      };
    }
    authorMap[m.author].mention_count++;
    authorMap[m.author].total_engagement += m.engagement || 0;
    authorMap[m.author].total_reach += m.reach || 0;
    authorMap[m.author].platforms.add(m.platform);
    authorMap[m.author].avg_influence += m.influence_score || 0;
  });
  
  return Object.values(authorMap)
    .map(a => ({
      ...a,
      platforms: Array.from(a.platforms),
      avg_influence: Math.round(a.avg_influence / a.mention_count)
    }))
    .sort((a, b) => b.total_engagement - a.total_engagement)
    .slice(0, limit);
}

// Helper function to get top hashtags
function getTopHashtags(mentions, limit) {
  const hashtagCount = {};
  
  mentions.forEach(m => {
    if (m.hashtags && Array.isArray(m.hashtags)) {
      m.hashtags.forEach(tag => {
        hashtagCount[tag] = (hashtagCount[tag] || 0) + 1;
      });
    }
  });
  
  return Object.entries(hashtagCount)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

// Helper function to get top subreddits
function getTopSubreddits(mentions, limit) {
  const subredditCount = {};
  
  mentions.forEach(m => {
    if (m.subreddit && m.subreddit !== 'Unknown') {
      if (!subredditCount[m.subreddit]) {
        subredditCount[m.subreddit] = {
          name: m.subreddit,
          count: 0,
          total_engagement: 0,
          subscribers: m.subreddit_subscribers || 0
        };
      }
      subredditCount[m.subreddit].count++;
      subredditCount[m.subreddit].total_engagement += m.engagement || 0;
    }
  });
  
  return Object.values(subredditCount)
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

// Helper function to get top locations
function getTopLocations(mentions, limit) {
  const locationCount = {};
  
  mentions.forEach(m => {
    if (m.location && m.location.trim() !== '') {
      locationCount[m.location] = (locationCount[m.location] || 0) + 1;
    }
  });
  
  return Object.entries(locationCount)
    .map(([location, count]) => ({ location, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, limit);
}

// Helper function to get timeline data
function getTimeline(mentions) {
  const timeline = {};
  
  mentions.forEach(m => {
    if (!m.timestamp) return;
    
    const date = new Date(m.timestamp).toISOString().split('T')[0];
    if (!timeline[date]) {
      timeline[date] = {
        date,
        count: 0,
        positive: 0,
        negative: 0,
        neutral: 0,
        engagement: 0,
        reach: 0
      };
    }
    timeline[date].count++;
    timeline[date][m.sentiment || 'neutral']++;
    timeline[date].engagement += m.engagement || 0;
    timeline[date].reach += m.reach || 0;
  });
  
  return Object.values(timeline).sort((a, b) => a.date.localeCompare(b.date));
}

export default router;

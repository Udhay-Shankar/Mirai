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
    
    // Path to Python scraper
    const scraperPath = path.resolve(__dirname, '../../../scrapers/main_scraper.py');
    
    // Spawn Python process
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
        return res.status(500).json({ 
          error: 'Scraping failed', 
          details: errorString 
        });
      }
      
      // Get results from MongoDB
      const mentions = await Mention.find({ keyword }).sort({ timestamp: -1 }).limit(100);
      
      // Calculate analytics
      const analytics = {
        total_mentions: mentions.length,
        by_platform: {
          twitter: mentions.filter(m => m.platform === 'twitter').length,
          reddit: mentions.filter(m => m.platform === 'reddit').length,
          youtube: mentions.filter(m => m.platform === 'youtube').length
        },
        sentiment: {
          positive: mentions.filter(m => m.sentiment === 'positive').length,
          negative: mentions.filter(m => m.sentiment === 'negative').length,
          neutral: mentions.filter(m => m.sentiment === 'neutral').length
        },
        total_reach: mentions.reduce((sum, m) => sum + (m.reach || 0), 0),
        total_engagement: mentions.reduce((sum, m) => sum + (m.engagement || 0), 0)
      };
      
      return res.status(200).json({
        message: 'Scraping completed successfully',
        keyword,
        analytics,
        mentions: mentions.slice(0, 20) // Return top 20
      });
    });
    
    // Return immediately with status
    return res.status(202).json({ 
      message: 'Scraping started', 
      keyword,
      status: 'processing'
    });
    
  } catch (error) {
    console.error('Scrape error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scrape/mentions/:keyword - Get mentions for a keyword
router.get('/mentions/:keyword', authMiddleware, async (req, res) => {
  try {
    const { keyword } = req.params;
    const { platform, sentiment, limit = 100, skip = 0 } = req.query;
    
    // Build query
    const query = { keyword };
    if (platform) query.platform = platform;
    if (sentiment) query.sentiment = sentiment;
    
    // Get mentions
    const mentions = await Mention.find(query)
      .sort({ timestamp: -1 })
      .limit(parseInt(limit))
      .skip(parseInt(skip));
    
    // Get analytics
    const all_mentions = await Mention.find({ keyword });
    const analytics = {
      total_mentions: all_mentions.length,
      by_platform: {
        twitter: all_mentions.filter(m => m.platform === 'twitter').length,
        reddit: all_mentions.filter(m => m.platform === 'reddit').length,
        youtube: all_mentions.filter(m => m.platform === 'youtube').length
      },
      sentiment: {
        positive: all_mentions.filter(m => m.sentiment === 'positive').length,
        negative: all_mentions.filter(m => m.sentiment === 'negative').length,
        neutral: all_mentions.filter(m => m.sentiment === 'neutral').length
      },
      total_reach: all_mentions.reduce((sum, m) => sum + (m.reach || 0), 0),
      total_engagement: all_mentions.reduce((sum, m) => sum + (m.engagement || 0), 0),
      top_authors: getTopAuthors(all_mentions, 5)
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
    if (!authorMap[m.author]) {
      authorMap[m.author] = {
        author: m.author,
        author_name: m.author_name,
        followers: m.author_followers,
        mention_count: 0,
        total_engagement: 0
      };
    }
    authorMap[m.author].mention_count++;
    authorMap[m.author].total_engagement += m.engagement || 0;
  });
  
  return Object.values(authorMap)
    .sort((a, b) => b.total_engagement - a.total_engagement)
    .slice(0, limit);
}

export default router;

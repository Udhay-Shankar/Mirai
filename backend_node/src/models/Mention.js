import mongoose from 'mongoose';

const { Schema, model } = mongoose;

const mentionSchema = new Schema({
  // Core fields
  keyword: { type: String, required: true, index: true },
  platform: { type: String, required: true, enum: ['twitter', 'reddit', 'youtube', 'news'] },
  text: { type: String, required: true },
  full_text: { type: String },
  url: { type: String, unique: true },
  timestamp: { type: Date },
  scraped_at: { type: Date, default: () => new Date() },
  
  // Author information
  author: { type: String },
  author_name: { type: String },
  author_followers: { type: Number, default: 0 },
  author_verified: { type: Boolean, default: false },
  author_bio: { type: String },
  
  // Sentiment analysis
  sentiment: { type: String, enum: ['positive', 'negative', 'neutral'] },
  sentiment_score: { type: Number },
  
  // Engagement metrics
  likes: { type: Number, default: 0 },
  retweets: { type: Number, default: 0 },
  replies: { type: Number, default: 0 },
  comments: { type: Number, default: 0 },
  views: { type: Number, default: 0 },
  engagement: { type: Number, default: 0 },
  reach: { type: Number, default: 0 },
  engagement_rate: { type: Number, default: 0 },
  
  // Quality and influence metrics
  influence_score: { type: Number, default: 0 },
  source_quality: { type: String, enum: ['low', 'medium', 'high'], default: 'medium' },
  
  // Platform-specific fields
  language: { type: String },
  location: { type: String },
  
  // Twitter-specific
  hashtags: [{ type: String }],
  mentions: [{ type: String }],
  
  // Reddit-specific
  subreddit: { type: String },
  subreddit_subscribers: { type: Number },
  awards: { type: Number, default: 0 },
  upvote_ratio: { type: Number },
  domain: { type: String },
  is_video: { type: Boolean, default: false },
  
  // YouTube-specific
  channel_id: { type: String },
  channel_subscribers: { type: Number },
  tags: [{ type: String }],
  duration: { type: String },
  thumbnail: { type: String },
  
  // Content metadata
  content_type: { type: String } // tweet, retweet, post, video, comment, etc.
});

// Indexes for faster queries
mentionSchema.index({ keyword: 1, platform: 1 });
mentionSchema.index({ timestamp: -1 });
mentionSchema.index({ sentiment: 1 });
mentionSchema.index({ influence_score: -1 });
mentionSchema.index({ source_quality: 1 });
mentionSchema.index({ author: 1 });

export default model('Mention', mentionSchema);

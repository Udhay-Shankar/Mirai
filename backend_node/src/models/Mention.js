import mongoose from 'mongoose';

const { Schema, model } = mongoose;

const mentionSchema = new Schema({
  keyword: { type: String, required: true, index: true },
  platform: { type: String, required: true, enum: ['twitter', 'reddit', 'youtube', 'news'] },
  text: { type: String, required: true },
  author: { type: String },
  author_name: { type: String },
  author_followers: { type: Number, default: 0 },
  url: { type: String, unique: true },
  timestamp: { type: Date },
  sentiment: { type: String, enum: ['positive', 'negative', 'neutral'] },
  sentiment_score: { type: Number },
  likes: { type: Number, default: 0 },
  retweets: { type: Number, default: 0 },
  comments: { type: Number, default: 0 },
  views: { type: Number, default: 0 },
  engagement: { type: Number, default: 0 },
  reach: { type: Number, default: 0 },
  language: { type: String },
  subreddit: { type: String },
  scraped_at: { type: Date, default: () => new Date() }
});

// Indexes for faster queries
mentionSchema.index({ keyword: 1, platform: 1 });
mentionSchema.index({ timestamp: -1 });
mentionSchema.index({ sentiment: 1 });

export default model('Mention', mentionSchema);

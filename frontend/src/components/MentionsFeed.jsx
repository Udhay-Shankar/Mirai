import React, { useState } from 'react';
import { 
  Twitter, 
  MessageCircle, 
  Youtube, 
  TrendingUp, 
  Heart, 
  Repeat, 
  Eye,
  MapPin,
  Calendar,
  ExternalLink,
  CheckCircle2,
  Award,
  Hash,
  Users,
  ChevronDown,
  Filter,
  Star
} from 'lucide-react';

const MentionsFeed = ({ mentions, analytics }) => {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('recent');

  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'twitter':
        return <Twitter className="w-5 h-5 text-[#1DA1F2]" />;
      case 'reddit':
        return <MessageCircle className="w-5 h-5 text-[#FF4500]" />;
      case 'youtube':
        return <Youtube className="w-5 h-5 text-[#FF0000]" />;
      default:
        return null;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'text-mint bg-mint/10 border-mint/30';
      case 'negative':
        return 'text-warning bg-warning/10 border-warning/30';
      default:
        return 'text-text-gray bg-border-gray/30 border-border-gray';
    }
  };

  const getSourceQualityBadge = (quality) => {
    const colors = {
      high: 'bg-mint/20 text-mint border-mint/40',
      medium: 'bg-accent/20 text-accent border-accent/40',
      low: 'bg-border-gray text-text-gray border-border-gray'
    };
    
    return (
      <span className={`px-2 py-1 rounded text-xs border ${colors[quality] || colors.low}`}>
        {quality?.toUpperCase() || 'N/A'}
      </span>
    );
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num?.toLocaleString() || '0';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  const filteredMentions = mentions.filter(m => {
    if (filter === 'all') return true;
    if (filter === 'high-quality') return m.source_quality === 'high';
    if (filter === 'verified') return m.author_verified;
    if (filter === 'influential') return (m.influence_score || 0) > 50;
    return m.sentiment === filter;
  });

  const sortedMentions = [...filteredMentions].sort((a, b) => {
    switch (sortBy) {
      case 'engagement':
        return (b.engagement || 0) - (a.engagement || 0);
      case 'reach':
        return (b.reach || 0) - (a.reach || 0);
      case 'influence':
        return (b.influence_score || 0) - (a.influence_score || 0);
      default:
        return new Date(b.timestamp) - new Date(a.timestamp);
    }
  });

  return (
    <div className="space-y-4">
      {/* Filters and Sorting */}
      <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-4">
        <div className="flex flex-wrap gap-3 items-center justify-between">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                filter === 'all'
                  ? 'bg-coral text-white'
                  : 'text-text-gray hover:bg-border-gray'
              }`}
            >
              All ({mentions.length})
            </button>
            <button
              onClick={() => setFilter('high-quality')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                filter === 'high-quality'
                  ? 'bg-coral text-white'
                  : 'text-text-gray hover:bg-border-gray'
              }`}
            >
              <Award className="w-4 h-4 inline mr-1" />
              High Quality
            </button>
            <button
              onClick={() => setFilter('verified')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                filter === 'verified'
                  ? 'bg-coral text-white'
                  : 'text-text-gray hover:bg-border-gray'
              }`}
            >
              <CheckCircle2 className="w-4 h-4 inline mr-1" />
              Verified
            </button>
            <button
              onClick={() => setFilter('influential')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                filter === 'influential'
                  ? 'bg-coral text-white'
                  : 'text-text-gray hover:bg-border-gray'
              }`}
            >
              <Star className="w-4 h-4 inline mr-1" />
              Influential
            </button>
          </div>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 bg-dark-navy/50 border border-border-gray rounded-lg text-white text-sm focus:outline-none focus:border-primary"
          >
            <option value="recent">Most Recent</option>
            <option value="engagement">Most Engaging</option>
            <option value="reach">Highest Reach</option>
            <option value="influence">Most Influential</option>
          </select>
        </div>
      </div>

      {/* Mentions List */}
      <div className="space-y-4">
        {sortedMentions.length === 0 ? (
          <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-12 text-center">
            <Filter className="w-16 h-16 text-text-gray/30 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">No mentions found</h3>
            <p className="text-text-gray">Try adjusting your filters</p>
          </div>
        ) : (
          sortedMentions.map((mention, index) => (
            <div
              key={mention._id || index}
              className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6 hover:border-primary/50 transition-all"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {getPlatformIcon(mention.platform)}
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white">
                        {mention.author_name || mention.author}
                      </span>
                      {mention.author_verified && (
                        <CheckCircle2 className="w-4 h-4 text-[#1DA1F2]" />
                      )}
                      {getSourceQualityBadge(mention.source_quality)}
                    </div>
                    <div className="flex items-center gap-3 mt-1 text-xs text-text-gray">
                      <span className="flex items-center gap-1">
                        <Users className="w-3 h-3" />
                        {formatNumber(mention.author_followers || 0)} followers
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {formatDate(mention.timestamp)}
                      </span>
                      {mention.location && (
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {mention.location}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  {mention.influence_score > 0 && (
                    <div className="text-right">
                      <div className="text-xs text-text-gray">Influence</div>
                      <div className="text-sm font-bold text-coral">
                        {Math.round(mention.influence_score)}
                      </div>
                    </div>
                  )}
                  <a
                    href={mention.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 hover:bg-primary/20 rounded-lg transition-colors"
                  >
                    <ExternalLink className="w-4 h-4 text-primary" />
                  </a>
                </div>
              </div>

              {/* Content */}
              <p className="text-white mb-4 leading-relaxed">
                {mention.text}
              </p>

              {/* Metadata Tags */}
              {(mention.hashtags?.length > 0 || mention.subreddit || mention.tags?.length > 0) && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {mention.hashtags?.slice(0, 5).map((tag, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-primary/10 text-primary rounded text-xs flex items-center gap-1"
                    >
                      <Hash className="w-3 h-3" />
                      {tag}
                    </span>
                  ))}
                  {mention.subreddit && (
                    <span className="px-2 py-1 bg-[#FF4500]/10 text-[#FF4500] rounded text-xs">
                      r/{mention.subreddit}
                    </span>
                  )}
                  {mention.tags?.slice(0, 3).map((tag, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-accent/10 text-accent rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Footer - Metrics */}
              <div className="flex items-center justify-between pt-4 border-t border-border-gray">
                <div className="flex items-center gap-6">
                  <div
                    className={`px-3 py-1 rounded-full text-xs font-medium border ${getSentimentColor(
                      mention.sentiment
                    )}`}
                  >
                    {mention.sentiment?.toUpperCase() || 'NEUTRAL'}
                  </div>
                  
                  {mention.likes > 0 && (
                    <span className="flex items-center gap-1 text-sm text-text-gray">
                      <Heart className="w-4 h-4 text-warning" />
                      {formatNumber(mention.likes)}
                    </span>
                  )}
                  
                  {mention.retweets > 0 && (
                    <span className="flex items-center gap-1 text-sm text-text-gray">
                      <Repeat className="w-4 h-4 text-mint" />
                      {formatNumber(mention.retweets)}
                    </span>
                  )}
                  
                  {mention.comments > 0 && (
                    <span className="flex items-center gap-1 text-sm text-text-gray">
                      <MessageCircle className="w-4 h-4 text-accent" />
                      {formatNumber(mention.comments)}
                    </span>
                  )}
                  
                  {mention.views > 0 && (
                    <span className="flex items-center gap-1 text-sm text-text-gray">
                      <Eye className="w-4 h-4 text-coral" />
                      {formatNumber(mention.views)}
                    </span>
                  )}
                </div>
                
                <div className="flex items-center gap-4 text-xs text-text-gray">
                  <div>
                    <span className="text-text-gray/70">Engagement: </span>
                    <span className="font-medium text-white">
                      {formatNumber(mention.engagement || 0)}
                    </span>
                  </div>
                  <div>
                    <span className="text-text-gray/70">Reach: </span>
                    <span className="font-medium text-white">
                      {formatNumber(mention.reach || 0)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Load More */}
      {sortedMentions.length > 0 && sortedMentions.length < mentions.length && (
        <button className="w-full py-3 bg-border-gray hover:bg-border-gray/70 text-text-gray rounded-lg transition-colors flex items-center justify-center gap-2">
          <ChevronDown className="w-5 h-5" />
          Load More Mentions
        </button>
      )}
    </div>
  );
};

export default MentionsFeed;

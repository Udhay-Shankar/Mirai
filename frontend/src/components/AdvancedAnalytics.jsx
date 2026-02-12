import React from 'react';
import { 
  TrendingUp, 
  Users, 
  MapPin, 
  Award, 
  Hash, 
  MessageCircle,
  CheckCircle2,
  BarChart3,
  Target,
  Zap
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

const AdvancedAnalytics = ({ analytics }) => {
  if (!analytics) return null;

  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num?.toLocaleString() || '0';
  };

  // Quality breakdown data for pie chart
  const qualityData = [
    { name: 'High', value: analytics.by_quality?.high || 0, color: '#10B981' },
    { name: 'Medium', value: analytics.by_quality?.medium || 0, color: '#6366F1' },
    { name: 'Low', value: analytics.by_quality?.low || 0, color: '#6B7280' }
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Reach */}
        <div className="bg-gradient-to-br from-primary/20 to-primary/10 backdrop-blur-sm rounded-xl border border-primary/30 p-4 hover:border-primary/50 transition-all">
          <div className="flex items-center justify-between mb-2">
            <span className="text-text-gray text-sm">Total Reach</span>
            <TrendingUp className="w-5 h-5 text-primary" />
          </div>
          <div className="text-2xl font-bold text-white">
            {formatNumber(analytics.total_reach || 0)}
          </div>
          <div className="text-xs text-mint mt-1">
            Potential impressions
          </div>
        </div>

        {/* Total Engagement */}
        <div className="bg-gradient-to-br from-coral/20 to-coral/10 backdrop-blur-sm rounded-xl border border-coral/30 p-4 hover:border-coral/50 transition-all">
          <div className="flex items-center justify-between mb-2">
            <span className="text-text-gray text-sm">Total Engagement</span>
            <Zap className="w-5 h-5 text-coral" />
          </div>
          <div className="text-2xl font-bold text-white">
            {formatNumber(analytics.total_engagement || 0)}
          </div>
          <div className="text-xs text-mint mt-1">
            Avg: {formatNumber(analytics.avg_engagement || 0)} per mention
          </div>
        </div>

        {/* Verified Authors */}
        <div className="bg-gradient-to-br from-accent/20 to-accent/10 backdrop-blur-sm rounded-xl border border-accent/30 p-4 hover:border-accent/50 transition-all">
          <div className="flex items-center justify-between mb-2">
            <span className="text-text-gray text-sm">Verified Sources</span>
            <CheckCircle2 className="w-5 h-5 text-accent" />
          </div>
          <div className="text-2xl font-bold text-white">
            {analytics.verified_ratio?.verified || 0}
          </div>
          <div className="text-xs text-text-gray mt-1">
            {analytics.total_mentions > 0 
              ? `${Math.round((analytics.verified_ratio?.verified / analytics.total_mentions) * 100)}% of total`
              : '0% of total'}
          </div>
        </div>

        {/* Avg Influence */}
        <div className="bg-gradient-to-br from-mint/20 to-mint/10 backdrop-blur-sm rounded-xl border border-mint/30 p-4 hover:border-mint/50 transition-all">
          <div className="flex items-center justify-between mb-2">
            <span className="text-text-gray text-sm">Avg Influence</span>
            <Award className="w-5 h-5 text-mint" />
          </div>
          <div className="text-2xl font-bold text-white">
            {analytics.avg_influence_score || 0}/100
          </div>
          <div className="text-xs text-text-gray mt-1">
            Source quality score
          </div>
        </div>
      </div>

      {/* Timeline Chart */}
      {analytics.timeline && analytics.timeline.length > 0 && (
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-coral" />
            Mentions Over Time
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics.timeline}>
              <XAxis 
                dataKey="date" 
                stroke="#6B7280" 
                tick={{ fill: '#9CA3AF' }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis stroke="#6B7280" tick={{ fill: '#9CA3AF' }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#F3F4F6'
                }}
              />
              <Line type="monotone" dataKey="count" stroke="#A78BFA" strokeWidth={2} name="Mentions" />
              <Line type="monotone" dataKey="positive" stroke="#10B981" strokeWidth={2} name="Positive" />
              <Line type="monotone" dataKey="negative" stroke="#EF4444" strokeWidth={2} name="Negative" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Source Quality Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-mint" />
            Source Quality Breakdown
          </h3>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={qualityData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {qualityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-4">
            {qualityData.map((item, index) => (
              <div key={index} className="text-center">
                <div className="flex items-center justify-center gap-2 mb-1">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-text-gray">{item.name}</span>
                </div>
                <div className="text-lg font-bold text-white">{item.value}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Engagement Metrics */}
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-coral" />
            Engagement Breakdown
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-dark-navy/30 rounded-lg">
              <span className="text-text-gray flex items-center gap-2">
                <span className="text-2xl">❤️</span> Total Likes
              </span>
              <span className="text-white font-bold">{formatNumber(analytics.total_likes || 0)}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-dark-navy/30 rounded-lg">
              <span className="text-text-gray flex items-center gap-2">
                <MessageCircle className="w-5 h-5 text-accent" /> Total Comments
              </span>
              <span className="text-white font-bold">{formatNumber(analytics.total_comments || 0)}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-dark-navy/30 rounded-lg">
              <span className="text-text-gray flex items-center gap-2">
                <span className="text-2xl">🔁</span> Total Retweets
              </span>
              <span className="text-white font-bold">{formatNumber(analytics.total_retweets || 0)}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-dark-navy/30 rounded-lg">
              <span className="text-text-gray flex items-center gap-2">
                <span className="text-2xl">👁️</span> Total Views
              </span>
              <span className="text-white font-bold">{formatNumber(analytics.total_views || 0)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top Influencers */}
      {analytics.top_authors && analytics.top_authors.length > 0 && (
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-primary" />
            Top Influencers
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analytics.top_authors.slice(0, 6).map((author, index) => (
              <div key={index} className="bg-dark-navy/30 rounded-lg p-4 hover:bg-dark-navy/50 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-white">{author.author}</span>
                    {author.verified && (
                      <CheckCircle2 className="w-4 h-4 text-[#1DA1F2]" />
                    )}
                  </div>
                  <span className="text-xs text-text-gray">{author.mention_count} mentions</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-gray">Followers:</span>
                  <span className="text-white font-medium">{formatNumber(author.followers)}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-gray">Engagement:</span>
                  <span className="text-mint font-medium">{formatNumber(author.total_engagement)}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-gray">Influence:</span>
                  <span className="text-coral font-medium">{author.avg_influence}/100</span>
                </div>
                <div className="flex gap-1 mt-2">
                  {author.platforms.map((platform, i) => (
                    <span key={i} className="px-2 py-1 bg-border-gray text-text-gray rounded text-xs">
                      {platform}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Hashtags */}
      {analytics.top_hashtags && analytics.top_hashtags.length > 0 && (
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Hash className="w-5 h-5 text-accent" />
            Trending Hashtags
          </h3>
          <div className="flex flex-wrap gap-3">
            {analytics.top_hashtags.map((item, index) => (
              <div
                key={index}
                className="px-4 py-2 bg-primary/10 text-primary rounded-full border border-primary/30 hover:bg-primary/20 transition-all flex items-center gap-2"
              >
                <Hash className="w-4 h-4" />
                <span className="font-medium">{item.tag}</span>
                <span className="text-sm text-primary/70">({item.count})</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Subreddits */}
      {analytics.top_subreddits && analytics.top_subreddits.length > 0 && (
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <MessageCircle className="w-5 h-5 text-[#FF4500]" />
            Top Subreddits
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analytics.top_subreddits.map((item, index) => (
              <div key={index} className="bg-dark-navy/30 rounded-lg p-4 hover:bg-dark-navy/50 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-white font-bold">r/{item.name}</span>
                  <span className="text-xs text-text-gray">{item.count} posts</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-gray">Engagement:</span>
                  <span className="text-coral font-medium">{formatNumber(item.total_engagement)}</span>
                </div>
                {item.subscribers > 0 && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-gray">Subscribers:</span>
                    <span className="text-white font-medium">{formatNumber(item.subscribers)}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Geographic Distribution */}
      {analytics.top_locations && analytics.top_locations.length > 0 && (
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <MapPin className="w-5 h-5 text-mint" />
            Geographic Distribution
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {analytics.top_locations.map((item, index) => (
              <div
                key={index}
                className="bg-dark-navy/30 rounded-lg p-3 hover:bg-dark-navy/50 transition-all"
              >
                <div className="flex items-center gap-2 mb-1">
                  <MapPin className="w-4 h-4 text-mint" />
                  <span className="text-white text-sm font-medium truncate">
                    {item.location}
                  </span>
                </div>
                <div className="text-xs text-text-gray">{item.count} mentions</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedAnalytics;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { analyticsAPI, subscriptionAPI } from '../services/api';
import { Sparkles, Search, LogOut, Crown, TrendingUp, Users, BarChart3, AlertCircle, Bookmark, Zap, Eye, Clock, ArrowUpRight, ArrowDownRight, Plus, Filter, Star } from 'lucide-react';
import MentionsChart from './MentionsChart';
import SentimentChart from './SentimentChart';
import InfluencerList from './InfluencerList';
import TrendingMetrics from './TrendingMetrics';
import MiraiLogo from './MiraiLogo';
import MentionsFeed from './MentionsFeed';
import AdvancedAnalytics from './AdvancedAnalytics';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [keyword, setKeyword] = useState('');
  const [searching, setSearching] = useState(false);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [subscription, setSubscription] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [savedCollections, setSavedCollections] = useState([]);
  const [trackedNiches, setTrackedNiches] = useState([]);
  const [outliers, setOutliers] = useState([]);

  useEffect(() => {
    fetchSubscriptionStatus();
    // Initialize Mittalmar-style features
    initializeLiveTracking();
  }, []);

  const initializeLiveTracking = () => {
    // Mock data for Mittalmar-style features
    // In production, this would fetch from Awario API
    setTrackedNiches([
      {
        id: 1,
        name: 'AI Tools',
        mentions: 1247,
        growth: '+156%',
        trending: true,
        autoUpdate: true,
        lastUpdated: '23 min ago'
      },
      {
        id: 2,
        name: 'SaaS Pricing',
        mentions: 892,
        growth: '+89%',
        trending: true,
        autoUpdate: true,
        lastUpdated: '1 hour ago'
      }
    ]);

    setOutliers([
      {
        id: 1,
        content: 'How I automated my entire content workflow',
        mentions: 1840,
        spike: '+1200%',
        time: '4 hours ago'
      }
    ]);

    setSavedCollections([
      {
        id: 1,
        name: 'Viral Posts',
        count: 47,
        lastUpdated: '2 hours ago'
      }
    ]);
  };

  const fetchSubscriptionStatus = async () => {
    try {
      const response = await subscriptionAPI.getStatus();
      setSubscription(response.data);
    } catch (err) {
      console.error('Error fetching subscription:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setSearching(true);
    setError('');
    setAnalyticsData(null);

    try {
      // Use new scraper API
      const token = localStorage.getItem('accessToken');
      
      if (!token) {
        throw new Error('Not authenticated. Please login again.');
      }
      
      // Trigger scraping
      const scrapeResponse = await fetch('http://localhost:8000/api/scrape/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ keyword: keyword.trim() })
      });

      if (!scrapeResponse.ok) {
        throw new Error('Failed to scrape mentions');
      }

      const scrapeResult = await scrapeResponse.json();
      
      // Fetch analytics data
      const mentionsResponse = await fetch(`http://localhost:8000/api/scrape/mentions/${keyword.trim()}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!mentionsResponse.ok) {
        throw new Error('Failed to fetch analytics');
      }

      const analyticsResult = await mentionsResponse.json();
      
      // Transform data to match existing format
      const formattedData = {
        total_mentions: analyticsResult.analytics.total_mentions || 0,
        unique_authors: analyticsResult.analytics.by_platform ? 
          Object.values(analyticsResult.analytics.by_platform).reduce((a, b) => a + b, 0) : 0,
        total_reach: analyticsResult.analytics.total_reach || 0,
        avg_engagement: analyticsResult.analytics.total_engagement || 0,
        sentiment_breakdown: {
          positive: analyticsResult.analytics.sentiment?.positive || 0,
          neutral: analyticsResult.analytics.sentiment?.neutral || 0,
          negative: analyticsResult.analytics.sentiment?.negative || 0
        },
        sources: analyticsResult.analytics.by_platform || {},
        top_keywords: analyticsResult.analytics.top_keywords || [],
        mentions: analyticsResult.mentions || []
      };

      setAnalyticsData(formattedData);
    } catch (err) {
      setError(err.message || 'Failed to fetch analytics data');
      console.error('Error fetching analytics:', err);
    } finally {
      setSearching(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      console.error('Error logging out:', err);
    }
  };

  const handleUpgrade = () => {
    // In a real app, this would open a payment modal
    alert('Upgrade feature coming soon! For now, contact support to upgrade your account.');
  };

  const isPremium = subscription?.is_premium || false;

  return (
    <div className="min-h-screen bg-dark-navy text-text-gray">
      {/* Header */}
      <header className="bg-dark-navy/90 backdrop-blur-lg border-b border-border-gray shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <MiraiLogo size={40} />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary via-accent to-coral bg-clip-text text-transparent font-mirai">Mirai</h1>
            </div>

            <div className="flex items-center space-x-4">
              {!isPremium && (
                <button
                  onClick={handleUpgrade}
                  className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-lavender to-lavender/80 text-dark-navy rounded-lg hover:opacity-90 transition font-medium"
                >
                  <Crown className="w-4 h-4" />
                  <span>Upgrade to Premium</span>
                </button>
              )}
              
              <div className="flex items-center space-x-2">
                <div className="text-right">
                  <p className="text-sm font-medium text-white">
                    {user?.display_name || user?.email || 'User'}
                  </p>
                  <p className="text-xs text-text-gray">
                    {isPremium ? (
                      <span className="px-2 py-1 bg-mint/20 text-mint rounded text-xs">Premium</span>
                    ) : (
                      <span className="px-2 py-1 bg-border-gray text-text-gray rounded text-xs">Free</span>
                    )}
                  </p>
                </div>
                {user?.photo_url && (
                  <img
                    src={user.photo_url}
                    alt="Profile"
                    className="w-10 h-10 rounded-full border-2 border-primary"
                  />
                )}
              </div>

              <button
                onClick={handleLogout}
                className="p-2 text-text-gray hover:text-coral transition"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Mittalmar-style Quick Actions */}
        {isPremium && !analyticsData && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <button className="bg-gradient-to-br from-primary to-primary/80 rounded-xl p-6 text-left hover:scale-105 transition-transform shadow-lg shadow-primary/20">
              <Plus size={24} className="text-white mb-3" />
              <h3 className="text-lg font-bold text-white mb-2">Create Niche Folder</h3>
              <p className="text-sm text-white/70">Auto-track topics & competitors</p>
            </button>
            
            <button className="bg-gradient-to-br from-coral to-coral/80 rounded-xl p-6 text-left hover:scale-105 transition-transform shadow-lg shadow-coral/20">
              <Zap size={24} className="text-white mb-3" />
              <h3 className="text-lg font-bold text-white mb-2">Find Outliers</h3>
              <p className="text-sm text-white/70">Discover viral spikes instantly</p>
            </button>
            
            <button className="bg-gradient-to-br from-accent to-accent/80 rounded-xl p-6 text-left hover:scale-105 transition-transform shadow-lg shadow-accent/20">
              <Bookmark size={24} className="text-white mb-3" />
              <h3 className="text-lg font-bold text-white mb-2">Save Collections</h3>
              <p className="text-sm text-white/70">Build viral content boards</p>
            </button>
          </div>
        )}

        {/* Search Section */}
        <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6 mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">Search Brand Mentions</h2>
          <form onSubmit={handleSearch} className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-3.5 w-5 h-5 text-text-gray" />
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Enter brand name or keyword..."
                className="w-full pl-10 pr-4 py-3 bg-dark-navy/50 border border-border-gray rounded-lg text-white placeholder-text-gray focus:outline-none focus:border-primary transition-colors"
                disabled={searching}
              />
            </div>
            <button
              type="submit"
              disabled={searching || !keyword.trim()}
              className="px-6 py-3 bg-gradient-to-r from-lavender to-lavender/90 text-dark-navy rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {searching ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>

        {error && (
          <div className="bg-warning/10 border border-warning text-warning px-4 py-3 rounded-lg mb-8 flex items-start">
            <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {analyticsData && (
          <>
            {/* Upgrade Notice for Free Users */}
            {!isPremium && analyticsData.message && (
              <div className="bg-primary/10 border border-primary text-primary px-4 py-3 rounded-lg mb-8 flex items-center justify-between">
                <span>{analyticsData.message}</span>
                <button onClick={handleUpgrade} className="btn btn-primary btn-sm ml-4">
                  Upgrade Now
                </button>
              </div>
            )}

            {/* Tabs - Mittalmar Style */}
            <div className="flex gap-3 mb-6 flex-wrap">
              <button
                onClick={() => setActiveTab('overview')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === 'overview'
                    ? 'bg-coral text-white shadow-lg shadow-coral/30'
                    : 'text-text-gray hover:text-white hover:bg-border-gray'
                }`}
              >
                <BarChart3 size={16} />
                Overview
              </button>
              {isPremium && (
                <>
                  <button
                    onClick={() => setActiveTab('trends')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === 'trends'
                        ? 'bg-coral text-white shadow-lg shadow-coral/30'
                        : 'text-text-gray hover:text-white hover:bg-border-gray'
                    }`}
                  >
                    <TrendingUp size={16} />
                    Trends
                  </button>
                  <button
                    onClick={() => setActiveTab('influencers')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === 'influencers'
                        ? 'bg-coral text-white shadow-lg shadow-coral/30'
                        : 'text-text-gray hover:text-white hover:bg-border-gray'
                    }`}
                  >
                    <Users size={16} />
                    Influencers
                  </button>
                  <button
                    onClick={() => setActiveTab('outliers')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === 'outliers'
                        ? 'bg-coral text-white shadow-lg shadow-coral/30'
                        : 'text-text-gray hover:text-white hover:bg-border-gray'
                    }`}
                  >
                    <Sparkles size={16} />
                    Outliers
                  </button>
                  <button
                    onClick={() => setActiveTab('collections')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === 'collections'
                        ? 'bg-coral text-white shadow-lg shadow-coral/30'
                        : 'text-text-gray hover:text-white hover:bg-border-gray'
                    }`}
                  >
                    <Bookmark size={16} />
                    Collections
                  </button>
                </>
              )}
            </div>

            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Stats Grid - Mittalmar Style */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-gradient-to-br from-primary/20 to-primary/10 backdrop-blur-sm rounded-xl border border-primary/30 p-6 hover:border-primary/50 transition-all shadow-lg shadow-primary/10">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-text-gray text-sm mb-1">Total Mentions</p>
                        <p className="text-3xl font-bold text-white">
                          {analyticsData.total_mentions?.toLocaleString() || 0}
                        </p>
                        <p className="text-mint text-sm mt-2">+23% vs last week</p>
                      </div>
                      <TrendingUp className="w-8 h-8 text-primary" />
                    </div>
                  </div>

                  {isPremium && analyticsData.unique_authors !== undefined && (
                    <div className="bg-gradient-to-br from-coral/20 to-coral/10 backdrop-blur-sm rounded-xl border border-coral/30 p-6 hover:border-coral/50 transition-all shadow-lg shadow-coral/10">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-text-gray text-sm mb-1">Unique Authors</p>
                          <p className="text-3xl font-bold text-white">
                            {analyticsData.unique_authors?.toLocaleString() || 0}
                          </p>
                          <p className="text-mint text-sm mt-2">+15% growth</p>
                        </div>
                        <Users className="w-8 h-8 text-coral" />
                      </div>
                    </div>
                  )}

                  {isPremium && analyticsData.total_reach !== undefined && (
                    <div className="bg-gradient-to-br from-accent/20 to-accent/10 backdrop-blur-sm rounded-xl border border-accent/30 p-6 hover:border-accent/50 transition-all shadow-lg shadow-accent/10">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-text-gray text-sm mb-1">Total Reach</p>
                          <p className="text-3xl font-bold text-white">
                            {(analyticsData.total_reach / 1000).toFixed(1)}K
                          </p>
                          <p className="text-mint text-sm mt-2">Trending up</p>
                        </div>
                        <BarChart3 className="w-8 h-8 text-accent" />
                      </div>
                    </div>
                  )}
                </div>

                {/* Sentiment Chart */}
                {analyticsData.sentiment_breakdown && (
                  <SentimentChart data={analyticsData.sentiment_breakdown} />
                )}

                {/* Top Keywords */}
                {analyticsData.top_keywords && analyticsData.top_keywords.length > 0 && (
                  <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
                    <h3 className="text-xl font-bold text-white mb-4">Top Keywords/Hashtags</h3>
                    <div className="flex flex-wrap gap-2">
                      {analyticsData.top_keywords.map((item, index) => (
                        <span key={index} className="px-4 py-2 bg-primary/20 text-primary rounded-full text-sm font-medium border border-primary/30 hover:bg-primary/30 transition-colors">
                          #{item.tag || item.keyword} ({item.count})
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Source Breakdown */}
                {analyticsData.sources && Object.keys(analyticsData.sources).length > 0 && (
                  <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6">
                    <h3 className="text-xl font-bold text-white mb-4">Source Breakdown</h3>
                    <div className="space-y-3">
                      {Object.entries(analyticsData.sources).map(([source, count]) => (
                        <div key={source} className="flex items-center justify-between">
                          <span className="capitalize font-medium text-white">{source}</span>
                          <div className="flex items-center space-x-2">
                            <div className="w-32 bg-border-gray rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-primary to-accent h-2 rounded-full"
                                style={{
                                  width: `${(count / analyticsData.total_mentions) * 100}%`,
                                }}
                              ></div>
                            </div>
                            <span className="text-text-gray text-sm w-12 text-right">
                              {count}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Trends Tab (Premium) */}
            {activeTab === 'trends' && isPremium && (
              <div className="space-y-6">
                {analyticsData.trends && <MentionsChart data={analyticsData.trends} />}
                {analyticsData.trends && <TrendingMetrics data={analyticsData.trends} />}
              </div>
            )}

            {/* Influencers Tab (Premium) */}
            {activeTab === 'influencers' && isPremium && (
              <InfluencerList keyword={keyword} />
            )}

            {/* Outliers Tab (Premium) - Mittalmar Style */}
            {activeTab === 'outliers' && isPremium && (
              <div className="space-y-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-white">Viral Outliers</h2>
                    <p className="text-sm text-text-gray mt-1">Content experiencing unusual spikes</p>
                  </div>
                  <button className="flex items-center gap-2 px-4 py-2 bg-border-gray text-text-gray rounded-lg hover:bg-border-gray/70 transition-colors">
                    <Filter size={16} />
                    Filter
                  </button>
                </div>

                {outliers.length > 0 ? (
                  <div className="grid grid-cols-1 gap-6">
                    {outliers.map(outlier => (
                      <div key={outlier.id} className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-6 hover:border-mint/50 transition-all">
                        <div className="flex items-start gap-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-mint/20 to-mint/10 rounded-lg flex items-center justify-center flex-shrink-0">
                            <Sparkles size={24} className="text-mint" />
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <span className="px-3 py-1 bg-mint/20 text-mint rounded-full text-xs font-bold">
                                {outlier.spike} SPIKE
                              </span>
                              <span className="text-xs text-text-gray">{outlier.time}</span>
                            </div>
                            
                            <h3 className="text-lg font-bold text-white mb-2">{outlier.content}</h3>
                            
                            <div className="flex items-center gap-6">
                              <div className="flex items-center gap-2">
                                <TrendingUp size={16} className="text-accent" />
                                <span className="text-sm text-text-gray">{outlier.mentions} mentions</span>
                              </div>
                            </div>
                          </div>

                          <div className="flex gap-2">
                            <button className="p-2 bg-coral/20 text-coral rounded-lg hover:bg-coral/30 transition-colors">
                              <Bookmark size={16} />
                            </button>
                            <button className="px-4 py-2 bg-primary/20 text-primary rounded-lg text-sm hover:bg-primary/30 transition-colors">
                              Analyze
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-12 text-center">
                    <Sparkles className="w-16 h-16 text-text-gray/30 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">No Outliers Found</h3>
                    <p className="text-text-gray">Search for keywords to discover viral spikes</p>
                  </div>
                )}
              </div>
            )}

            {/* Collections Tab (Premium) - Mittalmar Style */}
            {activeTab === 'collections' && isPremium && (
              <div className="space-y-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-white">Viral Content Collections</h2>
                  <button className="flex items-center gap-2 px-4 py-2 bg-coral text-white rounded-lg hover:opacity-90 transition-opacity">
                    <Plus size={16} />
                    New Collection
                  </button>
                </div>

                {savedCollections.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {savedCollections.map(collection => (
                      <div key={collection.id} className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray overflow-hidden hover:border-coral/50 transition-all hover:scale-105">
                        <div className="h-40 bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
                          <Bookmark size={48} className="text-white/50" />
                        </div>
                        <div className="p-6">
                          <h3 className="text-lg font-bold text-white mb-2">{collection.name}</h3>
                          <div className="space-y-2 mb-4">
                            <div className="flex items-center justify-between text-sm">
                              <span className="text-text-gray">Content Items</span>
                              <span className="text-white font-medium">{collection.count}</span>
                            </div>
                          </div>
                          <p className="text-xs text-text-gray/70 mb-4">Updated {collection.lastUpdated}</p>
                          <button className="w-full py-2 bg-coral/20 text-coral rounded-lg text-sm hover:bg-coral/30 transition-colors">
                            View Collection
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-12 text-center">
                    <Bookmark className="w-16 h-16 text-text-gray/30 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">No Collections Yet</h3>
                    <p className="text-text-gray">Start saving viral content to build inspiration boards</p>
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {/* Empty State */}
        {!analyticsData && !searching && (
          <div className="bg-gradient-to-br from-[#F5F7FA]/[0.05] to-[#F5F7FA]/[0.02] backdrop-blur-sm rounded-xl border border-border-gray p-12 text-center">
            <Search className="w-16 h-16 text-text-gray/30 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">
              No Data Yet
            </h3>
            <p className="text-text-gray">
              Enter a keyword above to start tracking mentions and analytics
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;

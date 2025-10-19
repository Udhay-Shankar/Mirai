import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { Users, ExternalLink, CheckCircle } from 'lucide-react';

const InfluencerList = ({ keyword }) => {
  const [influencers, setInfluencers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (keyword) {
      fetchInfluencers();
    }
  }, [keyword]);

  const fetchInfluencers = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await analyticsAPI.getInfluencers(keyword);
      setInfluencers(response.data.influencers || []);
    } catch (err) {
      setError('Failed to fetch influencers');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
        <p className="text-neutral-600 mt-4">Loading influencers...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-warning/10 border border-warning text-warning">
        {error}
      </div>
    );
  }

  if (influencers.length === 0) {
    return (
      <div className="card text-center py-8">
        <Users className="w-12 h-12 text-neutral-300 mx-auto mb-4" />
        <p className="text-neutral-600">No influencers found for this keyword</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-xl font-display mb-6">Top Influencers</h3>
      
      <div className="space-y-4">
        {influencers.map((influencer, index) => (
          <div
            key={influencer.author_id || index}
            className="flex items-start space-x-4 p-4 border border-neutral-200 rounded-lg hover:border-primary transition"
          >
            {/* Profile Image */}
            <div className="flex-shrink-0">
              {influencer.profile_image ? (
                <img
                  src={influencer.profile_image}
                  alt={influencer.author_name}
                  className="w-12 h-12 rounded-full"
                />
              ) : (
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <Users className="w-6 h-6 text-primary" />
                </div>
              )}
            </div>

            {/* Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-1">
                <h4 className="font-medium text-neutral-800 truncate">
                  {influencer.author_name || 'Unknown'}
                </h4>
                {influencer.verified && (
                  <CheckCircle className="w-4 h-4 text-primary flex-shrink-0" />
                )}
              </div>
              
              {influencer.author_username && (
                <p className="text-sm text-neutral-500 mb-2">
                  @{influencer.author_username}
                </p>
              )}

              <div className="flex flex-wrap gap-4 text-sm">
                <span className="text-neutral-600">
                  <strong className="text-neutral-800">
                    {influencer.followers?.toLocaleString() || 0}
                  </strong>{' '}
                  followers
                </span>
                <span className="text-neutral-600">
                  <strong className="text-neutral-800">
                    {influencer.mention_count || 0}
                  </strong>{' '}
                  mentions
                </span>
                <span className="text-neutral-600">
                  <strong className="text-neutral-800">
                    {influencer.avg_engagement_rate || 0}%
                  </strong>{' '}
                  engagement
                </span>
              </div>
            </div>

            {/* Action */}
            {influencer.profile_url && (
              <a
                href={influencer.profile_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-shrink-0 p-2 text-primary hover:bg-primary/10 rounded-lg transition"
                title="View Profile"
              >
                <ExternalLink className="w-5 h-5" />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default InfluencerList;

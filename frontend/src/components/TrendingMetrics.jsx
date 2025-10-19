import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';

const TrendingMetrics = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Calculate trend (comparing first and last data points)
  const firstPoint = data[0];
  const lastPoint = data[data.length - 1];
  const trendPercentage = ((lastPoint.count - firstPoint.count) / firstPoint.count) * 100;
  const isPositiveTrend = trendPercentage > 0;

  // Prepare sentiment data for chart
  const sentimentData = data.map((item) => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    positive: item.sentiment?.positive || 0,
    neutral: item.sentiment?.neutral || 0,
    negative: item.sentiment?.negative || 0,
  }));

  return (
    <div className="space-y-6">
      {/* Trend Summary */}
      <div className="card">
        <h3 className="text-xl font-display mb-4">Trend Analysis</h3>
        
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-neutral-100 rounded-lg">
            <p className="text-sm text-neutral-600 mb-1">Trend Direction</p>
            <div className="flex items-center space-x-2">
              {isPositiveTrend ? (
                <>
                  <TrendingUp className="w-6 h-6 text-accent" />
                  <span className="text-2xl font-bold text-accent">
                    +{Math.abs(trendPercentage).toFixed(1)}%
                  </span>
                </>
              ) : (
                <>
                  <TrendingDown className="w-6 h-6 text-warning" />
                  <span className="text-2xl font-bold text-warning">
                    -{Math.abs(trendPercentage).toFixed(1)}%
                  </span>
                </>
              )}
            </div>
          </div>

          <div className="p-4 bg-neutral-100 rounded-lg">
            <p className="text-sm text-neutral-600 mb-1">Peak Mentions</p>
            <p className="text-2xl font-bold text-neutral-800">
              {Math.max(...data.map(d => d.count))}
            </p>
          </div>

          <div className="p-4 bg-neutral-100 rounded-lg">
            <p className="text-sm text-neutral-600 mb-1">Average Daily</p>
            <p className="text-2xl font-bold text-neutral-800">
              {Math.round(data.reduce((sum, d) => sum + d.count, 0) / data.length)}
            </p>
          </div>
        </div>
      </div>

      {/* Sentiment Timeline */}
      <div className="card">
        <h3 className="text-xl font-display mb-4">Sentiment Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={sentimentData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="positive" stackId="a" fill="#059669" />
            <Bar dataKey="neutral" stackId="a" fill="#6B7280" />
            <Bar dataKey="negative" stackId="a" fill="#DC2626" />
          </BarChart>
        </ResponsiveContainer>
        
        <div className="flex justify-center space-x-6 mt-4">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-accent rounded"></div>
            <span className="text-sm text-neutral-600">Positive</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-neutral-500 rounded"></div>
            <span className="text-sm text-neutral-600">Neutral</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-warning rounded"></div>
            <span className="text-sm text-neutral-600">Negative</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendingMetrics;

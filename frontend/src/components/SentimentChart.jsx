import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Smile, Meh, Frown } from 'lucide-react';

const SentimentChart = ({ data }) => {
  if (!data) return null;

  const chartData = [
    { name: 'Positive', value: data.positive || 0, color: '#059669' },
    { name: 'Neutral', value: data.neutral || 0, color: '#6B7280' },
    { name: 'Negative', value: data.negative || 0, color: '#DC2626' },
  ].filter(item => item.value > 0);

  if (chartData.length === 0) return null;

  const total = chartData.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="card">
      <h3 className="text-xl font-display mb-4">Sentiment Analysis</h3>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>

        {/* Sentiment Stats */}
        <div className="flex flex-col justify-center space-y-4">
          {data.positive > 0 && (
            <div className="flex items-center justify-between p-3 bg-accent/10 rounded-lg">
              <div className="flex items-center space-x-2">
                <Smile className="w-5 h-5 text-accent" />
                <span className="font-medium text-neutral-800">Positive</span>
              </div>
              <span className="text-lg font-bold text-accent">
                {data.positive} ({((data.positive / total) * 100).toFixed(1)}%)
              </span>
            </div>
          )}

          {data.neutral > 0 && (
            <div className="flex items-center justify-between p-3 bg-neutral-200 rounded-lg">
              <div className="flex items-center space-x-2">
                <Meh className="w-5 h-5 text-neutral-600" />
                <span className="font-medium text-neutral-800">Neutral</span>
              </div>
              <span className="text-lg font-bold text-neutral-600">
                {data.neutral} ({((data.neutral / total) * 100).toFixed(1)}%)
              </span>
            </div>
          )}

          {data.negative > 0 && (
            <div className="flex items-center justify-between p-3 bg-warning/10 rounded-lg">
              <div className="flex items-center space-x-2">
                <Frown className="w-5 h-5 text-warning" />
                <span className="font-medium text-neutral-800">Negative</span>
              </div>
              <span className="text-lg font-bold text-warning">
                {data.negative} ({((data.negative / total) * 100).toFixed(1)}%)
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;

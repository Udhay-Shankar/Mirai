import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const MentionsChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.map((item) => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    mentions: item.count,
    reach: item.reach,
  }));

  return (
    <div className="card">
      <h3 className="text-xl font-display mb-4">Mentions Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="mentions"
            stroke="#0066CC"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="reach"
            stroke="#6B46C1"
            strokeWidth={2}
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MentionsChart;

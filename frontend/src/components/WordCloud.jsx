import React from 'react';

// Simple WordCloud component
// In a production app, you'd use a library like react-wordcloud or d3-cloud
const WordCloud = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Simple word cloud visualization using scaled text
  const maxCount = Math.max(...data.map(item => item.count));

  const getSize = (count) => {
    const minSize = 14;
    const maxSize = 48;
    return minSize + ((count / maxCount) * (maxSize - minSize));
  };

  const colors = ['#0066CC', '#6B46C1', '#059669', '#DC2626', '#6B7280'];

  return (
    <div className="card">
      <h3 className="text-xl font-display mb-4">Trending Words</h3>
      
      <div className="flex flex-wrap gap-3 items-center justify-center p-6 bg-neutral-50 rounded-lg min-h-[200px]">
        {data.slice(0, 30).map((item, index) => (
          <span
            key={index}
            className="font-bold transition-transform hover:scale-110 cursor-default"
            style={{
              fontSize: `${getSize(item.count)}px`,
              color: colors[index % colors.length],
              opacity: 0.7 + (item.count / maxCount) * 0.3,
            }}
            title={`${item.tag || item.word}: ${item.count} mentions`}
          >
            {item.tag || item.word}
          </span>
        ))}
      </div>
    </div>
  );
};

export default WordCloud;

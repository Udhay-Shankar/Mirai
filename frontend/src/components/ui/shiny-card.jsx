import React from 'react';
import './shiny-card.css';

const ShinyCard = ({ featureName, featureItems, icon, price, period, popular = false, className = '' }) => {
  return (
    <div className={`shiny-card space-y-3 min-h-72 shadow-2xl ${className}`}>
      {popular && (
        <div className="inline-block px-3 py-1 bg-white/10 text-white/60 text-xs tracking-wider mb-2">
          MOST POPULAR
        </div>
      )}
      
      {icon && <p className="text-5xl mb-5 mt-1">{icon}</p>}
      
      <div className="border-b border-white/10 pb-6 mb-6">
        <div className="text-xs text-white/30 tracking-wider mb-2">{featureName}</div>
        <div className="flex items-baseline gap-2">
          <span className="text-7xl font-bold text-white">${price}</span>
          <span className="text-xs text-white/30">{period}</span>
        </div>
      </div>

      <ul className="space-y-3">
        {featureItems.map((item, index) => (
          <li
            key={index}
            className="text-sm font-medium flex items-start gap-3 text-white/60"
          >
            <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center bg-white/10 text-white rounded-full mt-0.5">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
              </svg>
            </span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ShinyCard;

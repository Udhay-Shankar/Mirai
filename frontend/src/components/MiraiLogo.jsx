import React from 'react';

const MiraiLogo = ({ size = 40, animate = false, className = '' }) => {
  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <svg 
        viewBox="0 0 200 200" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        className={animate ? 'animate-spin-logo' : ''}
        style={{ width: '100%', height: '100%' }}
      >
        {/* Growth leaves at top - Cyan */}
        <g className="leaves">
          <path d="M100 20 Q85 35 90 50 Q95 45 100 40 Q105 45 110 50 Q115 35 100 20 Z" fill="url(#cyanGradient)" opacity="0.9" />
          <path d="M85 30 Q75 40 78 52 Q82 48 85 45" stroke="url(#cyanGradient)" strokeWidth="2" fill="none" />
          <path d="M115 30 Q125 40 122 52 Q118 48 115 45" stroke="url(#cyanGradient)" strokeWidth="2" fill="none" />
        </g>

        {/* Main spiral swirl - Multiple curves */}
        <g className="spiral-swirl">
          {/* Outer coral/orange curves */}
          <path 
            d="M120 50 Q140 70 145 100 Q148 130 130 150 Q110 165 85 160" 
            stroke="url(#coralOrangeGradient)" 
            strokeWidth="5" 
            strokeLinecap="round"
            fill="none"
            opacity="0.85"
          />
          <path 
            d="M125 55 Q143 75 147 102 Q149 128 133 145" 
            stroke="url(#coralOrangeGradient)" 
            strokeWidth="4" 
            strokeLinecap="round"
            fill="none"
            opacity="0.7"
          />
          
          {/* Pink/Magenta inner curves */}
          <path 
            d="M110 55 Q95 75 92 100 Q90 125 105 145 Q125 160 145 155" 
            stroke="url(#pinkMagentaGradient)" 
            strokeWidth="5" 
            strokeLinecap="round"
            fill="none"
            opacity="0.85"
          />
          <path 
            d="M105 60 Q92 78 90 103 Q89 123 102 140" 
            stroke="url(#pinkMagentaGradient)" 
            strokeWidth="4" 
            strokeLinecap="round"
            fill="none"
            opacity="0.7"
          />
          
          {/* Cyan/Blue flowing curves */}
          <path 
            d="M115 45 Q130 65 138 90 Q142 110 135 130 Q125 145 110 148" 
            stroke="url(#cyanBlueGradient)" 
            strokeWidth="5" 
            strokeLinecap="round"
            fill="none"
            opacity="0.85"
          />
          <path 
            d="M118 50 Q132 68 139 88 Q142 105 137 125" 
            stroke="url(#cyanBlueGradient)" 
            strokeWidth="4" 
            strokeLinecap="round"
            fill="none"
            opacity="0.7"
          />
          
          {/* Inner spiral loops */}
          <path 
            d="M100 70 Q85 85 83 105 Q82 120 95 130 Q110 135 120 125" 
            stroke="url(#purplePinkGradient)" 
            strokeWidth="4" 
            strokeLinecap="round"
            fill="none"
            opacity="0.8"
          />
          <path 
            d="M105 75 Q115 85 117 100 Q118 112 110 120 Q100 125 92 120" 
            stroke="url(#purplePinkGradient)" 
            strokeWidth="3.5" 
            strokeLinecap="round"
            fill="none"
            opacity="0.75"
          />
        </g>

        {/* Scattered geometric particles */}
        <g className="particles">
          {/* Cyan particles top right */}
          <polygon points="155,65 160,70 155,75" fill="#00E5FF" opacity="0.8" />
          <rect x="145" y="50" width="5" height="5" fill="#00E5FF" opacity="0.7" transform="rotate(45 147.5 52.5)" />
          <circle cx="165" cy="85" r="2.5" fill="#00E5FF" opacity="0.8" />
          
          {/* Orange particles right */}
          <polygon points="170,100 175,105 170,110" fill="#FF8A65" opacity="0.8" />
          <rect x="165" y="120" width="4" height="4" fill="#FF6B47" opacity="0.7" />
          <circle cx="172" cy="135" r="2" fill="#FF8A65" opacity="0.8" />
          
          {/* Pink/Magenta particles bottom */}
          <polygon points="145,165 150,170 145,175" fill="#FF6B9D" opacity="0.8" />
          <circle cx="130" cy="175" r="2.5" fill="#E91E63" opacity="0.8" />
          <rect x="110" y="172" width="4" height="4" fill="#FF6B9D" opacity="0.7" transform="rotate(45 112 174)" />
          
          {/* Purple particles left bottom */}
          <polygon points="70,155 75,160 70,165" fill="#9C27B0" opacity="0.8" />
          <circle cx="60" cy="140" r="2" fill="#9C27B0" opacity="0.8" />
          
          {/* Cyan particles left */}
          <rect x="55" y="115" width="5" height="5" fill="#00E5FF" opacity="0.7" transform="rotate(45 57.5 117.5)" />
          <polygon points="45,95 50,100 45,105" fill="#00E5FF" opacity="0.8" />
          <circle cx="50" cy="75" r="2.5" fill="#00E5FF" opacity="0.8" />
          
          {/* Orange particles top left */}
          <circle cx="65" cy="55" r="2" fill="#FF8A65" opacity="0.8" />
          <rect x="75" y="45" width="4" height="4" fill="#FF6B47" opacity="0.7" />
        </g>

        {/* Gradients */}
        <defs>
          <linearGradient id="cyanGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00E5FF" />
            <stop offset="100%" stopColor="#00B8D4" />
          </linearGradient>
          
          <linearGradient id="coralOrangeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FF8A65" />
            <stop offset="50%" stopColor="#FF6B47" />
            <stop offset="100%" stopColor="#FF5722" />
          </linearGradient>
          
          <linearGradient id="pinkMagentaGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FF6B9D" />
            <stop offset="50%" stopColor="#E91E63" />
            <stop offset="100%" stopColor="#C2185B" />
          </linearGradient>
          
          <linearGradient id="cyanBlueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00E5FF" />
            <stop offset="50%" stopColor="#00B0FF" />
            <stop offset="100%" stopColor="#1A73E8" />
          </linearGradient>
          
          <linearGradient id="purplePinkGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#9C27B0" />
            <stop offset="50%" stopColor="#E91E63" />
            <stop offset="100%" stopColor="#FF6B9D" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
};

export default MiraiLogo;

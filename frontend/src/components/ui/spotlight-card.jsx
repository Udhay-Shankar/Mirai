import React, { useRef, useState } from 'react';

const glowColors = {
  blue: 'rgba(59, 130, 246, 0.5)',
  purple: 'rgba(168, 85, 247, 0.5)',
  green: 'rgba(34, 197, 94, 0.5)',
  red: 'rgba(239, 68, 68, 0.5)',
  orange: 'rgba(249, 115, 22, 0.5)',
  cyan: 'rgba(6, 182, 212, 0.5)',
};

const sizePresets = {
  sm: { width: '250px', height: '200px' },
  md: { width: '350px', height: '250px' },
  lg: { width: '450px', height: '300px' },
};

export const SpotlightCard = ({
  children,
  className = '',
  glowColor = 'blue',
  size = 'md',
  width,
  height,
  customSize = false,
  style = {},
  ...props
}) => {
  const cardRef = useRef(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e) => {
    if (!cardRef.current) return;
    
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setMousePosition({ x, y });
  };

  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);

  const cardSize = customSize
    ? { width, height }
    : sizePresets[size];

  const selectedGlowColor = glowColors[glowColor] || glowColors.blue;

  return (
    <div
      ref={cardRef}
      className={`spotlight-card relative overflow-hidden rounded-xl border border-white/10 bg-black/40 backdrop-blur-sm transition-all duration-300 ${className}`}
      style={{
        width: cardSize.width,
        height: cardSize.height,
        ...style,
      }}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      {...props}
    >
      {/* Spotlight effect */}
      {isHovered && (
        <div
          className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300"
          style={{
            opacity: isHovered ? 1 : 0,
            background: `radial-gradient(600px circle at ${mousePosition.x}px ${mousePosition.y}px, ${selectedGlowColor}, transparent 40%)`,
          }}
        />
      )}

      {/* Border glow */}
      <div
        className="absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300"
        style={{
          opacity: isHovered ? 0.5 : 0,
          background: `radial-gradient(800px circle at ${mousePosition.x}px ${mousePosition.y}px, ${selectedGlowColor}, transparent 40%)`,
          maskImage: 'linear-gradient(black, black) content-box, linear-gradient(black, black)',
          maskComposite: 'exclude',
          WebkitMaskComposite: 'xor',
          padding: '1px',
        }}
      />

      {/* Content */}
      <div className="relative z-10 h-full w-full p-6">
        {children}
      </div>
    </div>
  );
};

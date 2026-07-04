import React from 'react';
import { motion } from 'framer-motion';

interface LogoProps {
  className?: string;
  size?: 'small' | 'medium' | 'large';
}

const Logo: React.FC<LogoProps> = ({ className = '', size = 'medium' }) => {
  const sizeClasses = {
    small: 'h-8',
    medium: 'h-12',
    large: 'h-20',
  };

  return (
    <motion.div 
      className={`flex items-center ${className}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Placeholder for actual logo - replace with actual SVG or image when available */}
      <div className={`${sizeClasses[size]} aspect-auto flex items-center justify-center`}>
        <div className="text-brand-primary font-heading font-bold">
          <span className="text-brand-secondary">Throwing</span> Starfish Studios
        </div>
      </div>
    </motion.div>
  );
};

export default Logo; 
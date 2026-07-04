import React from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';

interface AnimatedCursorProps {
  initialPosition?: { x: number; y: number };
  targetPosition: { x: number; y: number };
  onClick?: boolean;
  delay?: number;
  duration?: number;
  onAnimationComplete?: () => void;
}

const AnimatedCursor: React.FC<AnimatedCursorProps> = ({
  initialPosition = { x: -100, y: 50 },
  targetPosition,
  onClick = false,
  delay = 0.5,
  duration = 1.5,
  onAnimationComplete
}) => {
  // Check for reduced motion preference
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
  
  // If user prefers reduced motion, don't show the cursor
  if (prefersReducedMotion) {
    return null;
  }

  return (
    <motion.div
      className="absolute pointer-events-none z-50"
      initial={{ 
        x: initialPosition.x, 
        y: initialPosition.y,
        opacity: 0 
      }}
      animate={{ 
        x: targetPosition.x, 
        y: targetPosition.y,
        opacity: 1,
        transition: {
          x: { delay, duration, type: "spring", stiffness: 100, damping: 15 },
          y: { delay, duration, type: "spring", stiffness: 100, damping: 15 },
          opacity: { delay: delay - 0.2, duration: 0.3 }
        }
      }}
      onAnimationComplete={onAnimationComplete}
    >
      <Image 
        src={onClick ? "/images/cursor/cursor-click.svg" : "/images/cursor/cursor.svg"} 
        alt="Cursor" 
        width={32} 
        height={32}
        priority
      />
    </motion.div>
  );
};

export default AnimatedCursor; 
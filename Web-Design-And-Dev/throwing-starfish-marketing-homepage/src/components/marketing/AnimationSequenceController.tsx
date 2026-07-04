import React, { useState, useEffect } from 'react';
import { useInView } from 'framer-motion';

// This component will be used to control the animation sequence
// It will be used by each section to determine when to start its animation
// based on the previous section's animation completion

interface AnimationSequenceControllerProps {
  id: string;
  children: React.ReactNode;
  onInView?: () => void;
  threshold?: number;
}

export const useAnimationSequence = (id: string, dependencies: React.DependencyList = []) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  
  const startAnimation = () => {
    setIsAnimating(true);
  };
  
  const completeAnimation = () => {
    setIsAnimating(false);
    setIsComplete(true);
  };
  
  // Reset animation state when dependencies change
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    setIsAnimating(false);
    setIsComplete(false);
  }, [id, ...dependencies]);
  
  return {
    id,
    isAnimating,
    isComplete,
    startAnimation,
    completeAnimation
  };
};

const AnimationSequenceController: React.FC<AnimationSequenceControllerProps> = ({
  id,
  children,
  onInView,
  threshold = 0.5
}) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: false, amount: threshold });
  
  useEffect(() => {
    if (isInView && onInView) {
      onInView();
    }
  }, [isInView, onInView]);
  
  return (
    <div ref={ref} id={id} className="relative">
      {children}
    </div>
  );
};

export default AnimationSequenceController; 
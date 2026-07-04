import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';

// Words to cycle through
const PAIN_POINT_WORDS = ['unclear', 'lonely', 'exhausting', 'scary'];
const WORD_CHANGE_INTERVAL = 1500; // 1.5 seconds

const PainPointsSection: React.FC = () => {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'pain-points',
    'section_pain_points_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_pain_points_animation');
  
  // Word cycling effect
  useEffect(() => {
    if (!isVisible) return;
    
    const interval = setInterval(() => {
      setCurrentWordIndex((prevIndex) => 
        (prevIndex + 1) % PAIN_POINT_WORDS.length
      );
    }, WORD_CHANGE_INTERVAL);
    
    return () => clearInterval(interval);
  }, [isVisible]);
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_pain_points_container', {
    initial: { opacity: 0, y: 50 },
    whileInView: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6 }
    },
    viewport: { once: true, amount: 0.3 },
    onViewportEnter: () => setIsVisible(true)
  });
  
  // Reduced motion alternative
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
  
  return (
    <section 
      id="pain-points"
      ref={sectionRef}
      className="py-24 px-4 bg-white"
      data-testid="pain-points-section"
    >
      <motion.div
        className="max-w-4xl mx-auto text-center"
        {...containerProps}
      >
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-8">
          <span className="mr-2">Running a small business can be</span>
          
          {prefersReducedMotion ? (
            // Static alternative for reduced motion preference
            <span className="text-blue-500">challenging</span>
          ) : (
            // Animated words for standard motion preference
            <AnimatePresence mode="wait">
              <motion.span
                key={currentWordIndex}
                className="inline-block text-blue-500"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                {PAIN_POINT_WORDS[currentWordIndex]}
              </motion.span>
            </AnimatePresence>
          )}
        </h2>
      </motion.div>
    </section>
  );
};

export default PainPointsSection; 
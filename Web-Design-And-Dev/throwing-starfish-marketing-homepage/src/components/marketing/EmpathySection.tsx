import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';

const EmpathySection: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'empathy',
    'section_empathy_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_empathy_animation');
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_empathy_container', {
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
  
  // Text emphasis animation variants
  const textVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.4, delay: 0.2 }
    }
  };
  
  const emphasisVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { 
        duration: 0.5, 
        delay: 0.4,
        type: "spring",
        stiffness: 100
      }
    }
  };
  
  return (
    <section 
      id="empathy"
      ref={sectionRef}
      className="py-24 px-4 bg-gray-50"
      data-testid="empathy-section"
    >
      <motion.div
        className="max-w-4xl mx-auto text-center"
        {...containerProps}
      >
        {prefersReducedMotion ? (
          // Static version for reduced motion preference
          <p className="text-2xl md:text-3xl lg:text-4xl font-medium">
            You already know that, and you're still doing it. 
            <span className="block mt-4 text-blue-600 font-bold">
              That's the reason I work with small business.
            </span>
          </p>
        ) : (
          // Animated version with emphasis
          <motion.div
            initial="hidden"
            animate={isVisible ? "visible" : "hidden"}
          >
            <motion.p 
              className="text-2xl md:text-3xl lg:text-4xl font-medium"
              variants={textVariants}
            >
              You already know that, and you're still doing it.
            </motion.p>
            
            <motion.p
              className="mt-4 text-2xl md:text-3xl lg:text-4xl text-blue-600 font-bold"
              variants={emphasisVariants}
            >
              That's the reason I work with small business.
            </motion.p>
          </motion.div>
        )}
      </motion.div>
    </section>
  );
};

export default EmpathySection; 
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';

const ValuePropositionSection: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'value-proposition',
    'section_value_proposition_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_value_proposition_animation');
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_value_proposition_container', {
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
    hidden: { opacity: 0, scale: 0.95 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { 
        duration: 0.5, 
        delay: 0.2,
        type: "spring",
        stiffness: 100
      }
    }
  };
  
  return (
    <section 
      id="value-proposition"
      ref={sectionRef}
      className="py-24 px-4 bg-white"
      data-testid="value-proposition-section"
    >
      <motion.div
        className="max-w-4xl mx-auto text-center"
        {...containerProps}
      >
        {prefersReducedMotion ? (
          // Static version for reduced motion preference
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-black">
            Goal-oriented marketing <span className="text-yellow-400">gets results</span>
          </h2>
        ) : (
          // Animated version with emphasis
          <motion.div
            initial="hidden"
            animate={isVisible ? "visible" : "hidden"}
          >
            <motion.h2 
              className="text-3xl md:text-4xl lg:text-5xl font-bold text-black"
              variants={textVariants}
            >
              Goal-oriented marketing{" "}
              <motion.span 
                className="text-yellow-400"
                initial={{ opacity: 0, y: 10 }}
                animate={{ 
                  opacity: 1, 
                  y: 0,
                  transition: { 
                    delay: 0.5, 
                    duration: 0.4,
                    type: "spring"
                  }
                }}
              >
                gets results
              </motion.span>
            </motion.h2>
          </motion.div>
        )}
      </motion.div>
    </section>
  );
};

export default ValuePropositionSection; 
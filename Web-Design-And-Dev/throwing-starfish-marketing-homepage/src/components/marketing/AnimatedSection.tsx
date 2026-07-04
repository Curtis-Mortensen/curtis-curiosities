import React from 'react';
import { motion } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';

interface AnimatedSectionProps {
  id: string;
  title: string;
  children: React.ReactNode;
  delay?: number;
}

const AnimatedSection: React.FC<AnimatedSectionProps> = ({
  id,
  title,
  children,
  delay = 0,
}) => {
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    id,
    `section_${id}_visible`
  );
  
  // Track the animation lifecycle
  useTrackAnimation(`section_${id}_animation`);
  
  // Define animation variants
  const containerVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        delay,
        staggerChildren: 0.1,
      },
    },
  };
  
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
      },
    },
  };
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps(`section_${id}_container`, {
    variants: containerVariants,
    initial: 'hidden',
    whileInView: 'visible',
    viewport: { once: true, amount: 0.3 },
  });
  
  return (
    <section 
      id={id}
      ref={sectionRef}
      className="py-16 px-4"
      data-testid={id}
    >
      <motion.div
        className="max-w-6xl mx-auto"
        {...containerProps}
      >
        <motion.h2 
          className="text-3xl font-bold mb-8 text-center"
          variants={itemVariants}
        >
          {title}
        </motion.h2>
        
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-8"
          variants={itemVariants}
        >
          {children}
        </motion.div>
      </motion.div>
    </section>
  );
};

export default AnimatedSection; 
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';
import AnimatedCursor from './AnimatedCursor';
import AnimationSequenceController, { useAnimationSequence } from './AnimationSequenceController';

const LearnMoreSection: React.FC = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [showClickCursor, setShowClickCursor] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  
  // Animation sequence
  const animation = useAnimationSequence('learn-more-animation');
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'learn-more',
    'section_learn_more_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_learn_more_animation');
  
  // Reduced motion alternative
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_learn_more_container', {
    initial: { opacity: 0, y: 50 },
    whileInView: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6 }
    },
    viewport: { once: true, amount: 0.3 },
    onViewportEnter: () => {
      // Animation will be controlled by the sequence controller
    }
  });
  
  // Dropdown animation variants
  const dropdownVariants = {
    closed: { 
      height: 0,
      opacity: 0,
      transition: {
        duration: 0.4,
        ease: "easeInOut"
      }
    },
    open: { 
      height: "auto",
      opacity: 1,
      transition: {
        duration: 0.4,
        ease: "easeInOut"
      }
    }
  };
  
  // Calculate cursor target position
  const getCursorTargetPosition = () => {
    if (!dropdownRef.current) return { x: 0, y: 0 };
    
    const dropdownRect = dropdownRef.current.getBoundingClientRect();
    return {
      x: dropdownRect.left + 20, // Left side of dropdown plus offset
      y: dropdownRect.top + 20   // Top of dropdown plus offset
    };
  };
  
  // Handle cursor animation complete
  const handleCursorAnimationComplete = () => {
    // Show click cursor
    setShowClickCursor(true);
    
    // Simulate dropdown click after a short delay
    setTimeout(() => {
      setIsDropdownOpen(true);
      
      // Complete animation sequence after dropdown opens
      setTimeout(() => {
        animation.completeAnimation();
      }, 800);
    }, 300);
  };
  
  // Toggle dropdown manually
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };
  
  // Start animation when previous section is complete
  useEffect(() => {
    const startAnimationOnScroll = () => {
      const element = document.getElementById('learn-more');
      if (!element) return;
      
      const rect = element.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
      
      if (isVisible) {
        animation.startAnimation();
        window.removeEventListener('scroll', startAnimationOnScroll);
      }
    };
    
    window.addEventListener('scroll', startAnimationOnScroll);
    return () => window.removeEventListener('scroll', startAnimationOnScroll);
  }, [animation]);
  
  return (
    <AnimationSequenceController 
      id="learn-more"
      onInView={() => {
        // Animation will start when section is in view and previous animation is complete
      }}
    >
      <section 
        ref={sectionRef}
        className="py-24 px-4 bg-gray-50"
        data-testid="learn-more-section"
      >
        <motion.div
          className="max-w-4xl mx-auto"
          {...containerProps}
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Learn More About the Brand
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Discover the story behind our mission and values
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-lg shadow-sm">
            <div className="flex flex-col items-center">
              <p className="text-gray-600 mb-8 max-w-2xl text-center">
                This demonstration shows a cursor animation that opens a dropdown menu to reveal more information.
              </p>
              
              <div className="w-full max-w-2xl mx-auto">
                {/* Dropdown header */}
                <div 
                  ref={dropdownRef}
                  className="bg-gray-100 p-4 rounded-t-lg cursor-pointer flex justify-between items-center"
                  onClick={toggleDropdown}
                  data-testid="dropdown-header"
                >
                  <h3 className="text-xl font-semibold">Our Mission</h3>
                  <svg 
                    className={`w-5 h-5 transform transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24" 
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
                
                {/* Dropdown content */}
                <AnimatePresence>
                  {isDropdownOpen && (
                    <motion.div
                      className="bg-white border border-gray-200 border-t-0 p-4 rounded-b-lg overflow-hidden"
                      variants={dropdownVariants}
                      initial="closed"
                      animate="open"
                      exit="closed"
                      data-testid="dropdown-content"
                    >
                      <p className="mb-4">
                        Our mission is to empower small businesses with effective marketing strategies that drive real results. We believe that every small business deserves access to high-quality marketing services that are tailored to their unique needs and goals.
                      </p>
                      <p>
                        We work closely with our clients to understand their business, their customers, and their objectives. This allows us to create customized marketing solutions that help them reach their target audience, build brand awareness, and ultimately grow their business.
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {/* Animated cursor */}
                {!prefersReducedMotion && animation.isAnimating && (
                  <AnimatedCursor
                    initialPosition={{ x: -150, y: 50 }}
                    targetPosition={getCursorTargetPosition()}
                    onClick={showClickCursor}
                    delay={0.5}
                    duration={1.5}
                    onAnimationComplete={handleCursorAnimationComplete}
                  />
                )}
              </div>
              
              {prefersReducedMotion && (
                <p className="text-sm text-gray-500 mt-4">
                  Note: Cursor animation is disabled due to reduced motion preference.
                </p>
              )}
            </div>
          </div>
        </motion.div>
      </section>
    </AnimationSequenceController>
  );
};

export default LearnMoreSection; 
import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';
import AnimatedCursor from './AnimatedCursor';
import AnimationSequenceController, { useAnimationSequence } from './AnimationSequenceController';

const BuyProductSection: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [showClickCursor, setShowClickCursor] = useState(false);
  const [buttonClicked, setButtonClicked] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  
  // Animation sequence
  const animation = useAnimationSequence('buy-product-animation');
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'buy-product',
    'section_buy_product_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_buy_product_animation');
  
  // Reduced motion alternative
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_buy_product_container', {
    initial: { opacity: 0, y: 50 },
    whileInView: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6 }
    },
    viewport: { once: true, amount: 0.3 },
    onViewportEnter: () => {
      setIsVisible(true);
      // Start animation sequence after a delay
      setTimeout(() => {
        animation.startAnimation();
      }, 1000);
    }
  });
  
  // Button animation variants
  const buttonVariants = {
    initial: { scale: 1 },
    hover: { 
      scale: 1.05,
      backgroundColor: "#fde047", // gold color
      transition: { duration: 0.3 }
    },
    clicked: {
      scale: 0.95,
      backgroundColor: "#fde047",
      transition: { duration: 0.2 }
    }
  };

  // Calculate cursor target position
  const getCursorTargetPosition = () => {
    if (!buttonRef.current) return { x: 0, y: 0 };
    
    const buttonRect = buttonRef.current.getBoundingClientRect();
    return {
      x: buttonRect.left + buttonRect.width / 2 - 16, // Center of button minus half cursor width
      y: buttonRect.top + buttonRect.height / 2 - 16  // Center of button minus half cursor height
    };
  };

  // Handle cursor animation complete
  const handleCursorAnimationComplete = () => {
    // Show click cursor
    setShowClickCursor(true);
    
    // Simulate button click after a short delay
    setTimeout(() => {
      setButtonClicked(true);
      
      // Complete animation sequence after button click
      setTimeout(() => {
        animation.completeAnimation();
      }, 500);
    }, 300);
  };
  
  return (
    <AnimationSequenceController 
      id="buy-product"
      onInView={() => {
        // Animation will start when section is in view and previous animation is complete
      }}
    >
      <section 
        ref={sectionRef}
        className="py-24 px-4 bg-white"
        data-testid="buy-product-section"
      >
        <motion.div
          className="max-w-4xl mx-auto"
          {...containerProps}
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Interactive Elements
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Explore our interactive elements that enhance user engagement
            </p>
          </div>
          
          <div className="bg-gray-50 p-8 rounded-lg shadow-sm">
            <h3 className="text-2xl font-bold mb-6 text-center">
              Buy the Product
            </h3>
            
            <div className="flex flex-col items-center">
              <p className="text-gray-600 mb-8 max-w-2xl text-center">
                This demonstration shows a cursor animation that guides users toward the call-to-action button.
              </p>
              
              <div className="relative inline-block">
                {/* Button */}
                <motion.button
                  ref={buttonRef}
                  className="btn-primary bg-blue-600 hover:bg-yellow-400 hover:text-black text-white font-bold py-3 px-8 rounded-lg shadow-lg transition-all duration-300"
                  variants={buttonVariants}
                  initial="initial"
                  animate={buttonClicked ? "clicked" : "initial"}
                  whileHover="hover"
                  data-testid="buy-product-button"
                >
                  Buy Now
                </motion.button>
                
                {/* Animated cursor */}
                {!prefersReducedMotion && isVisible && animation.isAnimating && (
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

export default BuyProductSection; 
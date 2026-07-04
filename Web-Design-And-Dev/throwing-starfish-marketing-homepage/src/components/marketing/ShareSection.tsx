import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';
import createTrackedMotionProps from '../../utils/motionAnalytics';
import AnimatedCursor from './AnimatedCursor';
import AnimationSequenceController, { useAnimationSequence } from './AnimationSequenceController';

const ShareSection: React.FC = () => {
  const [activeButton, setActiveButton] = useState<string | null>(null);
  const [showClickCursor, setShowClickCursor] = useState(false);
  const [currentButtonIndex, setCurrentButtonIndex] = useState(0);
  const socialButtonsRef = useRef<(HTMLAnchorElement | null)[]>([]);
  
  // Animation sequence
  const animation = useAnimationSequence('share-animation');
  
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'share',
    'section_share_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_share_animation');
  
  // Reduced motion alternative
  const prefersReducedMotion = 
    typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
  
  // Create tracked motion props
  const containerProps = createTrackedMotionProps('section_share_container', {
    initial: { opacity: 0, y: 50 },
    whileInView: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6 }
    },
    viewport: { once: true, amount: 0.3 }
  });
  
  // Social media buttons
  const socialButtons = [
    { id: 'facebook', label: 'Facebook' },
    { id: 'instagram', label: 'Instagram' },
    { id: 'twitter', label: 'Twitter' },
    { id: 'email', label: 'Email' }
  ];
  
  // Calculate cursor target position
  const getCursorTargetPosition = () => {
    if (!socialButtonsRef.current[currentButtonIndex]) return { x: 0, y: 0 };
    
    const buttonRect = socialButtonsRef.current[currentButtonIndex]?.getBoundingClientRect();
    if (!buttonRect) return { x: 0, y: 0 };
    
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
      setActiveButton(socialButtons[currentButtonIndex].id);
      
      // Move to next button or complete animation
      setTimeout(() => {
        if (currentButtonIndex < socialButtons.length - 1) {
          setShowClickCursor(false);
          setCurrentButtonIndex(currentButtonIndex + 1);
        } else {
          // All buttons clicked, complete animation
          animation.completeAnimation();
        }
      }, 500);
    }, 300);
  };
  
  // Start animation when previous section is complete
  useEffect(() => {
    const startAnimationOnScroll = () => {
      const element = document.getElementById('share');
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
      id="share"
      onInView={() => {
        // Animation will start when section is in view and previous animation is complete
      }}
    >
      <section 
        ref={sectionRef}
        className="py-24 px-4 bg-white"
        data-testid="share-section"
      >
        <motion.div 
          className="max-w-4xl mx-auto"
          {...containerProps}
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Share With Family and Friends
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              If you find our services valuable, please share with others who might benefit. Word of mouth is our best marketing tool.
            </p>
          </div>
          
          <div className="bg-gray-50 p-8 rounded-lg shadow-sm">
            <div className="flex flex-col items-center">
              <p className="text-gray-600 mb-8 max-w-2xl text-center">
                This demonstration shows a cursor animation that clicks on social sharing buttons.
              </p>
              
              <div className="flex flex-wrap justify-center gap-6 relative">
                {socialButtons.map((button, index) => (
                  <a 
                    key={button.id}
                    ref={(el: HTMLAnchorElement | null) => {
                      socialButtonsRef.current[index] = el;
                    }}
                    href="#" 
                    className="flex flex-col items-center"
                    aria-label={`Share on ${button.label}`}
                    data-testid={`${button.id}-share`}
                  >
                    <motion.div 
                      className={`w-12 h-12 flex items-center justify-center rounded-full shadow-sm mb-2 transition-colors ${
                        activeButton === button.id 
                          ? 'bg-blue-500 text-white' 
                          : 'bg-white text-gray-600'
                      }`}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {button.id === 'facebook' && (
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                          <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                        </svg>
                      )}
                      {button.id === 'instagram' && (
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                          <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                        </svg>
                      )}
                      {button.id === 'twitter' && (
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                        </svg>
                      )}
                      {button.id === 'email' && (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                        </svg>
                      )}
                    </motion.div>
                    <span className="text-sm text-gray-600">{button.label}</span>
                  </a>
                ))}
                
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

export default ShareSection; 
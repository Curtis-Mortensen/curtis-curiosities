import { useRef, useEffect, RefObject } from 'react';
import { AnimationControls } from 'framer-motion';

// Function to track analytics events
const trackEvent = (eventName: string, properties?: Record<string, unknown>): void => {
  // In a real implementation, this would send data to an analytics service
  console.log(`[Analytics] ${eventName}`, properties);
};

/**
 * Hook to track when an element becomes visible in the viewport
 * @param elementId - The ID of the element to track
 * @param eventName - The name of the event to track
 * @returns A ref to attach to the element
 */
export const useTrackElementVisibility = (
  elementId: string,
  eventName: string
): RefObject<HTMLElement> => {
  const ref = useRef<HTMLElement>(null);
  
  useEffect(() => {
    if (!ref.current) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Track when element becomes visible
            trackEvent(eventName, {
              elementId,
              visible: true,
              timestamp: new Date().toISOString(),
            });
            
            // Disconnect after first visibility
            observer.disconnect();
          }
        });
      },
      { threshold: 0.1 }
    );
    
    // Start observing the element
    observer.observe(ref.current);
    
    // Cleanup function
    return () => {
      observer.disconnect();
    };
  }, [elementId, eventName]);
  
  return ref;
};

/**
 * Hook to track animation lifecycle events
 * @param animationName - The name of the animation to track
 * @param controls - Optional animation controls
 */
export const useTrackAnimation = (
  animationName: string,
  controls?: AnimationControls
): void => {
  useEffect(() => {
    trackEvent(`${animationName}_init`, {
      timestamp: new Date().toISOString(),
      hasControls: !!controls,
    });
    
    return () => {
      trackEvent(`${animationName}_cleanup`, {
        timestamp: new Date().toISOString(),
      });
    };
  }, [animationName, controls]);
}; 
import { 
  MotionProps, 
  AnimationDefinition 
} from 'framer-motion';

// Function to track animation events
export const trackAnimationEvent = (
  eventName: string,
  properties?: Record<string, unknown>
): void => {
  // In a real implementation, this would send data to an analytics service
  console.log(`[Analytics] ${eventName}`, properties);
};

// Create motion props with tracking
export const createTrackedMotionProps = (
  componentName: string,
  props: MotionProps
): MotionProps & { 'data-analytics-component': string } => {
  // Create a copy of the props to avoid mutating the original
  const trackedProps = { 
    ...props,
    'data-analytics-component': componentName 
  };
  
  // Track animation start
  const originalOnAnimationStart = props.onAnimationStart;
  trackedProps.onAnimationStart = (definition: AnimationDefinition) => {
    trackAnimationEvent(`${componentName}_animation_start`, {
      definition: typeof definition === 'string' ? definition : 'complex',
    });
    
    // Call the original handler if it exists
    if (originalOnAnimationStart) {
      originalOnAnimationStart(definition);
    }
  };
  
  // Track animation complete
  const originalOnAnimationComplete = props.onAnimationComplete;
  trackedProps.onAnimationComplete = (definition: AnimationDefinition) => {
    trackAnimationEvent(`${componentName}_animation_complete`, {
      definition: typeof definition === 'string' ? definition : 'complex',
    });
    
    // Call the original handler if it exists
    if (originalOnAnimationComplete) {
      originalOnAnimationComplete(definition);
    }
  };
  
  return trackedProps;
};

export default createTrackedMotionProps; 
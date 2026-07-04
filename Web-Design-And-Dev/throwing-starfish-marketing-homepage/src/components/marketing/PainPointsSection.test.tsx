import React from 'react';
import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import PainPointsSection from './PainPointsSection';

// Mock the analytics hooks
jest.mock('../../hooks/useAnalytics', () => ({
  useTrackElementVisibility: () => React.createRef(),
  useTrackAnimation: jest.fn(),
}));

// Mock the motion analytics utility
jest.mock('../../utils/motionAnalytics', () => ({
  __esModule: true,
  default: jest.fn().mockImplementation((_, props) => props),
}));

// Mock the framer-motion
jest.mock('framer-motion', () => {
  const actual = jest.requireActual('framer-motion');
  return {
    ...actual,
    motion: {
      div: ({ children, ...props }: React.ComponentProps<'div'>) => (
        <div data-testmotion="div" {...props}>
          {children}
        </div>
      ),
      span: ({ children, ...props }: React.ComponentProps<'span'>) => (
        <span data-testmotion="span" {...props}>
          {children}
        </span>
      ),
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  };
});

describe('PainPointsSection', () => {
  beforeEach(() => {
    // Mock window.matchMedia
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
    
    // Reset timers
    jest.useFakeTimers();
  });
  
  afterEach(() => {
    jest.useRealTimers();
  });

  it('renders the static text correctly', () => {
    render(<PainPointsSection />);
    expect(screen.getByText(/Running a small business can be/i)).toBeInTheDocument();
  });

  it('shows the first pain point word initially', () => {
    render(<PainPointsSection />);
    
    // Trigger visibility
    act(() => {
      const props = screen.getByTestId('pain-points-section');
      const onViewportEnter = props.querySelector('[data-testmotion="div"]')?.onViewportEnter;
      if (onViewportEnter) onViewportEnter();
    });
    
    expect(screen.getByText('unclear')).toBeInTheDocument();
  });
  
  it('cycles through pain point words', () => {
    render(<PainPointsSection />);
    
    // Trigger visibility
    act(() => {
      const props = screen.getByTestId('pain-points-section');
      const onViewportEnter = props.querySelector('[data-testmotion="div"]')?.onViewportEnter;
      if (onViewportEnter) onViewportEnter();
    });
    
    // Check initial word
    expect(screen.getByText('unclear')).toBeInTheDocument();
    
    // Advance timer to next word
    act(() => {
      jest.advanceTimersByTime(1500);
    });
    
    // Check second word
    expect(screen.getByText('lonely')).toBeInTheDocument();
  });

  it('shows static text for reduced motion preference', () => {
    // Mock reduced motion preference
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation(query => ({
        matches: query === '(prefers-reduced-motion: reduce)',
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
    
    render(<PainPointsSection />);
    expect(screen.getByText('challenging')).toBeInTheDocument();
  });
}); 
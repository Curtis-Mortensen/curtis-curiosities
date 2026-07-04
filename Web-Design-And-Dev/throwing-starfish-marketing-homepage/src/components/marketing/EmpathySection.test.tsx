import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import EmpathySection from './EmpathySection';

// Mock the analytics hooks
jest.mock('../../hooks/useAnalytics', () => ({
  useTrackElementVisibility: jest.fn(() => React.createRef()),
  useTrackAnimation: jest.fn(),
}));

// Mock the motion analytics utilities
jest.mock('../../utils/motionAnalytics', () => ({
  __esModule: true,
  default: jest.fn((name, props) => ({
    ...props,
    'data-testid': name,
  })),
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
      p: ({ children, ...props }: React.ComponentProps<'p'>) => (
        <p data-testmotion="p" {...props}>
          {children}
        </p>
      ),
    },
  };
});

// Mock the window.matchMedia
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

describe('EmpathySection', () => {
  it('renders the section with correct ID and data attributes', () => {
    render(<EmpathySection />);
    
    const section = screen.getByTestId('empathy-section');
    expect(section).toBeInTheDocument();
    expect(section).toHaveAttribute('id', 'empathy');
  });
  
  it('renders the main text content', () => {
    render(<EmpathySection />);
    
    expect(screen.getByText("You already know that, and you're still doing it.")).toBeInTheDocument();
    expect(screen.getByText("That's the reason I work with small business.")).toBeInTheDocument();
  });
  
  it('applies motion props to the container', () => {
    render(<EmpathySection />);
    
    const container = screen.getByTestId('section_empathy_container');
    expect(container).toBeInTheDocument();
    expect(container).toHaveAttribute('data-testmotion', 'div');
  });
  
  it('renders static version when reduced motion is preferred', () => {
    // Mock the matchMedia to return reduced motion preference
    window.matchMedia = jest.fn().mockImplementation(query => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    }));
    
    render(<EmpathySection />);
    
    // In reduced motion mode, we should have a single paragraph with both texts
    const paragraph = screen.getByText(/You already know that, and you're still doing it./);
    expect(paragraph).toBeInTheDocument();
    expect(paragraph).not.toHaveAttribute('data-testmotion');
  });
}); 
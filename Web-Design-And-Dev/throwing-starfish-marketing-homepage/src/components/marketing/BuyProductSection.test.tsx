import React from 'react';
import { render, screen } from '@testing-library/react';
import BuyProductSection from './BuyProductSection';

// Mock the analytics hooks
jest.mock('../../hooks/useAnalytics', () => ({
  useTrackElementVisibility: jest.fn(() => React.createRef()),
  useTrackAnimation: jest.fn(),
}));

// Mock the motion analytics utility
jest.mock('../../utils/motionAnalytics', () => ({
  __esModule: true,
  default: jest.fn(() => ({
    initial: { opacity: 0 },
    whileInView: { opacity: 1 },
    viewport: { once: true },
  })),
}));

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

describe('BuyProductSection', () => {
  it('renders the section with correct heading', () => {
    render(<BuyProductSection />);
    
    const heading = screen.getByText('Interactive Elements');
    expect(heading).toBeInTheDocument();
    
    const subheading = screen.getByText('Buy the Product');
    expect(subheading).toBeInTheDocument();
  });
  
  it('renders the button with correct text', () => {
    render(<BuyProductSection />);
    
    const button = screen.getByTestId('buy-product-button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('Buy Now');
  });
  
  it('has the correct section ID', () => {
    render(<BuyProductSection />);
    
    const section = screen.getByTestId('buy-product-section');
    expect(section).toHaveAttribute('id', 'buy-product');
  });
  
  it('displays the demonstration description', () => {
    render(<BuyProductSection />);
    
    const description = screen.getByText('This demonstration shows a cursor animation that guides users toward the call-to-action button.');
    expect(description).toBeInTheDocument();
  });
  
  it('applies the correct styling to the button', () => {
    render(<BuyProductSection />);
    
    const button = screen.getByTestId('buy-product-button');
    expect(button).toHaveClass('btn-primary');
    expect(button).toHaveClass('bg-blue-600');
  });
  
  describe('with reduced motion preference', () => {
    beforeEach(() => {
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
    });
    
    it('does not render the cursor animation when reduced motion is preferred', () => {
      render(<BuyProductSection />);
      
      // The SVG cursor should not be in the document
      const svgElements = document.querySelectorAll('svg');
      expect(svgElements.length).toBe(0);
    });
    
    it('shows a note about disabled animation when reduced motion is preferred', () => {
      render(<BuyProductSection />);
      
      const note = screen.getByText('Note: Cursor animation is disabled due to reduced motion preference.');
      expect(note).toBeInTheDocument();
    });
  });
}); 
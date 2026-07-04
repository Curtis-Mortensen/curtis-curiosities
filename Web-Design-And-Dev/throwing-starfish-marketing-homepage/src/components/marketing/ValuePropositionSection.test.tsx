import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ValuePropositionSection from './ValuePropositionSection';

// Mock the IntersectionObserver
const mockIntersectionObserver = jest.fn();
mockIntersectionObserver.mockReturnValue({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
});
window.IntersectionObserver = mockIntersectionObserver;

// Mock the matchMedia function
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query: string) => ({
    matches: false, // Default to standard motion
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

describe('ValuePropositionSection', () => {
  it('renders the section with correct ID and test ID', () => {
    render(<ValuePropositionSection />);
    
    const section = screen.getByTestId('value-proposition-section');
    expect(section).toBeInTheDocument();
    expect(section.id).toBe('value-proposition');
  });
  
  it('displays the correct value proposition text', () => {
    render(<ValuePropositionSection />);
    
    expect(screen.getByText(/Goal-oriented marketing/i)).toBeInTheDocument();
    expect(screen.getByText(/gets results/i)).toBeInTheDocument();
  });
  
  it('renders with reduced motion when preference is set', () => {
    // Mock reduced motion preference
    window.matchMedia = jest.fn().mockImplementation((query: string) => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    }));
    
    render(<ValuePropositionSection />);
    
    // In reduced motion mode, the text should be rendered statically
    const heading = screen.getByRole('heading');
    expect(heading).toHaveTextContent('Goal-oriented marketing gets results');
  });
  
  it('has the correct styling for emphasis', () => {
    render(<ValuePropositionSection />);
    
    // Check that "gets results" has the emphasis styling
    const emphasisText = screen.getByText('gets results');
    expect(emphasisText).toHaveClass('text-yellow-400');
  });
}); 
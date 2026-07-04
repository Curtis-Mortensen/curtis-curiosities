import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LearnMoreSection from './LearnMoreSection';

// Mock the intersection observer
const mockIntersectionObserver = jest.fn();
mockIntersectionObserver.mockReturnValue({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
});
window.IntersectionObserver = mockIntersectionObserver;

// Mock the matchMedia for reduced motion
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

describe('LearnMoreSection', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the section with correct heading', () => {
    render(<LearnMoreSection />);
    
    expect(screen.getByTestId('learn-more-section')).toBeInTheDocument();
    expect(screen.getByText('Learn More')).toBeInTheDocument();
    expect(screen.getByText("You already know that, and you're still doing it. That's the reason I work with small business.")).toBeInTheDocument();
  });

  it('renders the dropdown trigger button', () => {
    render(<LearnMoreSection />);
    
    const triggerButton = screen.getByTestId('learn-more-dropdown-trigger');
    expect(triggerButton).toBeInTheDocument();
    expect(triggerButton).toHaveTextContent('Learn more about the Brand');
  });

  it('toggles dropdown when trigger is clicked', async () => {
    render(<LearnMoreSection />);
    
    // Initially dropdown should not be visible
    expect(screen.queryByTestId('learn-more-dropdown-content')).not.toBeInTheDocument();
    
    // Click the trigger button
    const triggerButton = screen.getByTestId('learn-more-dropdown-trigger');
    fireEvent.click(triggerButton);
    
    // Dropdown should now be visible
    await waitFor(() => {
      expect(screen.getByTestId('learn-more-dropdown-content')).toBeInTheDocument();
    });
    
    // Check dropdown content
    expect(screen.getByText('Our Approach')).toBeInTheDocument();
    expect(screen.getByText('Why Choose Us')).toBeInTheDocument();
    
    // Click again to close
    fireEvent.click(triggerButton);
    
    // Dropdown should be removed after animation
    await waitFor(() => {
      expect(screen.queryByTestId('learn-more-dropdown-content')).not.toBeInTheDocument();
    });
  });

  it('shows reduced motion alternative when preference is set', () => {
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
    
    render(<LearnMoreSection />);
    
    // Dropdown should be visible immediately for reduced motion users
    expect(screen.getByTestId('learn-more-dropdown-content')).toBeInTheDocument();
    
    // Should show reduced motion message
    expect(screen.getByText('Note: Dropdown animation is disabled due to reduced motion preference.')).toBeInTheDocument();
  });

  it('has proper accessibility attributes', () => {
    render(<LearnMoreSection />);
    
    const triggerButton = screen.getByTestId('learn-more-dropdown-trigger');
    
    // Check ARIA attributes
    expect(triggerButton).toHaveAttribute('aria-expanded', 'false');
    expect(triggerButton).toHaveAttribute('aria-controls', 'learn-more-dropdown');
    
    // Click to open
    fireEvent.click(triggerButton);
    
    // ARIA attributes should update
    expect(triggerButton).toHaveAttribute('aria-expanded', 'true');
    
    const dropdownContent = screen.getByTestId('learn-more-dropdown-content');
    expect(dropdownContent).toHaveAttribute('aria-hidden', 'false');
  });
}); 
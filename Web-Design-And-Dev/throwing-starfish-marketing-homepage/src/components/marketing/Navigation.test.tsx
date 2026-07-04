import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Navigation from './Navigation';

// Mock the IntersectionObserver
const mockIntersectionObserver = jest.fn();
mockIntersectionObserver.mockReturnValue({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
});
window.IntersectionObserver = mockIntersectionObserver;

// Mock useRouter
jest.mock('next/router', () => ({
  useRouter: () => ({
    pathname: '/',
  }),
}));

// Mock sections for testing
const mockSections = [
  { id: 'home', label: 'Home' },
  { id: 'services', label: 'Services' },
  { id: 'testimonials', label: 'Testimonials' },
  { id: 'about', label: 'About' },
];

describe('Navigation Component', () => {
  beforeEach(() => {
    // Mock scrollIntoView
    Element.prototype.scrollIntoView = jest.fn();
    
    // Mock getElementById
    document.getElementById = jest.fn().mockImplementation((id) => {
      return {
        id,
        scrollIntoView: jest.fn(),
      };
    });
  });

  it('renders navigation with all sections', () => {
    render(<Navigation sections={mockSections} />);
    
    // Check if all section links are rendered
    mockSections.forEach(section => {
      expect(screen.getByText(section.label)).toBeInTheDocument();
    });
  });

  it('shows mobile menu when hamburger is clicked', () => {
    render(<Navigation sections={mockSections} />);
    
    // Mobile menu should be hidden initially
    expect(screen.queryByRole('button', { name: /home/i })).not.toBeVisible();
    
    // Click hamburger button
    const hamburgerButton = screen.getByLabelText('Toggle navigation menu');
    fireEvent.click(hamburgerButton);
    
    // Mobile menu should be visible now
    expect(screen.getAllByText('Home')[1]).toBeVisible();
  });

  it('scrolls to section when link is clicked', () => {
    render(<Navigation sections={mockSections} />);
    
    // Click on a section link
    const servicesLink = screen.getByText('Services');
    fireEvent.click(servicesLink);
    
    // Check if getElementById was called with the correct id
    expect(document.getElementById).toHaveBeenCalledWith('services');
  });

  it('changes appearance on scroll', () => {
    render(<Navigation sections={mockSections} />);
    
    // Initially, nav should not have shadow
    const nav = screen.getByRole('navigation');
    expect(nav).toHaveClass('bg-transparent');
    
    // Simulate scroll
    fireEvent.scroll(window, { target: { scrollY: 100 } });
    
    // Nav should now have shadow class
    expect(nav).toHaveClass('bg-white shadow-md');
  });
}); 
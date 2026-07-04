import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Logo from '../Logo';
import Link from 'next/link';
import { useRouter } from 'next/router';

// Function to track analytics events (imported from useAnalytics)
const trackEvent = (eventName: string, properties?: Record<string, unknown>): void => {
  // In a real implementation, this would send data to an analytics service
  console.log(`[Analytics] ${eventName}`, properties);
};

interface NavigationProps {
  links: {
    href: string;
    label: string;
  }[];
}

const Navigation: React.FC<NavigationProps> = ({ links }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const router = useRouter();

  // Handle scroll
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  // Handle navigation click
  const handleNavClick = (href: string) => {
    setIsOpen(false);
    
    // Track navigation click for analytics
    trackEvent('navigation_click', {
      destination: href,
      timestamp: new Date().toISOString()
    });
  };

  // Track mobile menu interactions
  const toggleMobileMenu = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    
    trackEvent('mobile_menu_toggle', {
      isOpen: newState,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <motion.nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-md py-2' : 'bg-transparent py-4'
      }`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link href="/" onClick={() => handleNavClick('/')}>
            <Logo size="small" />
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            {links.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                onClick={() => handleNavClick(href)}
                className={`text-[#448ade] hover:text-[#fde047] transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-[#448ade] px-2 py-1 rounded ${
                  router.pathname === href ? 'text-[#fde047] font-semibold' : ''
                }`}
                aria-current={router.pathname === href ? 'page' : undefined}
              >
                {label}
              </Link>
            ))}
          </div>

          {/* Mobile Hamburger Button */}
          <button
            className="md:hidden text-[#448ade] hover:text-[#fde047] transition-colors"
            onClick={toggleMobileMenu}
            aria-expanded={isOpen}
            aria-controls="mobile-menu"
            aria-label="Toggle navigation menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              id="mobile-menu"
              className="md:hidden mt-4 bg-white rounded-lg shadow-lg overflow-hidden"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="py-2 px-4 flex flex-col space-y-4">
                {links.map(({ href, label }) => (
                  <Link
                    key={href}
                    href={href}
                    onClick={() => handleNavClick(href)}
                    className={`text-left text-[#448ade] hover:text-[#fde047] transition-colors py-2 ${
                      router.pathname === href ? 'text-[#fde047] font-semibold' : ''
                    }`}
                    aria-current={router.pathname === href ? 'page' : undefined}
                  >
                    {label}
                  </Link>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.nav>
  );
};

export default Navigation; 
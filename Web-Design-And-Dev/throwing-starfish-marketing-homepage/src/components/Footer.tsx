import React from 'react';
import Link from 'next/link';
import Logo from './Logo';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-brand-dark text-white py-8">
      <div className="container-custom">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <Logo size="small" className="mb-4" />
            <p className="text-sm opacity-80 mt-4">
              Throwing Starfish Studios combines marketing expertise with game development creativity.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/marketing" className="text-sm opacity-80 hover:opacity-100 transition-opacity">
                  Marketing Services
                </Link>
              </li>
              <li>
                <Link href="/games" className="text-sm opacity-80 hover:opacity-100 transition-opacity">
                  Game Studio
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-sm opacity-80 hover:opacity-100 transition-opacity">
                  About Us
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-bold mb-4">Contact</h3>
            <ul className="space-y-2">
              <li className="text-sm opacity-80">
                <span className="block">Email: info@throwingstarfish.com</span>
              </li>
              <li className="text-sm opacity-80">
                <span className="block">Location: Virtual Company</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm opacity-70">
            &copy; {currentYear} Throwing Starfish Studios. All rights reserved.
          </p>
          <div className="mt-4 md:mt-0">
            <ul className="flex space-x-4">
              <li>
                <a href="#" className="text-sm opacity-70 hover:opacity-100 transition-opacity">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-sm opacity-70 hover:opacity-100 transition-opacity">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
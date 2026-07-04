import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import PainPointsSection from '../components/marketing/PainPointsSection';
import EmpathySection from '../components/marketing/EmpathySection';
import ValuePropositionSection from '../components/marketing/ValuePropositionSection';
import BuyProductSection from '../components/marketing/BuyProductSection';
import LearnMoreSection from '../components/marketing/LearnMoreSection';
import ShareSection from '../components/marketing/ShareSection';
import FewerDollarsSection from '../components/marketing/FewerDollarsSection';
import ContactFormSection from '../components/marketing/ContactFormSection';
import Navigation from '../components/marketing/Navigation';
import Logo from '../components/Logo';

const MarketingPage: React.FC = () => {
  // Define navigation links
  const navLinks = [
    { href: '/marketing', label: 'Home' },
    { href: '/marketing/services', label: 'Services' },
    { href: '/marketing/testimonials', label: 'Testimonials' },
    { href: '/marketing/about', label: 'About' },
  ];

  return (
    <>
      <Head>
        <title>Marketing Services - Throwing Starfish Studios</title>
        <meta name="description" content="Goal-oriented marketing services for small businesses - Throwing Starfish Studios" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Navigation */}
      <Navigation links={navLinks} />

      <main className="min-h-screen bg-white pt-16">
        {/* Hero Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4 max-w-6xl">
            <motion.div 
              className="text-center mb-12"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Logo size="medium" className="mx-auto mb-6" />
              <h2 className="text-4xl md:text-5xl font-bold mb-6">Goal-Oriented Marketing</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Marketing that focuses on your business goals and delivers measurable results.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Marketing Conversion Flow */}
        <PainPointsSection />
        <EmpathySection />
        <ValuePropositionSection />
        <BuyProductSection />
        <LearnMoreSection />
        <ShareSection />
        <FewerDollarsSection />

        {/* Contact Form Section */}
        <ContactFormSection />

        {/* Call to Action - Removed as it's replaced by the contact form */}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <Logo size="small" />
            </div>
            <div className="flex flex-wrap gap-6">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-gray-400 hover:text-[#fde047] transition-colors"
                >
                  {link.label}
                </a>
              ))}
            </div>
          </div>
          <div className="border-t border-gray-800 mt-6 pt-6 text-center text-gray-400">
            <p>&copy; {new Date().getFullYear()} Throwing Starfish Studios. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
};

export default MarketingPage; 
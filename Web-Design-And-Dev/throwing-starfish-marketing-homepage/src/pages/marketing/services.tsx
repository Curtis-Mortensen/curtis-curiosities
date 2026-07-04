import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import Navigation from '../../components/marketing/Navigation';
import Logo from '../../components/Logo';

const ServicesPage: React.FC = () => {
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
        <title>Our Services - Throwing Starfish Studios</title>
        <meta name="description" content="Explore our range of marketing services - Throwing Starfish Studios" />
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
              <h1 className="text-4xl md:text-5xl font-bold mb-6">Our Marketing Services</h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Comprehensive marketing solutions tailored to your business goals.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Services Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
              {[
                {
                  title: 'Strategy Development',
                  description: 'Custom marketing strategies aligned with your business goals.',
                  icon: '🎯',
                  features: ['Market research', 'Competitor analysis', 'Target audience definition', 'Goal setting'],
                },
                {
                  title: 'Content Creation',
                  description: 'Engaging content that resonates with your target audience.',
                  icon: '✍️',
                  features: ['Blog posts', 'Social media content', 'Email campaigns', 'Video production'],
                },
                {
                  title: 'Analytics & Reporting',
                  description: 'Data-driven insights to optimize your marketing efforts.',
                  icon: '📊',
                  features: ['Performance tracking', 'ROI analysis', 'Monthly reporting', 'Optimization recommendations'],
                },
              ].map((service, index) => (
                <motion.div
                  key={index}
                  className="bg-gray-50 p-8 rounded-lg shadow-sm"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="text-4xl mb-4">{service.icon}</div>
                  <h3 className="text-xl font-bold mb-3">{service.title}</h3>
                  <p className="text-gray-600 mb-4">{service.description}</p>
                  <ul className="space-y-2">
                    {service.features.map((feature, i) => (
                      <li key={i} className="flex items-center">
                        <span className="text-[#448ade] mr-2">✓</span>
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>

            <div className="bg-gray-50 p-8 rounded-lg">
              <h2 className="text-2xl font-bold mb-6">Our Process</h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {[
                  { step: 1, title: 'Discovery', description: 'We learn about your business, goals, and challenges.' },
                  { step: 2, title: 'Strategy', description: 'We develop a customized marketing plan for your business.' },
                  { step: 3, title: 'Implementation', description: 'We execute the strategy with precision and creativity.' },
                  { step: 4, title: 'Optimization', description: 'We analyze results and refine our approach for maximum impact.' },
                ].map((process, index) => (
                  <motion.div
                    key={index}
                    className="text-center p-4"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <div className="w-12 h-12 bg-[#448ade] text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                      {process.step}
                    </div>
                    <h3 className="text-lg font-bold mb-2">{process.title}</h3>
                    <p className="text-gray-600">{process.description}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="py-16 bg-[#448ade] text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to get started?</h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Contact us today to discuss how our services can help your business grow.
            </p>
            <motion.button 
              className="bg-white text-[#448ade] hover:bg-[#fde047] hover:text-gray-800 px-8 py-3 rounded-md font-bold text-lg transition-colors duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Contact Us
            </motion.button>
          </div>
        </section>
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

export default ServicesPage; 
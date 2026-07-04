import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import Navigation from '../../components/marketing/Navigation';
import Logo from '../../components/Logo';

const TestimonialsPage: React.FC = () => {
  // Define navigation links
  const navLinks = [
    { href: '/marketing', label: 'Home' },
    { href: '/marketing/services', label: 'Services' },
    { href: '/marketing/testimonials', label: 'Testimonials' },
    { href: '/marketing/about', label: 'About' },
  ];

  // Testimonial data
  const testimonials = [
    {
      quote: "Working with Throwing Starfish Studios transformed our marketing approach. Their goal-oriented strategy helped us increase conversions by 35%.",
      author: "Sarah Johnson",
      company: "Bright Ideas Co.",
      image: "/placeholder-avatar.jpg",
      industry: "Technology",
    },
    {
      quote: "The team's data-driven approach and creative solutions made all the difference for our small business.",
      author: "Michael Chen",
      company: "Urban Cafe",
      image: "/placeholder-avatar.jpg",
      industry: "Food & Beverage",
    },
    {
      quote: "Their marketing expertise helped us reach new customers and grow our business in ways we never thought possible.",
      author: "Jessica Williams",
      company: "Wellness Center",
      image: "/placeholder-avatar.jpg",
      industry: "Health & Wellness",
    },
    {
      quote: "The ROI on our marketing campaigns has been exceptional since working with Throwing Starfish Studios.",
      author: "David Rodriguez",
      company: "Financial Solutions",
      image: "/placeholder-avatar.jpg",
      industry: "Finance",
    },
    {
      quote: "They took the time to understand our unique challenges and created a strategy that perfectly aligned with our goals.",
      author: "Emily Thompson",
      company: "Green Living",
      image: "/placeholder-avatar.jpg",
      industry: "Sustainability",
    },
    {
      quote: "Our online presence has never been stronger. We're reaching more customers and seeing real business growth.",
      author: "Robert Kim",
      company: "Digital Innovations",
      image: "/placeholder-avatar.jpg",
      industry: "Technology",
    },
  ];

  return (
    <>
      <Head>
        <title>Client Testimonials - Throwing Starfish Studios</title>
        <meta name="description" content="What our clients say about our marketing services - Throwing Starfish Studios" />
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
              <h1 className="text-4xl md:text-5xl font-bold mb-6">Client Testimonials</h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Don't just take our word for it. Here's what our clients have to say about working with us.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={index}
                  className="bg-gray-50 p-8 rounded-lg shadow-sm"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="flex items-center mb-6">
                    <div className="w-12 h-12 bg-[#448ade] rounded-full flex items-center justify-center text-white font-bold">
                      {testimonial.author.charAt(0)}
                    </div>
                    <div className="ml-4">
                      <p className="font-bold">{testimonial.author}</p>
                      <p className="text-gray-600">{testimonial.company}</p>
                      <p className="text-sm text-[#448ade]">{testimonial.industry}</p>
                    </div>
                  </div>
                  <p className="text-lg italic mb-4">"{testimonial.quote}"</p>
                  <div className="flex items-center">
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <svg key={i} xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Case Study Highlight */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center">Featured Case Study</h2>
            <div className="bg-white p-8 rounded-lg shadow-sm max-w-4xl mx-auto">
              <div className="flex flex-col md:flex-row gap-8">
                <div className="md:w-1/2">
                  <h3 className="text-2xl font-bold mb-4">Bright Ideas Co.</h3>
                  <p className="text-gray-600 mb-4">
                    Bright Ideas Co. came to us with a challenge: they needed to increase their online conversions and reach a wider audience.
                  </p>
                  <div className="mb-6">
                    <p className="font-bold mb-2">The Results:</p>
                    <ul className="space-y-2">
                      <li className="flex items-center">
                        <span className="text-[#448ade] mr-2">✓</span>
                        <span>35% increase in conversion rate</span>
                      </li>
                      <li className="flex items-center">
                        <span className="text-[#448ade] mr-2">✓</span>
                        <span>42% growth in organic traffic</span>
                      </li>
                      <li className="flex items-center">
                        <span className="text-[#448ade] mr-2">✓</span>
                        <span>28% reduction in customer acquisition cost</span>
                      </li>
                    </ul>
                  </div>
                  <motion.button 
                    className="bg-[#448ade] hover:bg-[#fde047] text-white hover:text-gray-800 px-6 py-2 rounded-md font-bold transition-colors duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Read Full Case Study
                  </motion.button>
                </div>
                <div className="md:w-1/2">
                  <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                    <p className="text-gray-500">Case Study Graph</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="py-16 bg-[#448ade] text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to join our success stories?</h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Let's work together to create a marketing strategy that gets results for your business.
            </p>
            <motion.button 
              className="bg-white text-[#448ade] hover:bg-[#fde047] hover:text-gray-800 px-8 py-3 rounded-md font-bold text-lg transition-colors duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Contact Us Today
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

export default TestimonialsPage; 
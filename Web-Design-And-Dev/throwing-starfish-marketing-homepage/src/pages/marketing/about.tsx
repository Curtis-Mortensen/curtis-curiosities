import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import Navigation from '../../components/marketing/Navigation';
import Logo from '../../components/Logo';

const AboutPage: React.FC = () => {
  // Define navigation links
  const navLinks = [
    { href: '/marketing', label: 'Home' },
    { href: '/marketing/services', label: 'Services' },
    { href: '/marketing/testimonials', label: 'Testimonials' },
    { href: '/marketing/about', label: 'About' },
  ];

  // Team members data
  const teamMembers = [
    {
      name: "Alex Johnson",
      role: "Founder & CEO",
      bio: "With over 15 years of marketing experience, Alex founded Throwing Starfish Studios with a mission to help small businesses achieve their goals.",
      image: "/placeholder-avatar.jpg",
    },
    {
      name: "Maya Patel",
      role: "Marketing Strategist",
      bio: "Maya specializes in developing data-driven marketing strategies that deliver measurable results for our clients.",
      image: "/placeholder-avatar.jpg",
    },
    {
      name: "David Lee",
      role: "Content Director",
      bio: "David leads our content team, creating engaging and effective content that resonates with target audiences.",
      image: "/placeholder-avatar.jpg",
    },
    {
      name: "Sarah Wilson",
      role: "Analytics Specialist",
      bio: "Sarah transforms data into actionable insights, helping our clients optimize their marketing efforts.",
      image: "/placeholder-avatar.jpg",
    },
  ];

  return (
    <>
      <Head>
        <title>About Us - Throwing Starfish Studios</title>
        <meta name="description" content="Learn about our team and our approach to marketing - Throwing Starfish Studios" />
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
              <h1 className="text-4xl md:text-5xl font-bold mb-6">About Throwing Starfish Studios</h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                We're a team of passionate marketers dedicated to making a difference for small businesses.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Our Story Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center gap-12">
              <motion.div
                className="md:w-1/2"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
              >
                <h2 className="text-3xl font-bold mb-6">Our Story</h2>
                <p className="text-lg text-gray-600 mb-6">
                  Throwing Starfish Studios was founded in 2020 with a simple mission: to help small businesses succeed through effective, goal-oriented marketing.
                </p>
                <p className="text-lg text-gray-600 mb-6">
                  Our name comes from the starfish story - a tale about making a difference one small action at a time. We believe that even small marketing efforts, when strategically implemented, can make a significant impact on a business.
                </p>
                <p className="text-lg text-gray-600">
                  Today, we're proud to have helped dozens of businesses transform their digital presence and achieve their goals.
                </p>
              </motion.div>
              <motion.div
                className="md:w-1/2"
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
              >
                <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Company Timeline</p>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Our Approach Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-12 text-center">Our Approach</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  title: "Goal-Oriented",
                  description: "We focus on your business goals and develop marketing strategies that help you achieve them.",
                  icon: "🎯",
                },
                {
                  title: "Data-Driven",
                  description: "We use data and analytics to inform our decisions and optimize your marketing efforts.",
                  icon: "📊",
                },
                {
                  title: "Client-Focused",
                  description: "We work closely with you to understand your unique challenges and create customized solutions.",
                  icon: "🤝",
                },
              ].map((value, index) => (
                <motion.div
                  key={index}
                  className="text-center p-6"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="text-4xl mb-4">{value.icon}</div>
                  <h3 className="text-xl font-bold mb-3">{value.title}</h3>
                  <p className="text-gray-600">{value.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-12 text-center">Meet Our Team</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {teamMembers.map((member, index) => (
                <motion.div
                  key={index}
                  className="bg-gray-50 rounded-lg overflow-hidden"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <div className="h-48 bg-gray-200 flex items-center justify-center">
                    <div className="w-20 h-20 bg-[#448ade] rounded-full flex items-center justify-center text-white text-2xl font-bold">
                      {member.name.charAt(0)}
                    </div>
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl font-bold mb-1">{member.name}</h3>
                    <p className="text-[#448ade] mb-4">{member.role}</p>
                    <p className="text-gray-600">{member.bio}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="py-16 bg-[#448ade] text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to work with us?</h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Let's discuss how our team can help your business achieve its marketing goals.
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

export default AboutPage; 
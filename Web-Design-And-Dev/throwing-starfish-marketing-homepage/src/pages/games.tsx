import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import Link from 'next/link';

const GamesPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Games & Products - Throwing Starfish Studios</title>
        <meta name="description" content="Dragons and Dice Rolls board game items - Throwing Starfish Studios" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-white">
        {/* Header with navigation back to home */}
        <header className="bg-white shadow-sm">
          <div className="container mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Games & Products</h1>
            <Link href="/" className="text-blue-500 hover:text-blue-700 transition-colors">
              ← Back to Home
            </Link>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4 max-w-6xl">
            <motion.div 
              className="text-center mb-12"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6">Dragons and Dice Rolls</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Discover our collection of board game items and accessories.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Placeholder Content */}
        <section className="py-16">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Coming Soon!</h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Our games and products catalog is currently under development. 
              Check back soon for exciting board game items and accessories!
            </p>
          </div>
        </section>
      </main>
    </>
  );
};

export default GamesPage; 
import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import SelectionCard from '../components/SelectionCard';

const HomePage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Throwing Starfish Studios</title>
        <meta name="description" content="Throwing Starfish Studios - Marketing Agency and Game Studio" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl font-bold mb-12">Throwing Starfish Studios</h1>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <SelectionCard
              title="Marketing Services"
              description="See how goal-oriented marketing can help your business"
              href="/marketing"
            />
            
            <SelectionCard
              title="View Our Products"
              description="Dragons and Dice Rolls board game items"
              href="/games"
            />
          </div>
        </div>
      </main>
    </>
  );
};

export default HomePage; 
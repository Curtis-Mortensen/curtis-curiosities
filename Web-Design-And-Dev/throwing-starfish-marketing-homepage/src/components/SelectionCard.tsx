import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

interface SelectionCardProps {
  title: string;
  description: string;
  href: string;
}

const SelectionCard: React.FC<SelectionCardProps> = ({
  title,
  description,
  href,
}) => {
  return (
    <motion.div
      className="h-full"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
    >
      <Link href={href} className="block h-full">
        <div className="rounded-lg shadow-lg overflow-hidden h-full bg-white text-gray-800 border border-gray-200">
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-3">{title}</h2>
            <p className="text-gray-600">{description}</p>
            
            <div className="mt-6 flex justify-end">
              <span className="inline-flex items-center text-sm font-medium text-gray-700">
                Explore
                <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
};

export default SelectionCard; 
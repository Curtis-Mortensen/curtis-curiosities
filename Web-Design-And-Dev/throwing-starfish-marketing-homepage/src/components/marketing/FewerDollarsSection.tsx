import React from 'react';
import { useTrackElementVisibility, useTrackAnimation } from '../../hooks/useAnalytics';

const FewerDollarsSection: React.FC = () => {
  // Track when this section becomes visible in the viewport
  const sectionRef = useTrackElementVisibility(
    'fewer-dollars',
    'section_fewer_dollars_visible'
  );
  
  // Track the animation lifecycle
  useTrackAnimation('section_fewer_dollars_animation');
  
  return (
    <section 
      id="fewer-dollars"
      ref={sectionRef}
      className="py-24 px-4 bg-gray-50"
      data-testid="fewer-dollars-section"
    >
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            With Fewer Wasted Dollars
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Our approach ensures that your marketing budget is spent efficiently, targeting the right audience with the right message at the right time.
          </p>
        </div>
        
        <div className="bg-white p-8 rounded-lg shadow-sm">
          <div className="flex flex-col items-center">
            <p className="text-gray-600 mb-8 max-w-2xl text-center">
              Traditional marketing often wastes resources on untargeted campaigns. Our goal-oriented approach focuses on efficiency and results.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-3xl">
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-xl font-bold mb-3">Traditional Marketing</h3>
                <ul className="list-disc pl-5 text-gray-600 space-y-2">
                  <li>Broad, untargeted campaigns</li>
                  <li>Difficult to measure ROI</li>
                  <li>High cost per acquisition</li>
                  <li>Wasted spend on uninterested audiences</li>
                </ul>
              </div>
              
              <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="text-xl font-bold mb-3">Goal-Oriented Marketing</h3>
                <ul className="list-disc pl-5 text-gray-600 space-y-2">
                  <li>Targeted, focused campaigns</li>
                  <li>Clear, measurable results</li>
                  <li>Lower cost per acquisition</li>
                  <li>Efficient spend on interested audiences</li>
                </ul>
              </div>
            </div>
            
            <div className="mt-10 text-center">
              <p className="text-lg font-medium mb-4">
                On average, our clients see a <span className="font-bold text-blue-600">30% reduction</span> in marketing costs while achieving <span className="font-bold text-blue-600">better results</span>.
              </p>
              
              <p className="text-gray-600">
                We focus on what works and eliminate what doesn't, continuously optimizing your marketing strategy for maximum efficiency.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FewerDollarsSection; 
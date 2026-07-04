import React, { useState } from 'react';
import { motion } from 'framer-motion';

type FormState = {
  name: string;
  email: string;
  phone: string;
  businessName: string;
  message: string;
};

type FormErrors = {
  [key in keyof FormState]?: string;
};

const ContactFormSection: React.FC = () => {
  const [formState, setFormState] = useState<FormState>({
    name: '',
    email: '',
    phone: '',
    businessName: '',
    message: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [submitMessage, setSubmitMessage] = useState('');

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    // Validate name
    if (!formState.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    // Validate email
    if (!formState.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formState.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    // Validate message
    if (!formState.message.trim()) {
      newErrors.message = 'Message is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormState(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name as keyof FormState]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formState.name,
          email: formState.email,
          phone: formState.phone || undefined,
          businessName: formState.businessName || undefined,
          message: formState.message,
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSubmitStatus('success');
        setSubmitMessage(data.message || 'Thank you for your message. We will be in touch soon!');
        // Reset form on success
        setFormState({
          name: '',
          email: '',
          phone: '',
          businessName: '',
          message: '',
        });
      } else {
        setSubmitStatus('error');
        setSubmitMessage(data.message || 'Something went wrong. Please try again later.');
      }
    } catch (error) {
      setSubmitStatus('error');
      setSubmitMessage('An unexpected error occurred. Please try again later.');
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };
  
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <section className="py-16 bg-white border-t border-gray-100">
      <div className="container mx-auto px-4 max-w-4xl">
        <motion.div 
          className="text-center mb-12"
          initial={{ opacity: 0, y: -20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">If that sounds good to you, Contact Me</h2>
          <p className="text-xl italic text-gray-600">- Curtis Mortensen</p>
        </motion.div>
        
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="bg-gray-50 p-6 md:p-8 rounded-lg shadow-sm"
        >
          {submitStatus === 'idle' ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              <motion.div variants={itemVariants}>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formState.name}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#448ade] ${
                    errors.name ? 'border-red-500' : 'border-gray-300'
                  }`}
                  aria-invalid={errors.name ? 'true' : 'false'}
                  aria-describedby={errors.name ? 'name-error' : undefined}
                />
                {errors.name && (
                  <p id="name-error" className="mt-1 text-sm text-red-500">
                    {errors.name}
                  </p>
                )}
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formState.email}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#448ade] ${
                    errors.email ? 'border-red-500' : 'border-gray-300'
                  }`}
                  aria-invalid={errors.email ? 'true' : 'false'}
                  aria-describedby={errors.email ? 'email-error' : undefined}
                />
                {errors.email && (
                  <p id="email-error" className="mt-1 text-sm text-red-500">
                    {errors.email}
                  </p>
                )}
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                  Phone (Optional)
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formState.phone}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#448ade]"
                />
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <label htmlFor="businessName" className="block text-sm font-medium text-gray-700 mb-1">
                  Business Name
                </label>
                <input
                  type="text"
                  id="businessName"
                  name="businessName"
                  value={formState.businessName}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#448ade]"
                />
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
                  Message <span className="text-red-500">*</span>
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={5}
                  value={formState.message}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#448ade] ${
                    errors.message ? 'border-red-500' : 'border-gray-300'
                  }`}
                  aria-invalid={errors.message ? 'true' : 'false'}
                  aria-describedby={errors.message ? 'message-error' : undefined}
                />
                {errors.message && (
                  <p id="message-error" className="mt-1 text-sm text-red-500">
                    {errors.message}
                  </p>
                )}
              </motion.div>
              
              <motion.div variants={itemVariants} className="text-sm text-gray-500 mt-4">
                <p>
                  By submitting this form, you agree to our{' '}
                  <a href="/privacy-policy" className="text-[#448ade] hover:underline">
                    Privacy Policy
                  </a>
                  .
                </p>
              </motion.div>
              
              <motion.div variants={itemVariants} className="flex justify-center mt-8">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-[#fde047] hover:bg-[#fcd34d] text-gray-900 font-bold py-3 px-8 rounded-md transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fde047] disabled:opacity-70"
                >
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
              </motion.div>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className={`text-center py-12 ${
                submitStatus === 'success' ? 'text-green-700' : 'text-red-700'
              }`}
            >
              <div className="mb-6">
                {submitStatus === 'success' ? (
                  <svg
                    className="w-16 h-16 mx-auto text-green-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                ) : (
                  <svg
                    className="w-16 h-16 mx-auto text-red-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                )}
              </div>
              <h3 className="text-2xl font-bold mb-4">
                {submitStatus === 'success' ? 'Thank You!' : 'Oops!'}
              </h3>
              <p className="text-lg mb-6">{submitMessage}</p>
              <button
                onClick={() => setSubmitStatus('idle')}
                className="bg-[#448ade] hover:bg-[#3a75c4] text-white font-medium py-2 px-6 rounded-md transition-colors duration-300"
              >
                {submitStatus === 'success' ? 'Send Another Message' : 'Try Again'}
              </button>
            </motion.div>
          )}
        </motion.div>
      </div>
    </section>
  );
};

export default ContactFormSection; 
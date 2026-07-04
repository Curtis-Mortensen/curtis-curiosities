import type { NextApiRequest, NextApiResponse } from 'next';
import { insertContact, initializeDatabase } from '../../utils/db';

// Initialize the database when the API is first called
let initialized = false;

type ContactFormData = {
  name: string;
  email: string;
  phone?: string;
  businessName?: string;
  message: string;
};

type ResponseData = {
  success: boolean;
  message: string;
  id?: number;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  // Initialize the database if not already done
  if (!initialized) {
    await initializeDatabase();
    initialized = true;
  }

  try {
    // Extract form data from request body
    const { name, email, phone, businessName, message } = req.body as ContactFormData;

    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({
        success: false,
        message: 'Name, email, and message are required fields',
      });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        success: false,
        message: 'Please provide a valid email address',
      });
    }

    // Insert contact into database
    const result = await insertContact(name, email, message, phone, businessName);
    
    // Get the inserted ID - handle both pg QueryResult and direct array return from neon
    let id: number | undefined;
    if (result && 'rows' in result && result.rows && result.rows[0]) {
      id = result.rows[0].id;
    } else if (Array.isArray(result) && result[0]) {
      id = result[0].id;
    }

    // Return success response
    return res.status(200).json({
      success: true,
      message: 'Contact form submitted successfully',
      id,
    });
  } catch (error) {
    console.error('Error submitting contact form:', error);
    return res.status(500).json({
      success: false,
      message: 'An error occurred while submitting the form. Please try again later.',
    });
  }
} 
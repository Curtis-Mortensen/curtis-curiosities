import { neon, neonConfig } from '@neondatabase/serverless';
import { Pool } from 'pg';

// Configure neon to use WebSockets for serverless environments
neonConfig.fetchConnectionCache = true;

// Get the database connection string from environment variables
const connectionString = process.env.POSTGRES_URL;

// Create a SQL query executor using neon for serverless environments
export const sql = connectionString ? neon(connectionString) : null;

// Create a connection pool for server environments
let pool: Pool | null = null;

if (connectionString) {
  pool = new Pool({
    connectionString,
  });
}

// Function to execute SQL queries
export async function query(text: string, params: unknown[] = []) {
  if (!connectionString) {
    throw new Error('Database connection string not found');
  }
  
  // Use the appropriate client based on the environment
  if (process.env.VERCEL_ENV === 'production' || process.env.VERCEL_ENV === 'preview') {
    // Use neon for serverless environments
    return sql?.(text, params);
  } else {
    // Use pool for development environment
    if (!pool) {
      throw new Error('Database pool not initialized');
    }
    const start = Date.now();
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
  }
}

// Initialize the database with required tables
export async function initializeDatabase() {
  try {
    // Create contacts table if it doesn't exist
    await query(`
      CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(50),
        business_name VARCHAR(255),
        message TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
}

// Function to insert a new contact
export async function insertContact(
  name: string,
  email: string,
  message: string,
  phone?: string,
  businessName?: string
) {
  const result = await query(
    `INSERT INTO contacts (name, email, phone, business_name, message) 
     VALUES ($1, $2, $3, $4, $5) 
     RETURNING id`,
    [name, email, phone || null, businessName || null, message]
  );
  
  return result;
} 
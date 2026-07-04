# Throwing Starfish Studios Website

This is the official website for Throwing Starfish Studios, a multifaceted company operating as a marketing agency, game design studio, and blog platform.

## Project Structure

The website is structured to direct visitors to either the marketing services or the game products, while maintaining a somewhat separate blog section.

- **Homepage**: Selection screen that directs visitors to either the marketing agency or game studio sections
- **Marketing Section**: Showcases marketing services and expertise
- **Game Studio Section**: Displays game development projects and creative digital experiences
- **Blog Section**: Hosts the "Talking Politics by Curtis Mortensen" blog

## Technology Stack

- **Framework**: Next.js
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Database**: Neon Postgres (serverless)
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Node.js 14.x or higher
- npm or yarn
- Neon Postgres database (for contact form functionality)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/throwing-starfish-studios.git
   cd throwing-starfish-studios
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables:
   - Copy `.env.local.example` to `.env.local`
   - Update the `POSTGRES_URL` with your Neon Postgres connection string

4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## Database Setup

The project uses Neon Postgres for storing contact form submissions. To set up the database:

1. Create a Neon Postgres database at [neon.tech](https://neon.tech)
2. Get your connection string from the Neon dashboard
3. Add the connection string to your `.env.local` file as `POSTGRES_URL`
4. The database tables will be automatically created when the application starts

### Database Schema

The database contains the following tables:

- **contacts**: Stores contact form submissions
  - `id`: Serial primary key
  - `name`: Submitter's name
  - `email`: Submitter's email
  - `phone`: Submitter's phone number (optional)
  - `business_name`: Submitter's business name (optional)
  - `message`: The message content
  - `created_at`: Timestamp of submission

## Development

### File Structure

```
throwing-starfish-studios/
├── public/             # Static assets
├── src/
│   ├── components/     # Reusable components
│   │   └── marketing/  # Marketing-specific components
│   ├── pages/          # Next.js pages
│   │   └── api/        # API routes
│   ├── utils/          # Utility functions
│   │   └── db.ts       # Database utilities
│   └── styles/         # Global styles
├── .env.local          # Environment variables (not in repo)
├── .env.local.example  # Example environment variables
├── .eslintrc.json      # ESLint configuration
├── next.config.js      # Next.js configuration
├── package.json        # Project dependencies
├── postcss.config.js   # PostCSS configuration
├── tailwind.config.js  # Tailwind CSS configuration
└── tsconfig.json       # TypeScript configuration
```

## Deployment

The website is automatically deployed to Vercel when changes are pushed to the main branch.

### Vercel Deployment

When deploying to Vercel:

1. Add the `POSTGRES_URL` environment variable in the Vercel project settings
2. Vercel will automatically handle the serverless database connection

## License

This project is proprietary and confidential. All rights reserved.

## Contact

For inquiries, please contact info@throwingstarfish.com. 
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
  },
  // Ensure API routes are properly handled
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
}

module.exports = nextConfig 
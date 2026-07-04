# Architecture Decision Record (ADR)
## Throwing Starfish Studios Website

### Document Information
- **Version:** 1.0
- **Last Updated:** [Current Date]
- **Status:** Draft

## Executive Summary
This document outlines the architectural decisions for the Throwing Starfish Studios website, which will serve as a unified platform for the company's marketing agency, game design studio, and blog. The architecture is designed to support the distinct needs of each section while maintaining brand consistency and allowing for future expansion.

## Architectural Goals
1. Create a modular structure that allows independent development of each section
2. Ensure fast loading times and responsive design across all devices
3. Support easy content management for the blog section
4. Maintain clear separation between marketing and game studio sections
5. Allow for future expansion, particularly of the game studio section

## Technology Stack

### Frontend
- **Framework:** Next.js (React-based framework)
  - *Rationale:* Provides excellent static site generation capabilities with the option for server-side rendering where needed. Supports clean routing and code splitting.
- **Styling:** Tailwind CSS with custom theme
  - *Rationale:* Offers utility-first approach for rapid development while allowing for consistent branding through theming.
- **Animations:** Framer Motion
  - *Rationale:* React-specific animation library that provides smooth scroll-based animations for the marketing promotional flow with minimal performance impact.
- **State Management:** React Context API (minimal state requirements)
  - *Rationale:* Lightweight solution sufficient for the site's needs without adding unnecessary complexity.

### Content Management
- **Blog Content:** GitHub-based content management
  - *Rationale:* Direct updates to the repository allow for version control of content and trigger automatic deployments via Vercel.
- **Content Structure:** Markdown files with frontmatter for metadata
  - *Rationale:* Simple, developer-friendly format that works well with static site generation.
- **Marketing Content:** Static content with component-based structure
  - *Rationale:* Marketing content changes less frequently and benefits from the performance of pre-rendered pages.

### Deployment & Hosting
- **Hosting:** Vercel
  - *Rationale:* Seamless integration with Next.js, excellent performance, and automated deployments from GitHub.
- **CI/CD:** GitHub + Vercel integration
  - *Rationale:* Automatic deployments when content or code is updated in the repository.
- **Domain Management:** Single domain with path-based routing
  - *Rationale:* Maintains brand consistency while allowing section separation.

## System Architecture

### High-Level Structure
```
throwingstarfish.com/
├── / (Homepage Selection Screen)
├── /marketing/... (Marketing Agency Section)
├── /games/... (Game Studio Section)
├── /about (Shared About Section)
└── /blog/... (Talking Politics Blog)
```

### Component Architecture
- **Shared Components:**
  - Header (with conditional navigation based on section)
  - Footer
  - Logo
  - Button styles
  - Typography components
  - Animation wrappers for scroll-based effects
  
- **Marketing-Specific Components:**
  - Service showcase
  - Case study displays
  - Contact/lead generation forms
  - Animated promotional flow sections
  
- **Game-Specific Components:**
  - Game showcase templates (for future use)
  
- **Blog-Specific Components:**
  - Post templates
  - Category navigation
  - Author information

### Data Flow
1. **Static Content:**
   - Pre-rendered at build time
   - Served as static HTML/CSS/JS
   
2. **Blog Content:**
   - Stored as Markdown files in the GitHub repository
   - Updates trigger automatic rebuilds and deployments via Vercel
   - Content processed at build time using Next.js data fetching
   
3. **Form Submissions:**
   - Processed via serverless functions
   - Data stored in secure database or forwarded to email

## Routing Strategy
- **Path-Based Routing:**
  - `/` - Homepage selection screen
  - `/marketing/*` - All marketing-related pages
  - `/games/*` - All game studio-related pages
  - `/about` - Shared about page
  - `/blog/*` - All blog-related pages

- **Navigation Context:**
  - Navigation components will adapt based on the current section
  - Shared elements will maintain consistency across sections

## Performance Considerations
1. **Image Optimization:**
   - Next.js Image component for automatic optimization
   - WebP format with fallbacks
   - Lazy loading for below-the-fold content
   
2. **Animation Performance:**
   - Use Framer Motion's `whileInView` for scroll-based animations
   - Implement staggered animations to reduce CPU load
   - Ensure animations run on the compositor thread (transform/opacity)
   - Use `viewport` option to control when animations trigger
   
3. **Code Splitting:**
   - Section-specific code loaded only when needed
   - Critical CSS inlined for fast initial render
   
4. **Caching Strategy:**
   - Aggressive caching for static assets
   - Stale-while-revalidate for blog content

## Security Considerations
1. **Form Protection:**
   - CSRF protection on all forms
   - Rate limiting for submission endpoints
   
2. **Content Security:**
   - Strict Content-Security-Policy headers
   - HTTPS enforcement
   
3. **Authentication:**
   - JWT-based authentication for blog management
   - Secure, HTTP-only cookies

## Accessibility Approach
1. **Component Design:**
   - All components built with accessibility in mind
   - Proper semantic HTML structure
   
2. **Testing:**
   - Automated accessibility testing in CI/CD pipeline
   - Manual testing with screen readers

## Future Expansion Considerations
1. **Game Studio Section:**
   - Architecture allows for expansion to include game showcases
   - Potential integration with game distribution platforms
   
2. **E-commerce Capabilities:**
   - Structure supports future addition of e-commerce functionality
   - Clear separation of concerns allows for targeted updates

## Development Workflow
1. **Version Control:**
   - Git-based workflow with feature branches
   - Pull request reviews before merging
   - Content updates made directly to the main branch or through PRs
   
2. **CI/CD:**
   - Automated testing on pull requests
   - Preview deployments for review
   - Automated production deployments on merge to main or direct commits to main

## Monitoring and Analytics
1. **Performance Monitoring:**
   - Core Web Vitals tracking
   - Real User Monitoring (RUM)
   
2. **Usage Analytics:**
   - Section-specific analytics to track user flow
   - Conversion tracking for marketing section

## Appendix
### Technical Debt Considerations
- Initial game studio section will be minimal, with planned technical debt to be addressed in future phases
- Blog search functionality may use simpler implementation initially, with more robust solution planned for Phase 2

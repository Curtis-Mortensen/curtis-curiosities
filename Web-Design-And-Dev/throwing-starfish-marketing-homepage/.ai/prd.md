# Product Requirements Document (PRD)
## Throwing Starfish Studios Website

### Document Information
- **Version:** 0.1
- **Last Updated:** 1 March
- **Status:** Draft

### Executive Summary
Throwing Starfish Studios is a multifaceted company operating as a marketing agency, game design studio, and blog platform. This website will serve as the digital hub for all three aspects of the business, with a unique structure that directs visitors to either the marketing services or the game products, while maintaining a somewhat separate blog section.

### Product Vision
To create a cohesive yet distinct online presence that effectively showcases Throwing Starfish Studios' marketing services and game products, while also hosting the "Talking Politics by Curtis Mortensen" blog in a deliberately semi-hidden manner.

### Target Audience
1. **Marketing Clients:** Businesses seeking marketing services
2. **Game Enthusiasts:** Potential customers for game products
3. **Blog Readers:** People interested in political content by Curtis Mortensen

### Business Objectives
1. Generate leads for marketing services
2. Showcase and eventually sell game products
3. Provide a platform for political blog content
4. Maintain brand consistency while serving distinct audience needs

### Success Metrics
1. Conversion rate on marketing service inquiries
2. Engagement with game product previews
3. Blog readership and engagement
4. Overall site traffic and user flow between sections

## Product Requirements

### Epic 1: Landing Pages
Create the foundational structure that allows visitors to navigate between the different aspects of Throwing Starfish Studios.

#### Stories:
1. **Homepage Selection Screen**
   - Create a visually appealing landing page that clearly directs visitors to either the marketing agency or game studio sections
   - Include the Throwing Starfish Studios logo prominently
   - Ensure responsive design for all device types

2. **Shared Navigation Elements**
   - Implement the Throwing Starfish Studios logo as a consistent brand element across all pages
   - Create a shared "About" page accessible from both the marketing and game sections
   - Implement shared footer elements with essential company information

3. **URL Structure and Routing**
   - Set up proper routing for the different sections (/marketing, /games, /about, /blog)
   - Ensure clean URL structures throughout the site
   - Implement proper redirects and 404 handling

### Epic 2: Marketing Agency Section
Develop the marketing agency section of the website with a focus on lead generation.

#### Stories:
1. **Marketing Landing Page**
   - Create a compelling landing page that showcases marketing services
   - Implement a unique navigation bar specific to the marketing section
   - Design with conversion optimization in mind

2. **Marketing Services Showcase**
   - Create detailed pages for each marketing service offered
   - Include case studies and success stories
   - Implement visual elements that demonstrate marketing expertise

3. **Marketing Lead Generation Flow**
   - Design and implement a promotional flow that guides visitors toward conversion
   - Create an effective call-to-action (CTA) that encourages inquiries
   - Implement a contact/inquiry form optimized for conversion

4. **Marketing Section Navigation**
   - Implement a navigation bar specific to the marketing section
   - Ensure intuitive user flow through the marketing content
   - Include links to relevant case studies and testimonials

### Epic 3: Game Studio Section (Future Development)
Create a placeholder for the game studio section with basic information, to be expanded later.

#### Stories:
1. **Game Studio Landing Page**
   - Create a basic landing page for the game studio section
   - Implement a unique navigation bar specific to the game section
   - Include placeholder content for future development

2. **Game Studio Navigation**
   - Implement a navigation bar specific to the game studio section
   - Include links to placeholder pages for future game showcases
   - Ensure consistent branding with the rest of the site

### Epic 4: Talking Politics Blog
Develop the semi-hidden blog section focused on political content by Curtis Mortensen.

#### Stories:
1. **Blog Infrastructure**
   - Set up the blog using Markdown files in the GitHub repository
   - Implement blog-specific design elements and styling
   - Create templates for rendering blog posts from Markdown
   - Configure automatic deployment via Vercel when content is updated

2. **Blog Access Points**
   - Implement access to the blog via direct URL (/blog)
   - Add a subtle link to the blog from the About page
   - Ensure the blog remains somewhat hidden from the main navigation

3. **Introductory Blog Post**
   - Create and pin an introductory post explaining the blog's purpose
   - Implement pinning functionality for featured posts
   - Design the post to establish the blog's voice and focus

4. **Blog Navigation and Categories**
   - Implement blog-specific navigation
   - Create category structure using frontmatter in Markdown files
   - Implement search functionality for blog content

### Epic 5: About Section
Create a shared About section that connects all aspects of Throwing Starfish Studios.

#### Stories:
1. **About Page Content**
   - Create compelling content about Throwing Starfish Studios' history and mission
   - Include information about both the marketing and game development aspects
   - Add team information and credentials

2. **Blog Connection**
   - Implement a subtle but accessible link to the blog from the About page
   - Design this connection to maintain the semi-hidden nature of the blog
   - Ensure consistent navigation back to main sections

## Technical Requirements

### Platform & Technology
- Static website with Next.js framework
- Content managed through GitHub repository
- Automatic deployment via Vercel integration
- Responsive design for all device types
- SEO optimization across all pages
- Analytics implementation to track user flow between sections

### Performance
- Fast loading times (under 3 seconds for initial page load)
- Optimized images and assets
- Efficient routing between sections

### Security
- HTTPS implementation
- Proper data handling for any forms
- Security best practices for all user interactions

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility

## Implementation Considerations

### Phase 1 Priority (Initial Launch)
1. Epic 1: Landing Pages (all stories)
2. Epic 2: Marketing Agency Section (all stories)
3. Epic 5: About Section (all stories)

### Phase 2 Priority
1. Epic 4: Talking Politics Blog (all stories)

### Future Development
1. Epic 3: Game Studio Section (all stories)

## Appendix

### Glossary
- **TSS**: Throwing Starfish Studios
- **CTA**: Call to Action

### References
- Brand guidelines document (to be created)
- Content strategy document (to be created)

# Story: Testimonials Carousel

## Story Information
- **Epic:** Marketing Homepage
- **Story ID:** STORY-MH-4
- **Status:** Draft
- **Priority:** Medium
- **Estimated Effort:** Medium

## User Story
As a potential client visiting the marketing homepage, I want to see testimonials from other satisfied clients, so that I can build trust in the services offered and understand the real-world benefits others have experienced.

## Description
This story involves creating an interactive testimonials carousel that appears at the bottom of the page, after the contact form section. The carousel will showcase client feedback through rotating cards that feature client logos, photos, and reviews. Users will be able to navigate through testimonials using arrow controls, and the carousel will include smooth animations between cards. The design will follow the minimalist black/white aesthetic with strategic use of gold (fde047) and blue (448ade) accent colors.

## Acceptance Criteria

### Card Design
1. Each testimonial card features a client logo on the left side
2. Each card includes a client photo in a bubble format on the right side
3. Cards display review text in italicized quotations in the center
4. Default user icon appears when no client photo is available
5. Cards have a clean, professional design that matches the site's minimalist black/white aesthetic

### Carousel Functionality
6. Carousel displays one testimonial card at a time on mobile, and up to three on larger screens if space permits
7. Left and right arrow controls allow users to navigate between testimonials
8. Smooth animation transitions between cards when navigating
9. Carousel automatically rotates through testimonials at a reasonable interval (e.g., every 8 seconds)
10. Auto-rotation pauses when user hovers over or interacts with the carousel
11. Carousel is responsive and displays appropriately on all device sizes
12. Navigation arrows use blue accent color (448ade) with gold (fde047) on hover

### Accessibility & Performance
13. Carousel navigation is accessible via keyboard controls
14. Appropriate ARIA attributes are implemented for screen reader support
15. Animations respect user preferences for reduced motion
16. Carousel loads testimonial data efficiently to minimize performance impact
17. Navigation arrows have appropriate hover and focus states

## Technical Notes
- Implement using React components with state management for the current slide
- Use Framer Motion for card transition animations
- Implement lazy loading for testimonial images to improve performance
- Use IntersectionObserver to pause auto-rotation when carousel is not in view
- Consider using a swipe gesture library for touch device navigation
- Implement prefers-reduced-motion media query support
- Use sans-serif font for testimonial text
- Implement the specified color scheme: blue (448ade) for navigation arrows, gold (fde047) for hover states
- Create placeholder testimonials for initial implementation

## Dependencies
- Placeholder testimonial content (logos, photos, quotes)
- Animation library (Framer Motion)
- Design system for card styling
- Default user icon asset
- Color palette: black/white with blue (448ade) and gold (fde047) accents
- Sans-serif typography

## Tasks
1. Create basic carousel component structure
2. Implement testimonial card design
3. Add navigation controls (arrows) with appropriate colors
4. Implement card transition animations
5. Add auto-rotation functionality
6. Implement responsive behavior for different screen sizes
7. Add default user icon fallback for missing photos
8. Create placeholder testimonial content
9. Implement keyboard navigation
10. Add appropriate ARIA attributes for accessibility
11. Implement reduced motion support
12. Add hover pause functionality
13. Optimize image loading for performance
14. Implement analytics tracking for carousel interactions
15. Test across devices and browsers
16. Apply the minimalist black/white aesthetic with strategic use of accent colors

## Related Documents
- [Marketing Homepage Epic](./../epic-marketing-homepage.md)
- [Architecture Document](./../arch.md) 
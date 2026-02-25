## Project Summary
This project is a pixel-perfect clone of the "Well Being" blog (https://well-being.blogspot.com/), a health-focused blog specializing in holistic health applications. The design captures a classic blogger aesthetic with a DNA-themed banner, grey gradient navigation tabs, and a structured three-column layout.

## Tech Stack
- Framework: Next.js (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Components: React with Lucide icons (where applicable) and custom SVG/images from the original site.

## Architecture
- `src/app/page.tsx`: Main entry point assembling the cloned sections.
- `src/components/sections/`: Contains the modular components for each part of the website:
    - `header.tsx`: Top banner and main navigation tabs.
    - `navigation.tsx`: Secondary navigation/tabs logic.
    - `main-article.tsx`: Central content area for blog posts.
    - `sidebar.tsx`: Right-side widgets (Archive, Popular Posts, Contact).
    - `footer-navigation.tsx`: Pagination and subscription links.
    - `credits.tsx`: Bottom attribution and social links.

## User Preferences
- Pixel-perfect accuracy for the "Well Being" blog clone.

## Project Guidelines
- Use `"use client"` for components utilizing `styled-jsx` or complex inline style tags to avoid RSC conflicts.
- Maintain the original Greek content and link structure where possible.

## Common Patterns
- 3-column layout on desktop, stacking on mobile.
- Custom fonts like 'Trebuchet MS' and 'Times New Roman' for the authentic blog feel.

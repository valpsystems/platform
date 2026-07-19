# VALP SYSTEMS — Enterprise Website

**VALP SYSTEMS** is an enterprise cloud engineering and platform engineering company. This repository contains the official website — a production-quality frontend built with Next.js 16, TypeScript, and Tailwind CSS.

## Project Progress

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Complete | Frontend foundation: design system, layout, pages |
| 2 | ✅ Complete | Service detail pages, expanded content, restructured architecture |
| 3 | ⬜ Pending | FastAPI backend |
| 4 | ⬜ Pending | PostgreSQL database |
| 5 | ⬜ Pending | Authentication |
| 6 | ⬜ Pending | Docker containerization |
| 7 | ⬜ Pending | CI/CD pipelines |
| 8 | ⬜ Pending | AWS deployment |
| 9 | ⬜ Pending | Monitoring & observability |
| 10 | ⬜ Pending | AI platform integration |
| 11 | ⬜ Pending | Microservices architecture |

## Implemented Pages (17)

| Route | Description |
|-------|-------------|
| `/` | Home page with hero, trusted technologies, core services, why VALP, process, solutions, metrics, CTA |
| `/about` | Company overview, mission, vision, values, technology expertise, journey timeline, CTA |
| `/services` | Services landing page with card grid |
| `/services/cloud-engineering` | Cloud Engineering detail page |
| `/services/platform-engineering` | Platform Engineering detail page |
| `/services/devsecops` | DevSecOps detail page |
| `/services/ai-engineering` | AI Engineering detail page |
| `/services/managed-services` | Managed Services detail page |
| `/solutions` | Solutions landing page with card grid |
| `/resources` | Blogs, Architecture Guides, Whitepapers, Case Studies, Downloads |
| `/careers` | Company culture, benefits, hiring process, open positions |
| `/contact` | Contact info cards, contact form, office details, social links |
| `/privacy-policy` | Privacy policy legal content |
| `/terms-and-conditions` | Terms & conditions legal content |

## Architecture

```
src/
├── app/                    # Next.js App Router pages
│   ├── about/
│   ├── services/
│   │   ├── cloud-engineering/
│   │   ├── platform-engineering/
│   │   ├── devsecops/
│   │   ├── ai-engineering/
│   │   └── managed-services/
│   ├── solutions/
│   ├── resources/
│   ├── careers/
│   ├── contact/
│   ├── privacy-policy/
│   └── terms-and-conditions/
├── components/
│   ├── common/             # Logo, Container, SectionHeading, PageHero, CTASection, etc.
│   ├── home/               # Home page sections
│   ├── layout/             # Navbar, Footer
│   ├── ui/                 # Button, Badge, Card, ServiceCard, MetricCard, Timeline
│   └── placeholders/       # IllustrationPlaceholder
├── content/                # All business content
│   ├── services/           # Service detail content + index
│   ├── solutions/          # Solution detail content + index
│   └── shared/             # Metrics, technologies, FAQs, testimonials
├── config/                 # Brand configuration
├── types/                  # TypeScript interfaces
└── lib/                    # Utility functions
```

## Content Architecture

All business content is separated from UI components and stored in `src/content/`:

```
content/
├── home.ts                 # Home page content
├── about.ts                # About page content
├── services.ts             # Services landing page content
├── services/
│   ├── index.ts            # Services list (Service[])
│   ├── cloud-engineering.ts
│   ├── platform-engineering.ts
│   ├── devsecops.ts
│   ├── ai-engineering.ts
│   └── managed-services.ts
├── solutions.ts            # Solutions landing page content
├── solutions/
│   └── index.ts            # Solutions list (Solution[])
├── resources.ts
├── careers.ts
├── contact.ts
├── privacy.ts
├── terms.ts
└── shared/
    ├── metrics.ts
    ├── technologies.ts
    ├── faqs.ts
    └── testimonials.ts
```

## Future Backend Integration

The frontend is designed for seamless backend integration:

- All content is centralized in `src/content/` — swap static content with API calls
- Page structure follows a consistent pattern: Navbar → Hero → Sections → Placeholder → CTA → Footer
- Form on `/contact` ready for API endpoint integration
- Service detail pages follow a reusable template pattern

## Tech Stack

| Technology | Use |
|---|---|
| Next.js 16 | React framework with App Router |
| TypeScript | Type safety |
| Tailwind CSS v4 | Utility-first styling |
| Framer Motion | Animations |
| Lucide React | Icons |
| next/font | Font optimization |

## Getting Started

```bash
cd frontend
npm install
npm run dev       # Development server at localhost:3000
npm run build     # Production build
npm run lint      # Run ESLint
```

# Entity Relationship Diagram

## Tables Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BASE (Abstract)                          │
│  id │ created_at │ updated_at │ created_by │ updated_by    │
│  is_active │ is_deleted │ deleted_at │ version              │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼──────────────────────────┐
        │                     │                          │
        ▼                     ▼                          ▼
┌───────────────┐    ┌───────────────────┐    ┌──────────────────┐
│   contacts    │    │   newsletters     │    │ career_applications│
├───────────────┤    ├───────────────────┤    ├──────────────────┤
│ name          │    │ email (UQ)        │    │ name             │
│ email         │    │ name              │    │ email            │
│ phone         │    │ is_subscribed     │    │ phone            │
│ company       │    │ status            │    │ position         │
│ subject       │    │ subscribed_at     │    │ experience_years │
│ message       │    │ unsubscribed_at   │    │ cover_letter     │
│ status        │    └───────────────────┘    │ resume_path      │
│ notes         │                             │ linkedin_url     │
└───────────────┘                             │ portfolio_url    │
                                              │ status           │
┌──────────────────┐    ┌──────────────────┐  └──────────────────┘
│  quote_requests  │    │   feedbacks      │
├──────────────────┤    ├──────────────────┤  ┌──────────────────┐
│ company          │    │ name             │  │  technologies    │
│ name             │    │ email            │  ├──────────────────┤
│ email            │    │ category         │  │ name (UQ)        │
│ phone            │    │ rating           │  │ slug (UQ)        │
│ service          │    │ message          │  │ category         │
│ project_description│  └──────────────────┘  │ description      │
│ budget_range     │                          │ icon             │
│ timeline         │                          │ display_order    │
│ status           │                          │ is_featured      │
└──────────────────┘                          │ status           │
                                              └──────────────────┘
┌──────────────────┐    ┌──────────────────┐
│    services      │    │   solutions      │  ┌──────────────────┐
├──────────────────┤    ├──────────────────┤  │   resources      │
│ title (UQ)       │    │ title (UQ)       │  ├──────────────────┤
│ slug (UQ)        │    │ slug (UQ)        │  │ title (UQ)       │
│ description      │    │ description      │  │ slug (UQ)        │
│ icon             │    │ category         │  │ category         │
│ display_order    │    │ icon             │  │ summary          │
│ is_featured      │    │ display_order    │  │ content          │
│ status           │    │ is_featured      │  │ author           │
└──────────────────┘    │ status           │  │ published_date   │
                        └──────────────────┘  │ cover_image      │
                                              │ tags             │
                                              │ status           │
                                              └──────────────────┘
```

## Indexes

### contacts
- Primary: `id`
- Indexes: `name`, `email`, `status`
- Composite: `(email, status)`, `(status, created_at)`

### newsletters
- Primary: `id`
- Unique: `email`
- Indexes: `status`, `(is_subscribed, subscribed_at)`

### career_applications
- Primary: `id`
- Indexes: `name`, `email`, `position`, `status`
- Composite: `(position, status)`, `(created_at, status)`

### quote_requests
- Primary: `id`
- Indexes: `name`, `email`, `service`, `status`
- Composite: `(service, status)`, `(created_at, status)`

### feedbacks
- Primary: `id`
- Indexes: `category`, `(category, rating)`, `(created_at)`

### technologies
- Primary: `id`
- Unique: `name`, `slug`
- Indexes: `category`, `status`
- Composite: `(category, display_order)`, `(is_featured, display_order)`

### services
- Primary: `id`
- Unique: `title`, `slug`
- Indexes: `status`, `(display_order)`, `(is_featured, display_order)`

### solutions
- Primary: `id`
- Unique: `title`, `slug`
- Indexes: `category`, `status`
- Composite: `(category, display_order)`, `(is_featured, display_order)`

### resources
- Primary: `id`
- Unique: `title`, `slug`
- Indexes: `category`, `status`, `(published_date)`
- Composite: `(category, status)`, `(status, created_at)`

## Relationships

The current schema has no foreign key relationships between tables.
All tables are independent business entities designed for a modular monolith.

Future relationships (Phase 5+):
- `services` → `technologies` (many-to-many via junction table)
- `solutions` → `services` (many-to-many via junction table)
- `contacts` → `users` (assigned to)
- `quote_requests` → `users` (assigned to)
- All `created_by`/`updated_by` → `users`

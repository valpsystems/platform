export interface Service {
  title: string
  description: string
  icon: string
  features: readonly string[]
}

export interface ServiceDetail {
  hero: { title: string; subtitle: string }
  overview: { title: string; description: string }
  capabilities: { title: string; items: readonly string[] }
  benefits: { title: string; items: readonly BenefitItem[] }
  approach: { title: string; steps: readonly TimelineItem[] }
  technologies: readonly string[]
  cta: { title: string; description: string; button: string }
}

export interface BenefitItem {
  title: string
  description: string
}

export interface Solution {
  title: string
  description: string
  category: string
  features: readonly string[]
}

export interface SolutionDetail {
  hero: { title: string; subtitle: string }
  overview: { title: string; description: string }
  challenges: readonly string[]
  approach: string
  outcomes: readonly string[]
  cta: { title: string; description: string; button: string }
}

export interface Metric {
  value: string
  label: string
  prefix?: string
  suffix?: string
}

export interface TeamMember {
  name: string
  role: string
  bio: string
}

export interface FAQItem {
  question: string
  answer: string
}

export interface TimelineItem {
  year: string
  title: string
  description: string
}

export interface NavLink {
  label: string
  href: string
  children?: NavLink[]
}

export interface ResourceItem {
  title: string
  description: string
  type: string
}

export interface CareerRole {
  title: string
  location: string
  type: string
  description: string
  department: string
}

export interface ContactInfo {
  label: string
  value: string
  href: string
  icon: string
}

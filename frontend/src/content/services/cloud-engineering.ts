import type { ServiceDetail } from "@/types"

export const cloudEngineeringContent: ServiceDetail = {
  hero: {
    title: "Cloud Engineering",
    subtitle:
      "Design, migrate, and optimize multi-cloud infrastructure at enterprise scale.",
  },
  overview: {
    title: "Enterprise Cloud Engineering",
    description:
      "We architect, build, and manage cloud-native solutions across AWS, Azure, and GCP. Our cloud engineering practice delivers secure, scalable, and cost-optimized infrastructure that accelerates your digital transformation.",
  },
  capabilities: {
    title: "Our Capabilities",
    items: [
      "Multi-cloud architecture and strategy",
      "Cloud migration and modernization",
      "Kubernetes and container orchestration",
      "Infrastructure as Code at scale",
      "Cloud cost optimization and FinOps",
      "Serverless and event-driven computing",
      "Cloud security and compliance",
      "Disaster recovery and business continuity",
    ],
  },
  benefits: {
    title: "Why Choose Our Cloud Engineering",
    items: [
      {
        title: "Reduced Time to Market",
        description: "Automated infrastructure provisioning cuts deployment cycles from weeks to hours.",
      },
      {
        title: "Cost Optimization",
        description: "AI-driven resource right sizing and reserved instance management reduce cloud spend by 30-40%.",
      },
      {
        title: "Enterprise Security",
        description: "Zero-trust architecture with encryption, IAM, and compliance baked into every layer.",
      },
      {
        title: "Scalability by Design",
        description: "Auto-scaling infrastructure that handles peak loads without manual intervention.",
      },
    ],
  },
  approach: {
    title: "Our Engineering Approach",
    steps: [
      {
        year: "01",
        title: "Assessment",
        description: "Comprehensive audit of your current infrastructure, workloads, and cloud maturity.",
      },
      {
        year: "02",
        title: "Architecture Design",
        description: "Enterprise-grade cloud architecture designed for security, scalability, and resilience.",
      },
      {
        year: "03",
        title: "Migration & Build",
        description: "Phased migration with automated testing, validation, and rollback capabilities.",
      },
      {
        year: "04",
        title: "Optimization",
        description: "Continuous performance monitoring, cost optimization, and architecture refinement.",
      },
    ],
  },
  technologies: [
    "AWS", "Azure", "GCP", "Kubernetes", "Terraform",
    "Crossplane", "Helm", "Kustomize", "Docker", "Vault",
    "Istio", "Prometheus", "Grafana", "Datadog",
  ],
  cta: {
    title: "Transform Your Cloud Infrastructure",
    description: "Let our cloud architects design a solution tailored to your enterprise.",
    button: "Start Your Cloud Journey",
  },
}

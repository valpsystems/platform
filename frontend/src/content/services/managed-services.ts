import type { ServiceDetail } from "@/types"

export const managedServicesContent: ServiceDetail = {
  hero: {
    title: "Managed Services",
    subtitle:
      "24/7 management and support for your enterprise platforms.",
  },
  overview: {
    title: "Enterprise Platform Operations",
    description:
      "We provide comprehensive managed services including 24/7 monitoring, incident management, patch management, performance optimization, backup and disaster recovery, and security operations. Your platforms run smoothly while you focus on business growth.",
  },
  capabilities: {
    title: "Managed Services Capabilities",
    items: [
      "24/7 platform monitoring and alerting",
      "Incident management and resolution",
      "Patch management and upgrades",
      "Performance optimization and tuning",
      "Backup and disaster recovery",
      "Security operations and threat monitoring",
      "Cost optimization and reporting",
      "Capacity planning and scaling",
    ],
  },
  benefits: {
    title: "Why Choose Managed Services",
    items: [
      {
        title: "Reduced Operational Overhead",
        description: "Offload platform operations so your team focuses on strategic initiatives.",
      },
      {
        title: "Enterprise SLAs",
        description: "Guaranteed response times and resolution targets backed by 24/7 coverage.",
      },
      {
        title: "Proactive Management",
        description: "Predictive monitoring identifies issues before they impact your business.",
      },
      {
        title: "Cost Predictability",
        description: "Fixed monthly pricing with no surprise charges for operational support.",
      },
    ],
  },
  approach: {
    title: "Our Managed Services Model",
    steps: [
      {
        year: "01",
        title: "Onboarding",
        description: "Comprehensive environment assessment and knowledge transfer.",
      },
      {
        year: "02",
        title: "Baseline & Monitoring",
        description: "Establish performance baselines and deploy monitoring infrastructure.",
      },
      {
        year: "03",
        title: "Ongoing Operations",
        description: "24/7 monitoring, incident response, and proactive maintenance.",
      },
      {
        year: "04",
        title: "Continuous Improvement",
        description: "Regular reviews, optimization, and architecture evolution.",
      },
    ],
  },
  technologies: [
    "Prometheus", "Grafana", "Datadog", "PagerDuty", "Opsgenie",
    "Terraform", "Ansible", "Docker", "Kubernetes", "Helm",
    "Vault", "Velero", "CloudWatch", "Azure Monitor",
  ],
  cta: {
    title: "Let Us Run Your Platforms",
    description: "Enterprise-grade managed services with 24/7 coverage and proactive support.",
    button: "Explore Managed Services",
  },
}

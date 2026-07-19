import type { ServiceDetail } from "@/types"

export const platformEngineeringContent: ServiceDetail = {
  hero: {
    title: "Platform Engineering",
    subtitle:
      "Build internal developer platforms that accelerate delivery while enforcing governance.",
  },
  overview: {
    title: "Internal Developer Platforms at Scale",
    description:
      "We design and build internal developer platforms (IDPs) that enable your engineering teams to ship faster, with built-in security, compliance, and observability. Our platforms reduce cognitive load while maintaining enterprise standards.",
  },
  capabilities: {
    title: "Platform Capabilities",
    items: [
      "Internal developer platform architecture",
      "Developer portals and self-service catalogs",
      "CI/CD pipeline engineering",
      "Platform observability and monitoring",
      "Golden path templating and scaffolding",
      "API gateway and service mesh integration",
      "Secret management and access control",
      "Platform cost allocation and chargeback",
    ],
  },
  benefits: {
    title: "Benefits of Platform Engineering",
    items: [
      {
        title: "Developer Velocity",
        description: "Self-service capabilities reduce onboarding time from weeks to minutes.",
      },
      {
        title: "Consistent Governance",
        description: "Built-in security, compliance, and cost policies enforced across all services.",
      },
      {
        title: "Reduced Cognitive Load",
        description: "Abstract infrastructure complexity so developers focus on business logic.",
      },
      {
        title: "Standardized Tooling",
        description: "Golden paths ensure consistent architecture patterns across the organization.",
      },
    ],
  },
  approach: {
    title: "How We Build Platforms",
    steps: [
      {
        year: "01",
        title: "Discovery",
        description: "Map developer workflows, pain points, and organizational structures.",
      },
      {
        year: "02",
        title: "Platform Design",
        description: "Design the platform architecture, service catalog, and golden path templates.",
      },
      {
        year: "03",
        title: "Build & Iterate",
        description: "Agile platform development with continuous feedback from developer teams.",
      },
      {
        year: "04",
        title: "Adoption & Scale",
        description: "Roll out across teams with documentation, training, and ongoing support.",
      },
    ],
  },
  technologies: [
    "Backstage", "Kubernetes", "Crossplane", "ArgoCD", "Terraform",
    "Docker", "Helm", "Prometheus", "Grafana", "OpenTelemetry",
    "Istio", "Cert-Manager", "Vault", "Kyverno",
  ],
  cta: {
    title: "Accelerate Your Engineering Teams",
    description: "Build the platform your developers deserve.",
    button: "Discuss Platform Engineering",
  },
}

export const solutionsContent = {
  hero: {
    title: "Enterprise Solutions",
    subtitle:
      "Proven, scalable solutions engineered to solve the most complex enterprise challenges.",
  },
  solutions: [
    {
      title: "Cloud Native Platform",
      description:
        "A fully managed cloud-native platform with Kubernetes orchestration, service mesh, and observability built in.",
      category: "Infrastructure",
      features: [
        "Multi-cloud Kubernetes",
        "Service mesh integration",
        "Built-in observability",
        "Automated scaling",
        "Disaster recovery",
      ],
    },
    {
      title: "Enterprise DevSecOps Pipeline",
      description:
        "End-to-end automated security pipeline integrating SAST, DAST, dependency scanning, and compliance verification.",
      category: "Security",
      features: [
        "Automated security scanning",
        "Compliance verification",
        "Secrets detection",
        "Container image scanning",
        "Policy as Code",
      ],
    },
    {
      title: "AI/ML Platform",
      description:
        "Production-grade MLOps platform with model registry, feature store, and automated deployment pipelines.",
      category: "AI",
      features: [
        "ML model registry",
        "Feature store",
        "Automated retraining",
        "Model monitoring",
        "A/B testing infrastructure",
      ],
    },
    {
      title: "Internal Developer Portal",
      description:
        "Self-service developer portal with golden path templates, service catalog, and automated provisioning.",
      category: "Platform",
      features: [
        "Self-service catalog",
        "Golden path templates",
        "Service ownership",
        "Cost visibility",
        "Documentation hub",
      ],
    },
    {
      title: "Cloud Cost Optimization",
      description:
        "AI-driven cloud cost optimization platform that analyzes usage patterns and automatically rightsizes resources.",
      category: "FinOps",
      features: [
        "Real-time cost monitoring",
        "Anomaly detection",
        "Rightsizing recommendations",
        "Reserved instance management",
        "Commitment optimization",
      ],
    },
    {
      title: "Zero-Trust Security Platform",
      description:
        "Comprehensive zero-trust security platform with identity-aware access, microsegmentation, and continuous verification.",
      category: "Security",
      features: [
        "Identity-aware access",
        "Microsegmentation",
        "Zero-trust networking",
        "Continuous verification",
        "Automated threat response",
      ],
    },
  ],
  cta: {
    title: "Discuss Your Requirements",
    description: "Our solution architects will map your needs to the right enterprise architecture.",
    button: "Schedule a Discovery Call",
  },
} as const

export const resourcesContent = {
  hero: {
    title: "Resources",
    subtitle:
      "Technical insights, best practices, and thought leadership from our engineering team.",
  },
  sections: [
    {
      title: "Blogs",
      description: "Technical articles and insights from our engineering team.",
      items: [
        {
          title: "Building Internal Developer Platforms with Backstage",
          description:
            "A comprehensive guide to implementing Backstage as your internal developer portal, including software catalog, scaffolder, and plugin architecture.",
          type: "Blog",
        },
        {
          title: "Kubernetes at Scale: Lessons from Production",
          description:
            "Best practices for running Kubernetes clusters in production environments with thousands of nodes and microservices.",
          type: "Blog",
        },
        {
          title: "Zero-Trust Security in Cloud-Native Environments",
          description:
            "Implementing zero-trust architecture principles in Kubernetes and multi-cloud environments.",
          type: "Blog",
        },
      ],
    },
    {
      title: "Architecture Guides",
      description: "Deep dives into enterprise architecture patterns and best practices.",
      items: [
        {
          title: "Multi-Cloud Architecture Patterns",
          description:
            "Reference architectures for designing resilient, portable multi-cloud infrastructure using Terraform and Crossplane.",
          type: "Guide",
        },
        {
          title: "Event-Driven Architecture with Kafka",
          description:
            "Designing and implementing event-driven systems using Apache Kafka for enterprise-scale applications.",
          type: "Guide",
        },
        {
          title: "MLOps Pipeline Architecture",
          description:
            "End-to-end MLOps pipeline design including feature stores, model registries, and automated deployment.",
          type: "Guide",
        },
      ],
    },
    {
      title: "Whitepapers",
      description: "In-depth research and analysis on enterprise technology topics.",
      items: [
        {
          title: "The State of Platform Engineering 2024",
          description:
            "An analysis of platform engineering adoption trends, challenges, and best practices across enterprises.",
          type: "Whitepaper",
        },
        {
          title: "Enterprise AI Readiness Framework",
          description:
            "A framework for assessing and building enterprise AI capabilities, from data infrastructure to MLOps.",
          type: "Whitepaper",
        },
        {
          title: "Cloud Cost Optimization at Scale",
          description:
            "Strategies and tools for managing and optimizing cloud costs across multi-cloud environments.",
          type: "Whitepaper",
        },
      ],
    },
    {
      title: "Case Studies",
      description: "Real-world results from our enterprise engagements.",
      items: [
        {
          title: "Fortune 500 Financial Services Cloud Migration",
          description:
            "How we migrated 500+ applications to AWS, reducing infrastructure costs by 45% while improving security and compliance.",
          type: "Case Study",
        },
        {
          title: "Global E-Commerce Platform Modernization",
          description:
            "Transforming a legacy e-commerce platform into a cloud-native architecture serving 50M+ users.",
          type: "Case Study",
        },
        {
          title: "Healthcare AI Platform Implementation",
          description:
            "Building a production-grade AI platform for medical imaging analysis with HIPAA-compliant MLOps pipelines.",
          type: "Case Study",
        },
      ],
    },
    {
      title: "Downloads",
      description: "Technical resources, templates, and tools for platform engineers.",
      items: [
        {
          title: "Kubernetes Production Checklist",
          description:
            "A comprehensive checklist for running Kubernetes workloads in production environments.",
          type: "Download",
        },
        {
          title: "Terraform Module Template",
          description:
            "Reusable Terraform module template following enterprise best practices for structure and testing.",
          type: "Download",
        },
        {
          title: "Platform Engineering Maturity Model",
          description:
            "Assess your organization's platform engineering maturity across key dimensions.",
          type: "Download",
        },
      ],
    },
  ],
  cta: {
    title: "Stay Updated",
    description: "Subscribe to receive the latest resources and insights from our engineering team.",
    button: "Subscribe",
  },
} as const

export const servicesContent = {
  hero: {
    title: "Our Services",
    subtitle:
      "Enterprise-grade engineering services designed to accelerate your cloud and platform transformation.",
  },
  services: [
    {
      title: "Cloud Engineering",
      description:
        "Design, migrate, and optimize multi-cloud infrastructure at enterprise scale. We architect cloud-native solutions across AWS, Azure, and GCP.",
      icon: "cloud",
      features: [
        "Multi-cloud architecture and strategy",
        "Cloud migration and modernization",
        "Kubernetes and container orchestration",
        "Infrastructure as Code",
        "Cloud cost optimization",
        "Serverless computing",
      ],
    },
    {
      title: "Platform Engineering",
      description:
        "Build internal developer platforms that accelerate delivery while enforcing governance, security, and compliance.",
      icon: "layers",
      features: [
        "Internal developer platforms",
        "Developer portals and self-service",
        "CI/CD pipeline engineering",
        "Platform observability",
        "Golden path templating",
        "API gateway and service mesh",
      ],
    },
    {
      title: "DevSecOps",
      description:
        "Integrate security into every phase of the software development lifecycle with automated, continuous security practices.",
      icon: "shield",
      features: [
        "Security automation and orchestration",
        "Compliance as Code",
        "Vulnerability management",
        "Secrets management",
        "Zero-trust architecture",
        "Security incident response",
      ],
    },
    {
      title: "AI Engineering",
      description:
        "Integrate artificial intelligence and machine learning into enterprise platforms with production-ready MLOps pipelines.",
      icon: "brain",
      features: [
        "MLOps and model lifecycle management",
        "LLM integration and fine-tuning",
        "Intelligent automation",
        "Data pipeline engineering",
        "AI governance and safety",
        "Predictive analytics platforms",
      ],
    },
    {
      title: "Managed Services",
      description:
        "24/7 management and support for your enterprise platforms with proactive monitoring, maintenance, and optimization.",
      icon: "settings",
      features: [
        "24/7 platform monitoring",
        "Incident management and resolution",
        "Patch management and upgrades",
        "Performance optimization",
        "Backup and disaster recovery",
        "Security operations",
      ],
    },
  ],
  cta: {
    title: "Need a Custom Solution?",
    description: "Our architects will design a solution tailored to your enterprise requirements.",
    button: "Schedule a Consultation",
  },
} as const

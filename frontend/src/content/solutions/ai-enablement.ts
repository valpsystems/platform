import type { SolutionDetail } from "@/types"

export const aiEnablementContent: SolutionDetail = {
  hero: {
    title: "AI Enablement",
    subtitle:
      "Build production-ready AI platforms that deliver measurable business impact.",
  },
  overview: {
    title: "AI from Experiment to Production",
    description:
      "We help enterprises operationalize artificial intelligence with robust MLOps pipelines, model governance frameworks, and scalable inference infrastructure. Move from AI experiments to production systems that drive business value.",
  },
  challenges: [
    "AI models that work in notebooks but fail in production",
    "Lack of reproducibility and versioning for ML experiments",
    "Manual model deployment processes prone to errors",
    "Difficulty monitoring model performance and drift",
    "Governance and compliance requirements for AI systems",
  ],
  approach:
    "Our AI enablement approach establishes end-to-end MLOps pipelines including feature stores, model registries, automated training and retraining, A/B testing infrastructure, and comprehensive monitoring for model performance, drift, and fairness.",
  outcomes: [
    "Production-ready AI platform within weeks, not months",
    "Automated model retraining and deployment",
    "Comprehensive model monitoring and observability",
    "AI governance framework meeting regulatory requirements",
    "Measurable business impact from AI investments",
  ],
  cta: {
    title: "Operationalize Your AI",
    description: "Turn AI experiments into production systems that drive business results.",
    button: "Enable AI in Your Enterprise",
  },
}

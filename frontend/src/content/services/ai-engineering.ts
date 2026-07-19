import type { ServiceDetail } from "@/types"

export const aiEngineeringContent: ServiceDetail = {
  hero: {
    title: "AI Engineering",
    subtitle:
      "Integrate artificial intelligence into enterprise platforms with production-ready MLOps.",
  },
  overview: {
    title: "AI at Enterprise Scale",
    description:
      "We build production-grade AI platforms with robust MLOps pipelines, model governance, and scalable inference infrastructure. From LLM integration to predictive analytics, we operationalize AI for business impact.",
  },
  capabilities: {
    title: "AI Engineering Capabilities",
    items: [
      "MLOps and model lifecycle management",
      "LLM integration and fine-tuning",
      "Intelligent automation and RPA",
      "Data pipeline engineering",
      "AI governance and safety frameworks",
      "Predictive analytics platforms",
      "Natural language processing solutions",
      "Computer vision systems",
    ],
  },
  benefits: {
    title: "Benefits of AI Engineering",
    items: [
      {
        title: "Production-Ready AI",
        description: "End-to-end MLOps pipelines ensure models are reliable, scalable, and maintainable.",
      },
      {
        title: "Responsible AI",
        description: "Built-in governance, bias detection, and explainability frameworks.",
      },
      {
        title: "Fast Time to Value",
        description: "Accelerated model deployment with automated retraining and A/B testing.",
      },
      {
        title: "Cost-Efficient Inference",
        description: "Optimized infrastructure for model serving with auto-scaling and cost controls.",
      },
    ],
  },
  approach: {
    title: "How We Deliver AI",
    steps: [
      {
        year: "01",
        title: "Use Case Discovery",
        description: "Identify high-impact AI opportunities aligned with business objectives.",
      },
      {
        year: "02",
        title: "Data Architecture",
        description: "Design data pipelines, feature stores, and training infrastructure.",
      },
      {
        year: "03",
        title: "Model Development",
        description: "Build, train, and validate models with rigorous testing and evaluation.",
      },
      {
        year: "04",
        title: "Deployment & Monitoring",
        description: "Deploy with automated pipelines, monitoring, and continuous optimization.",
      },
    ],
  },
  technologies: [
    "Python", "PyTorch", "TensorFlow", "MLflow", "Kubeflow",
    "LangChain", "LlamaIndex", "Weights & Biases", "Feast",
    "Ray", "Apache Kafka", "PostgreSQL", "DVC", "Hugging Face",
  ],
  cta: {
    title: "Operationalize AI in Your Enterprise",
    description: "Move from AI experiments to production impact.",
    button: "Start Your AI Journey",
  },
}

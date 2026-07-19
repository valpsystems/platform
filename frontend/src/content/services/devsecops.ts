import type { ServiceDetail } from "@/types"

export const devsecopsContent: ServiceDetail = {
  hero: {
    title: "DevSecOps",
    subtitle:
      "Integrate security into every phase of the software development lifecycle.",
  },
  overview: {
    title: "Security at Speed",
    description:
      "We implement automated security pipelines that integrate SAST, DAST, dependency scanning, container scanning, and compliance verification directly into your CI/CD workflows. Security becomes an enabler, not a bottleneck.",
  },
  capabilities: {
    title: "DevSecOps Capabilities",
    items: [
      "Automated security scanning and testing",
      "Compliance as Code",
      "Vulnerability management and remediation",
      "Secrets management and rotation",
      "Zero-trust architecture implementation",
      "Container image scanning and signing",
      "Infrastructure security scanning",
      "Security incident response automation",
    ],
  },
  benefits: {
    title: "Why DevSecOps Matters",
    items: [
      {
        title: "Shift Left Security",
        description: "Identify and fix vulnerabilities early in the development cycle when they're cheapest to address.",
      },
      {
        title: "Automated Compliance",
        description: "Continuous compliance verification against SOC 2, ISO 27001, HIPAA, and PCI DSS.",
      },
      {
        title: "Reduced Risk",
        description: "Automated security controls reduce the risk of breaches and data leaks.",
      },
      {
        title: "Developer Velocity",
        description: "Security automation removes manual gates and accelerates release cycles.",
      },
    ],
  },
  approach: {
    title: "Our DevSecOps Approach",
    steps: [
      {
        year: "01",
        title: "Security Audit",
        description: "Comprehensive assessment of current security posture, tools, and workflows.",
      },
      {
        year: "02",
        title: "Pipeline Design",
        description: "Design automated security pipelines integrated with existing CI/CD systems.",
      },
      {
        year: "03",
        title: "Implementation",
        description: "Deploy security automation tools, policies, and monitoring.",
      },
      {
        year: "04",
        title: "Continuous Improvement",
        description: "Ongoing monitoring, threat intelligence integration, and policy refinement.",
      },
    ],
  },
  technologies: [
    "SonarQube", "Snyk", "Trivy", "Checkov", "HashiCorp Vault",
    "Kyverno", "OPA", "Falco", "Aqua Security", "Twistlock",
    "GitHub Advanced Security", "GitLab Secure", "Wiz", "Lacework",
  ],
  cta: {
    title: "Secure Your Software Supply Chain",
    description: "Implement DevSecOps practices that protect your enterprise without slowing development.",
    button: "Start Your Security Transformation",
  },
}

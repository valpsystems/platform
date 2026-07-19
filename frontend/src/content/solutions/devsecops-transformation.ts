import type { SolutionDetail } from "@/types"

export const devsecopsTransformationContent: SolutionDetail = {
  hero: {
    title: "DevSecOps Transformation",
    subtitle:
      "Embed security into every phase of your software delivery lifecycle.",
  },
  overview: {
    title: "Security as Code, Security at Speed",
    description:
      "We implement automated security pipelines that integrate seamlessly with your CI/CD workflows. Security becomes an automated, continuous process that accelerates delivery rather than slowing it down.",
  },
  challenges: [
    "Security reviews creating bottlenecks in release cycles",
    "Vulnerabilities discovered late in the development process",
    "Manual compliance verification processes",
    "Lack of visibility into software supply chain security",
    "Inconsistent security policies across teams and environments",
  ],
  approach:
    "Our DevSecOps transformation integrates security tools directly into CI/CD pipelines, automates compliance verification, implements secrets management, container scanning, and infrastructure security scanning. We shift security left without sacrificing developer velocity.",
  outcomes: [
    "90% of vulnerabilities identified before production deployment",
    "Automated compliance across SOC 2, ISO 27001, and PCI DSS",
    "70% reduction in security incident response time",
    "Continuous security validation without manual gates",
    "Complete supply chain visibility and control",
  ],
  cta: {
    title: "Secure Your Delivery Pipeline",
    description: "Transform security from a bottleneck to an enabler.",
    button: "Start DevSecOps Transformation",
  },
}

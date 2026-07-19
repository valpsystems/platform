import type { SolutionDetail } from "@/types"

export const infrastructureAutomationContent: SolutionDetail = {
  hero: {
    title: "Infrastructure Automation",
    subtitle:
      "Automate your entire infrastructure lifecycle with IaC and GitOps.",
  },
  overview: {
    title: "Infrastructure as Code at Enterprise Scale",
    description:
      "We implement comprehensive infrastructure automation using Infrastructure as Code, policy enforcement, and GitOps workflows. Your infrastructure becomes versioned, testable, and fully automated.",
  },
  challenges: [
    "Manual infrastructure provisioning leading to configuration drift",
    "Inconsistent environments across development, staging, and production",
    "Slow and error-prone change management processes",
    "Lack of audit trail for infrastructure changes",
    "Difficulty enforcing compliance across multi-cloud environments",
  ],
  approach:
    "Our infrastructure automation methodology implements IaC with Terraform, Crossplane, or Pulumi, establishes GitOps workflows with ArgoCD or Flux, enforces policies with OPA and Kyverno, and provides complete visibility through automated drift detection and remediation.",
  outcomes: [
    "Infrastructure provisioning times reduced from days to minutes",
    "Zero configuration drift with automated remediation",
    "Complete audit trail for all infrastructure changes",
    "Consistent multi-cloud environment management",
    "Automated compliance enforcement across all resources",
  ],
  cta: {
    title: "Automate Your Infrastructure",
    description: "Eliminate manual operations and achieve true infrastructure automation.",
    button: "Start Automation Journey",
  },
}

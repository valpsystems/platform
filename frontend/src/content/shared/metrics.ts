import type { Metric } from "@/types"

export const enterpriseMetrics: Metric[] = [
  { value: "99.99", label: "Platform Uptime", suffix: "%" },
  { value: "500", label: "Enterprise Clients", suffix: "+" },
  { value: "50", label: "Cloud Platforms Managed", suffix: "+" },
  { value: "98", label: "Client Satisfaction", suffix: "%" },
]

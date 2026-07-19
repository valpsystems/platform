"use client"

import { Container } from "@/components/common/Container"
import { MetricCard } from "@/components/ui/MetricCard"
import { enterpriseMetrics } from "@/content/shared/metrics"

export function Metrics() {
  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-primary/[0.02] to-transparent" />
      <Container className="relative">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-12">
          {enterpriseMetrics.map((metric) => (
            <MetricCard
              key={metric.label}
              value={metric.value}
              label={metric.label}
              suffix={metric.suffix}
              prefix={metric.prefix}
            />
          ))}
        </div>
      </Container>
    </section>
  )
}

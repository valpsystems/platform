"use client"

import { motion } from "framer-motion"
import { Container } from "@/components/common/Container"
import { SectionHeading } from "@/components/common/SectionHeading"
import { TechnologyCard } from "@/components/ui/TechnologyCard"
import { homeContent } from "@/content/home"

const technologies = [
  "AWS", "Azure", "GCP", "Kubernetes", "Docker",
  "Terraform", "Crossplane", "Backstage", "ArgoCD",
  "Istio", "Prometheus", "Grafana", "Datadog",
  "Vault", "GitHub Actions", "GitLab CI",
]

export function TrustedTechnologies() {
  return (
    <section className="py-24">
      <Container>
        <SectionHeading
          title={homeContent.trusted.title}
          description={homeContent.trusted.description}
          badge="Technology Stack"
        />
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="flex flex-wrap justify-center gap-3"
        >
          {technologies.map((tech, index) => (
            <TechnologyCard key={tech} name={tech} index={index} />
          ))}
        </motion.div>
      </Container>
    </section>
  )
}

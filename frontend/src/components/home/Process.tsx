"use client"

import { motion } from "framer-motion"
import { Container } from "@/components/common/Container"
import { SectionHeading } from "@/components/common/SectionHeading"
import { homeContent } from "@/content/home"

export function Process() {
  return (
    <section className="py-24">
      <Container>
        <SectionHeading title={homeContent.process.title} badge="How We Deliver" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          {homeContent.process.steps.map((step, index) => (
            <motion.div
              key={step.year}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative"
            >
              <div className="text-5xl font-bold text-primary/20 mb-4">{step.year}</div>
              <h3 className="text-lg font-semibold text-foreground mb-2">{step.title}</h3>
              <p className="text-sm text-muted leading-relaxed">{step.description}</p>
              {index < homeContent.process.steps.length - 1 && (
                <div className="hidden lg:block absolute top-6 -right-3 w-6 h-px bg-border" />
              )}
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}

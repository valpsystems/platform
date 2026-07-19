"use client"

import { motion } from "framer-motion"
import { Container } from "@/components/common/Container"
import { SectionHeading } from "@/components/common/SectionHeading"
import { Card } from "@/components/ui/card"
import { homeContent } from "@/content/home"

const icons = [
  "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z",
  "M3 12h18M12 3v18",
  "M4.93 4.93l14.14 14.14M4.93 19.07L19.07 4.93",
]

export function WhyValp() {
  return (
    <section className="py-24 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/[0.02] to-transparent" />
      <Container className="relative">
        <SectionHeading title={homeContent.why.title} badge="Why Choose Us" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {homeContent.why.points.map((point, index) => (
            <motion.div
              key={point.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card hover className="h-full flex gap-4 p-6">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                  <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d={icons[index % icons.length]} />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">{point.title}</h3>
                  <p className="text-sm text-muted leading-relaxed">{point.description}</p>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  )
}

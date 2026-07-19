"use client"

import { motion } from "framer-motion"
import { Container } from "@/components/common/Container"
import { SectionHeading } from "@/components/common/SectionHeading"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { solutionsList } from "@/content/solutions/index"

export function FeaturedSolutions() {
  const featured = solutionsList.slice(0, 3)
  return (
    <section className="py-24">
      <Container>
        <SectionHeading
          title="Featured Solutions"
          description="Proven solutions engineered for enterprise-scale challenges."
          badge="Solutions"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          {featured.map((solution, index) => (
            <motion.div
              key={solution.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card hover className="h-full">
                <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-full">
                  {solution.category}
                </span>
                <h3 className="mt-4 text-lg font-semibold text-foreground">{solution.title}</h3>
                <p className="mt-2 text-sm text-muted leading-relaxed">{solution.description}</p>
              </Card>
            </motion.div>
          ))}
        </div>
        <div className="text-center">
          <Button variant="outline" as="a" href="/solutions">
            View All Solutions
          </Button>
        </div>
      </Container>
    </section>
  )
}

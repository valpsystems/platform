"use client"

import { Container } from "@/components/common/Container"
import { SectionHeading } from "@/components/common/SectionHeading"
import { ServiceCard } from "@/components/ui/ServiceCard"
import { servicesList } from "@/content/services/index"

export function CoreServices() {
  return (
    <section className="py-24" id="services">
      <Container>
        <SectionHeading
          title="Core Services"
          description="End-to-end enterprise capabilities delivered with precision and scale."
          badge="Core Services"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {servicesList.map((service, index) => (
            <ServiceCard key={service.title} service={service} index={index} />
          ))}
        </div>
      </Container>
    </section>
  )
}

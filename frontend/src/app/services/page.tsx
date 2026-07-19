import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ServiceCard } from "@/components/ui/ServiceCard"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { ContentSection } from "@/components/common/ContentSection"
import { servicesContent } from "@/content/services"
import { servicesList } from "@/content/services/index"

export const metadata: Metadata = {
  title: "Services",
  description: "Enterprise-grade engineering services for cloud, platform, DevSecOps, AI, and managed services.",
}

export default function ServicesPage() {
  return (
    <>
      <PageHero title={servicesContent.hero.title} subtitle={servicesContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      <ContentSection title="What We Deliver" description={servicesContent.hero.subtitle} badge="Our Services">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {servicesList.map((service, index) => (
            <ServiceCard key={service.title} service={service} index={index} />
          ))}
        </div>
      </ContentSection>

      <CTASection
        title={servicesContent.cta.title}
        description={servicesContent.cta.description}
        buttonText={servicesContent.cta.button}
      />
    </>
  )
}

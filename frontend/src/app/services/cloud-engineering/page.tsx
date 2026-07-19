import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ContentSection } from "@/components/common/ContentSection"
import { BenefitCard } from "@/components/common/BenefitCard"
import { TechnologyGrid } from "@/components/common/TechnologyGrid"
import { Timeline } from "@/components/ui/Timeline"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { cloudEngineeringContent } from "@/content/services/cloud-engineering"

export const metadata: Metadata = {
  title: "Cloud Engineering",
  description: "Enterprise cloud engineering services including multi-cloud architecture, migration, and optimization.",
}

export default function CloudEngineeringPage() {
  const { hero, overview, capabilities, benefits, approach, technologies, cta } = cloudEngineeringContent
  return (
    <>
      <PageHero title={hero.title} subtitle={hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      <ContentSection title={overview.title} description={overview.description} badge="Overview" />

      <ContentSection title={capabilities.title} alt>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {capabilities.items.map((item) => (
            <div key={item} className="p-4 rounded-xl border border-border bg-card/50 text-sm text-foreground font-medium">
              {item}
            </div>
          ))}
        </div>
      </ContentSection>

      <ContentSection title={benefits.title}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {benefits.items.map((item, i) => (
            <BenefitCard key={item.title} title={item.title} description={item.description} index={i} />
          ))}
        </div>
      </ContentSection>

      <ContentSection title={approach.title} alt>
        <Timeline items={approach.steps} />
      </ContentSection>

      <ContentSection title="Technologies We Use">
        <TechnologyGrid items={technologies} />
      </ContentSection>

      <CTASection title={cta.title} description={cta.description} buttonText={cta.button} />
    </>
  )
}

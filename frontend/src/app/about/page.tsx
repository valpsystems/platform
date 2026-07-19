import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ContentSection } from "@/components/common/ContentSection"
import { FeatureGrid } from "@/components/common/FeatureGrid"
import { TechnologyGrid } from "@/components/common/TechnologyGrid"
import { Timeline } from "@/components/ui/Timeline"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { aboutContent } from "@/content/about"
import { technologies } from "@/content/shared/technologies"

export const metadata: Metadata = {
  title: "About",
  description: "Learn about VALP SYSTEMS, our mission, story, and values.",
}

export default function AboutPage() {
  return (
    <>
      <PageHero title={aboutContent.hero.title} subtitle={aboutContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-80 md:h-96" />
      </Container>

      <ContentSection title={aboutContent.overview.title} description={aboutContent.overview.description} badge="Overview" />

      <ContentSection title={aboutContent.mission.title} description={aboutContent.mission.description} badge="Our Mission" alt />

      <ContentSection title={aboutContent.vision.title} description={aboutContent.vision.description} badge="Our Vision" />

      <ContentSection title="Our Values" badge="Core Values">
        <FeatureGrid items={aboutContent.values} columns={3} />
      </ContentSection>

      <ContentSection title="Technology Expertise" description={aboutContent.expertise.description} badge="Expertise" alt>
        <TechnologyGrid items={technologies} />
      </ContentSection>

      <ContentSection title="Our Journey" badge="Timeline">
        <Timeline items={aboutContent.journey.map((j) => ({ year: j.year, title: j.title, description: j.description }))} />
      </ContentSection>

      <ContentSection title="Why VALP SYSTEMS">
        <FeatureGrid items={aboutContent.why.points} columns={2} />
      </ContentSection>

      <CTASection
        title={aboutContent.cta.title}
        description={aboutContent.cta.description}
        buttonText={aboutContent.cta.button}
        buttonHref="/careers"
      />
    </>
  )
}

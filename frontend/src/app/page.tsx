import { Hero } from "@/components/home/Hero"
import { TrustedTechnologies } from "@/components/home/TrustedTechnologies"
import { CoreServices } from "@/components/home/CoreServices"
import { WhyValp } from "@/components/home/WhyValp"
import { Process } from "@/components/home/Process"
import { FeaturedSolutions } from "@/components/home/FeaturedSolutions"
import { Metrics } from "@/components/home/Metrics"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { Container } from "@/components/common/Container"
import { homeContent } from "@/content/home"

export default function HomePage() {
  return (
    <>
      <Hero />
      <TrustedTechnologies />
      <CoreServices />
      <WhyValp />
      <Process />
      <Container className="py-12">
        <IllustrationPlaceholder height="h-80 md:h-96" />
      </Container>
      <FeaturedSolutions />
      <Metrics />
      <CTASection
        title={homeContent.cta.title}
        description={homeContent.cta.description}
        buttonText={homeContent.cta.button}
      />
    </>
  )
}

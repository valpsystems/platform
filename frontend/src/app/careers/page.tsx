import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ContentSection } from "@/components/common/ContentSection"
import { FeatureGrid } from "@/components/common/FeatureGrid"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Timeline } from "@/components/ui/Timeline"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { careersContent } from "@/content/careers"

export const metadata: Metadata = {
  title: "Careers",
  description: "Join VALP SYSTEMS and engineer the future of enterprise platforms.",
}

export default function CareersPage() {
  return (
    <>
      <PageHero title={careersContent.hero.title} subtitle={careersContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      <ContentSection title={careersContent.culture.title} description={careersContent.culture.description} badge="Culture">
        <FeatureGrid items={careersContent.culture.points} columns={3} />
      </ContentSection>

      <ContentSection title={careersContent.benefits.title} alt>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {careersContent.benefits.items.map((benefit) => (
            <Card key={benefit} glass className="text-center p-4">
              <span className="text-sm text-foreground font-medium">{benefit}</span>
            </Card>
          ))}
        </div>
      </ContentSection>

      <ContentSection title={careersContent.hiring.title} badge="How We Hire">
        <Timeline items={careersContent.hiring.steps.map((s) => ({ year: s.year, title: s.title, description: s.description }))} />
      </ContentSection>

      <ContentSection title="Open Positions" badge="Join Us">
        <div className="space-y-4">
          {careersContent.roles.map((role) => (
            <Card key={role.title} hover>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold text-foreground">{role.title}</h3>
                  <div className="flex gap-2 mt-2">
                    <Badge>{role.location}</Badge>
                    <Badge variant="outline">{role.type}</Badge>
                    <Badge variant="primary">{role.department}</Badge>
                  </div>
                  <p className="mt-2 text-sm text-muted">{role.description}</p>
                </div>
                <Button size="sm" as="a" href="/contact">
                  Apply Now
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </ContentSection>

      <CTASection
        title={careersContent.cta.title}
        description={careersContent.cta.description}
        buttonText={careersContent.cta.button}
      />
    </>
  )
}

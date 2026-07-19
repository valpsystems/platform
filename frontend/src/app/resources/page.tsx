import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ContentSection } from "@/components/common/ContentSection"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { resourcesContent } from "@/content/resources"

export const metadata: Metadata = {
  title: "Resources",
  description: "White papers, case studies, technical guides, and webinars from VALP SYSTEMS.",
}

const typeColors: Record<string, "default" | "outline" | "primary"> = {
  Blog: "primary",
  Guide: "outline",
  Whitepaper: "default",
  "Case Study": "primary",
  Download: "outline",
}

export default function ResourcesPage() {
  return (
    <>
      <PageHero title={resourcesContent.hero.title} subtitle={resourcesContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      {resourcesContent.sections.map((section) => (
        <ContentSection key={section.title} title={section.title} description={section.description} alt>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {section.items.map((item) => (
              <Card key={item.title} hover className="h-full">
                <Badge variant={typeColors[item.type] ?? "default"}>{item.type}</Badge>
                <h3 className="mt-3 text-lg font-semibold text-foreground leading-snug">{item.title}</h3>
                <p className="mt-2 text-sm text-muted leading-relaxed">{item.description}</p>
              </Card>
            ))}
          </div>
        </ContentSection>
      ))}

      <CTASection
        title={resourcesContent.cta.title}
        description={resourcesContent.cta.description}
        buttonText={resourcesContent.cta.button}
      />
    </>
  )
}

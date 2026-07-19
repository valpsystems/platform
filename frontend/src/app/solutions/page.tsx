import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { ContentSection } from "@/components/common/ContentSection"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { solutionsList } from "@/content/solutions/index"
import { solutionsContent } from "@/content/solutions"

export const metadata: Metadata = {
  title: "Solutions",
  description: "Proven enterprise solutions for cloud-native platforms, DevSecOps, AI/ML, and more.",
}

export default function SolutionsPage() {
  return (
    <>
      <PageHero title={solutionsContent.hero.title} subtitle={solutionsContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      <ContentSection title="Our Solutions" description="Proven, scalable solutions engineered to solve the most complex enterprise challenges." badge="Solutions">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {solutionsList.map((solution) => (
            <Card key={solution.title} hover className="h-full">
              <Badge variant="primary">{solution.category}</Badge>
              <h3 className="mt-4 text-lg font-semibold text-foreground">{solution.title}</h3>
              <p className="mt-2 text-sm text-muted leading-relaxed">{solution.description}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {solution.features.slice(0, 3).map((feature) => (
                  <Badge key={feature}>{feature}</Badge>
                ))}
                {solution.features.length > 3 && (
                  <Badge>+{solution.features.length - 3}</Badge>
                )}
              </div>
            </Card>
          ))}
        </div>
      </ContentSection>

      <CTASection
        title={solutionsContent.cta.title}
        description={solutionsContent.cta.description}
        buttonText={solutionsContent.cta.button}
      />
    </>
  )
}

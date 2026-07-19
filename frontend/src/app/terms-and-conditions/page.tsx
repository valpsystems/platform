import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { Breadcrumb } from "@/components/common/Breadcrumb"
import { termsContent } from "@/content/terms"

export const metadata: Metadata = {
  title: "Terms & Conditions",
  description: "VALP SYSTEMS terms and conditions for website and services.",
}

export default function TermsAndConditionsPage() {
  return (
    <>
      <PageHero title={termsContent.hero.title} subtitle={termsContent.hero.subtitle} />

      <Container className="py-12">
        <Breadcrumb items={[{ label: "Terms & Conditions" }]} />
      </Container>

      <Container className="pb-24">
        <p className="text-sm text-muted mb-12">Last updated: {termsContent.lastUpdated}</p>
        <div className="space-y-10 max-w-3xl">
          {termsContent.sections.map((section) => (
            <div key={section.title}>
              <h2 className="text-xl font-semibold text-foreground mb-3">{section.title}</h2>
              <p className="text-sm text-muted leading-relaxed">{section.content}</p>
            </div>
          ))}
        </div>
      </Container>
    </>
  )
}

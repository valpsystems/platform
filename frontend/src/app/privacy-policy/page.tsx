import type { Metadata } from "next"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { Breadcrumb } from "@/components/common/Breadcrumb"
import { privacyContent } from "@/content/privacy"

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "VALP SYSTEMS privacy policy and data protection practices.",
}

export default function PrivacyPolicyPage() {
  return (
    <>
      <PageHero title={privacyContent.hero.title} subtitle={privacyContent.hero.subtitle} />

      <Container className="py-12">
        <Breadcrumb items={[{ label: "Privacy Policy" }]} />
      </Container>

      <Container className="pb-24">
        <p className="text-sm text-muted mb-12">Last updated: {privacyContent.lastUpdated}</p>
        <div className="space-y-10 max-w-3xl">
          {privacyContent.sections.map((section) => (
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

import { SectionHeading } from "./SectionHeading"
import { Container } from "./Container"
import { cn } from "@/lib/utils"

interface ContentSectionProps {
  title: string
  description?: string
  badge?: string
  className?: string
  children?: React.ReactNode
  alt?: boolean
}

export function ContentSection({ title, description, badge, className, children, alt = false }: ContentSectionProps) {
  return (
    <section className={cn("py-20", alt && "bg-gradient-to-b from-transparent via-primary/[0.02] to-transparent", className)}>
      <Container>
        {children ? (
          <>
            <SectionHeading title={title} description={description} badge={badge} />
            {children}
          </>
        ) : (
          <SectionHeading title={title} description={description} badge={badge} />
        )}
      </Container>
    </section>
  )
}

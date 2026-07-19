import { Container } from "./Container"
import { Button } from "@/components/ui/button"

interface CTASectionProps {
  title: string
  description: string
  buttonText: string
  buttonHref?: string
}

export function CTASection({ title, description, buttonText, buttonHref = "/contact" }: CTASectionProps) {
  return (
    <section className="relative py-24 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl" />
      <Container className="relative text-center">
        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-foreground">
          {title}
        </h2>
        <p className="mt-4 text-lg text-muted max-w-2xl mx-auto">
          {description}
        </p>
        <div className="mt-8">
          <Button as="a" href={buttonHref} size="lg">
            {buttonText}
          </Button>
        </div>
      </Container>
    </section>
  )
}

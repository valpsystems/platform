import type { Metadata } from "next"
import { Mail, Phone, MapPin, Globe } from "lucide-react"
import { PageHero } from "@/components/common/PageHero"
import { Container } from "@/components/common/Container"
import { Card } from "@/components/ui/card"
import { IllustrationPlaceholder } from "@/components/placeholders/IllustrationPlaceholder"
import { CTASection } from "@/components/common/CTASection"
import { Button } from "@/components/ui/button"
import { contactContent } from "@/content/contact"
import { brand } from "@/config/brand"

export const metadata: Metadata = {
  title: "Contact",
  description: "Get in touch with VALP SYSTEMS for enterprise platform engineering services.",
}

const iconMap: Record<string, typeof Mail> = {
  mail: Mail,
  phone: Phone,
  map: MapPin,
  linkedin: Globe,
}

export default function ContactPage() {
  return (
    <>
      <PageHero title={contactContent.hero.title} subtitle={contactContent.hero.subtitle} />

      <Container className="pb-12">
        <IllustrationPlaceholder height="h-64 md:h-80" />
      </Container>

      <div className="py-12">
        <Container>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
            {contactContent.info.map((item) => {
              const Icon = iconMap[item.icon] ?? Mail
              return (
                <Card key={item.label} hover className="text-center">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="text-sm font-medium text-muted mb-2">{item.label}</h3>
                  <a href={item.href} className="text-foreground hover:text-primary transition-colors font-medium text-sm">
                    {item.value}
                  </a>
                </Card>
              )
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <Card className="p-8">
              <h2 className="text-2xl font-bold text-foreground mb-6">Send Us a Message</h2>
              <form className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">Full Name</label>
                    <input type="text" id="name" placeholder="John Doe" className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors" />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">Email</label>
                    <input type="email" id="email" placeholder="john@company.com" className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors" />
                  </div>
                </div>
                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-foreground mb-2">Company</label>
                  <input type="text" id="company" placeholder="Your Company" className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors" />
                </div>
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-foreground mb-2">Message</label>
                  <textarea id="message" rows={5} placeholder="Tell us about your project..." className="w-full px-4 py-3 rounded-lg border border-border bg-background text-foreground placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors resize-none" />
                </div>
                <Button type="submit" className="w-full">Send Message</Button>
              </form>
            </Card>

            <div className="space-y-6">
              <Card className="p-8 h-full">
                <h2 className="text-2xl font-bold text-foreground mb-4">Our Office</h2>
                <div className="space-y-4 text-sm text-muted">
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                    <div>
                      <p className="text-foreground font-medium">VALP SYSTEMS Headquarters</p>
                      <p>San Francisco, CA</p>
                      <p>United States</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Mail className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                    <div>
                      <p className="text-foreground font-medium">Email</p>
                      <a href={`mailto:${brand.email}`} className="hover:text-primary transition-colors">{brand.email}</a>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Phone className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                    <div>
                      <p className="text-foreground font-medium">Phone</p>
                      <a href={`tel:${brand.phone}`} className="hover:text-primary transition-colors">{brand.phone}</a>
                    </div>
                  </div>
                </div>
                <div className="mt-8">
                  <h3 className="text-sm font-semibold text-foreground mb-3">Connect With Us</h3>
                  <div className="flex gap-3">
                    {Object.entries(brand.social).map(([key, url]) => (
                      <a key={key} href={url} target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-lg border border-border flex items-center justify-center text-muted hover:text-primary hover:border-primary/50 transition-all" aria-label={key}>
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                          {key === "linkedin" && <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />}
                          {key === "twitter" && <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />}
                          {key === "github" && <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />}
                        </svg>
                      </a>
                    ))}
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </Container>
      </div>

      <CTASection
        title={contactContent.cta.title}
        description={contactContent.cta.description}
        buttonText={contactContent.cta.button}
      />
    </>
  )
}

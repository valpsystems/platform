import { cn } from "@/lib/utils"

interface SectionHeadingProps {
  title: string
  description?: string
  className?: string
  align?: "left" | "center"
  badge?: string
}

export function SectionHeading({ title, description, className, align = "center", badge }: SectionHeadingProps) {
  return (
    <div className={cn("max-w-3xl mb-16", align === "center" ? "mx-auto text-center" : "", className)}>
      {badge && (
        <span className="inline-block px-3 py-1 mb-4 text-xs font-medium text-primary bg-primary/10 rounded-full border border-primary/20">
          {badge}
        </span>
      )}
      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-foreground">
        {title}
      </h2>
      {description && (
        <p className="mt-4 text-lg text-muted leading-relaxed max-w-2xl mx-auto">
          {description}
        </p>
      )}
    </div>
  )
}

import { cn } from "@/lib/utils"

interface BadgeProps {
  children: React.ReactNode
  variant?: "default" | "outline" | "primary"
  className?: string
}

export function Badge({ children, variant = "default", className }: BadgeProps) {
  const variants = {
    default: "bg-white/5 text-muted border border-border",
    outline: "bg-transparent text-primary border border-primary/30",
    primary: "bg-primary/10 text-primary border border-primary/20",
  }

  return (
    <span className={cn("inline-flex items-center px-3 py-1 text-xs font-medium rounded-full", variants[variant], className)}>
      {children}
    </span>
  )
}

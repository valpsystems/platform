import { cn } from "@/lib/utils"

interface CardProps {
  children: React.ReactNode
  className?: string
  hover?: boolean
  glass?: boolean
}

export function Card({ children, className, hover = false, glass = false }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card p-6",
        hover && "transition-all duration-300 hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-1",
        glass && "bg-white/70 backdrop-blur-xl",
        className
      )}
    >
      {children}
    </div>
  )
}

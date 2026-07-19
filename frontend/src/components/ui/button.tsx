"use client"

import { forwardRef } from "react"
import { cn } from "@/lib/utils"

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "outline"
  size?: "sm" | "md" | "lg"
  as?: "button" | "a"
  href?: string
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", as = "button", href, children, ...props }, ref) => {
    const base =
      "inline-flex items-center justify-center font-medium transition-all duration-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50"

    const variants = {
      primary:
        "bg-primary text-white hover:bg-primary-dark shadow-lg shadow-primary/25 hover:shadow-primary/40",
      secondary:
        "bg-white/5 text-foreground border border-border hover:bg-white/10 hover:border-primary/50",
      ghost: "text-foreground hover:bg-white/5",
      outline:
        "border border-border text-foreground hover:border-primary hover:text-primary",
    }

    const sizes = {
      sm: "px-4 py-2 text-sm gap-2",
      md: "px-6 py-3 text-base gap-2",
      lg: "px-8 py-4 text-lg gap-3",
    }

    if (as === "a" && href) {
      return (
        <a href={href} className={cn(base, variants[variant], sizes[size], className)}>
          {children}
        </a>
      )
    }

    return (
      <button ref={ref} className={cn(base, variants[variant], sizes[size], className)} {...props}>
        {children}
      </button>
    )
  }
)

Button.displayName = "Button"

export { Button }

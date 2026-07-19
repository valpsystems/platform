import { cn } from "@/lib/utils"

interface ContainerProps {
  children: React.ReactNode
  className?: string
  as?: "div" | "section" | "article"
  id?: string
}

export function Container({ children, className, as = "div", id }: ContainerProps) {
  const Tag = as
  return (
    <Tag id={id} className={cn("mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8", className)}>
      {children}
    </Tag>
  )
}

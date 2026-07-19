"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface TechnologyGridProps {
  items: readonly string[]
  className?: string
}

export function TechnologyGrid({ items, className }: TechnologyGridProps) {
  return (
    <div className={cn("flex flex-wrap justify-center gap-3", className)}>
      {items.map((tech, index) => (
        <motion.div
          key={tech}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: index * 0.03 }}
          className="px-4 py-2 rounded-xl border border-border bg-card/50 text-sm text-muted font-medium hover:border-primary/30 hover:text-foreground transition-all duration-300"
        >
          {tech}
        </motion.div>
      ))}
    </div>
  )
}

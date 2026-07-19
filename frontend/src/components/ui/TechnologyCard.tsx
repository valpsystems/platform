"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface TechnologyCardProps {
  name: string
  index: number
  className?: string
}

export function TechnologyCard({ name, index, className }: TechnologyCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      className={cn(
        "flex items-center justify-center px-6 py-4 rounded-xl border border-border bg-card/50 text-sm text-muted font-medium",
        "hover:border-primary/30 hover:text-foreground transition-all duration-300",
        className
      )}
    >
      {name}
    </motion.div>
  )
}

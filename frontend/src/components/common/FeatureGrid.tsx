"use client"

import { motion } from "framer-motion"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface FeatureGridProps {
  items: readonly { title: string; description: string }[]
  columns?: 2 | 3 | 4
  className?: string
}

export function FeatureGrid({ items, columns = 2, className }: FeatureGridProps) {
  return (
    <div
      className={cn(
        "grid gap-6",
        columns === 2 && "grid-cols-1 md:grid-cols-2",
        columns === 3 && "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
        columns === 4 && "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4",
        className
      )}
    >
      {items.map((item, index) => (
        <motion.div
          key={item.title}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: index * 0.08 }}
        >
          <Card hover className="h-full">
            <span className="text-sm font-semibold text-primary">0{index + 1}</span>
            <h3 className="mt-3 text-lg font-semibold text-foreground">{item.title}</h3>
            <p className="mt-2 text-sm text-muted leading-relaxed">{item.description}</p>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}

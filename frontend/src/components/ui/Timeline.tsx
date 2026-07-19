"use client"

import { motion } from "framer-motion"
import type { TimelineItem } from "@/types"

interface TimelineProps {
  items: readonly TimelineItem[]
}

export function Timeline({ items }: TimelineProps) {
  return (
    <div className="relative">
      <div className="absolute left-8 top-0 bottom-0 w-px bg-border hidden md:block" />
      <div className="space-y-12">
        {items.map((item, index) => (
          <motion.div
            key={item.year}
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="relative pl-0 md:pl-20"
          >
            <div className="hidden md:flex absolute left-4 top-1 w-8 h-8 rounded-full bg-primary/10 border border-primary/30 items-center justify-center -translate-x-1/2">
              <div className="w-2 h-2 rounded-full bg-primary" />
            </div>
            <span className="inline-block text-sm font-semibold text-primary mb-2">
              {item.year}
            </span>
            <h3 className="text-xl font-semibold text-foreground mb-2">{item.title}</h3>
            <p className="text-muted leading-relaxed">{item.description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

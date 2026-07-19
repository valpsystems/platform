"use client"

import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

interface MetricCardProps {
  value: string
  label: string
  suffix?: string
  prefix?: string
  className?: string
}

export function MetricCard({ value, label, suffix, prefix, className }: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={cn("text-center", className)}
    >
      <div className="text-4xl sm:text-5xl font-bold text-primary">
        {prefix}{value}{suffix}
      </div>
      <div className="mt-2 text-sm text-muted">{label}</div>
    </motion.div>
  )
}

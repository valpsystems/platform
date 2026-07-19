"use client"

import { motion } from "framer-motion"
import { CheckCircle } from "lucide-react"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface BenefitCardProps {
  title: string
  description: string
  index: number
  className?: string
}

export function BenefitCard({ title, description, index, className }: BenefitCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
    >
      <Card hover className={cn("flex gap-4 p-6 h-full", className)}>
        <div className="shrink-0 mt-1">
          <CheckCircle className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-foreground mb-1">{title}</h3>
          <p className="text-sm text-muted leading-relaxed">{description}</p>
        </div>
      </Card>
    </motion.div>
  )
}

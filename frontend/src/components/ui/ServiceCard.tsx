"use client"

import { motion } from "framer-motion"
import { Cloud, Layers, Shield, Brain, Settings, type LucideIcon } from "lucide-react"
import { Card } from "./card"
import { Badge } from "./badge"
import type { Service } from "@/types"

const iconMap: Record<string, LucideIcon> = {
  cloud: Cloud,
  layers: Layers,
  shield: Shield,
  brain: Brain,
  settings: Settings,
}

interface ServiceCardProps {
  service: Service
  index: number
}

export function ServiceCard({ service, index }: ServiceCardProps) {
  const Icon = iconMap[service.icon] || Cloud

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Card hover className="h-full">
        <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
          <Icon className="w-6 h-6 text-primary" />
        </div>
        <h3 className="text-xl font-semibold text-foreground mb-2">{service.title}</h3>
        <p className="text-sm text-muted leading-relaxed mb-4">{service.description}</p>
        <div className="flex flex-wrap gap-2">
          {service.features.slice(0, 3).map((feature) => (
            <Badge key={feature} variant="outline">{feature}</Badge>
          ))}
          {service.features.length > 3 && (
            <Badge>+{service.features.length - 3}</Badge>
          )}
        </div>
      </Card>
    </motion.div>
  )
}

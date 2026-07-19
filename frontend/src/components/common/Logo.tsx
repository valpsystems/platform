import Image from "next/image"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { brand } from "@/config/brand"

interface LogoProps {
  className?: string
  width?: number
  height?: number
  showText?: boolean
}

export function Logo({ className, width, height, showText = false }: LogoProps) {
  return (
    <Link href="/" className={cn("inline-flex items-center gap-3", className)}>
      <Image
        src={brand.logo.path}
        alt={brand.logo.alt}
        width={width ?? brand.logo.width}
        height={height ?? brand.logo.height}
        priority
        className="object-contain"
      />
      {showText && (
        <span className="text-xl font-bold tracking-tight text-foreground">
          {brand.name}
        </span>
      )}
    </Link>
  )
}

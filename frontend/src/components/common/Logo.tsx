import Image from "next/image"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { brand } from "@/config/brand"

interface LogoProps {
  className?: string
  showText?: boolean
  /** Use on dark backgrounds (e.g., footer) */
  variant?: "dark" | "light"
}

export function Logo({ className, showText = false, variant = "dark" }: LogoProps) {
  return (
    <Link href="/" className={cn("inline-flex items-center gap-2.5", className)} aria-label={brand.logo.alt}>
      <Image
        src={brand.logo.path}
        alt={brand.logo.alt}
        width={brand.logo.width}
        height={brand.logo.height}
        priority
        className="h-10 w-auto object-contain"
      />
      {showText && (
        <span className="flex flex-col leading-none">
          <span
            className={cn(
              "text-lg font-extrabold tracking-tight",
              variant === "light" ? "text-white" : "text-foreground"
            )}
          >
            VALP
          </span>
          <span
            className={cn(
              "mt-0.5 text-[10px] font-semibold uppercase tracking-[0.35em]",
              variant === "light" ? "text-slate-300" : "text-muted"
            )}
          >
            Systems
          </span>
        </span>
      )}
    </Link>
  )
}

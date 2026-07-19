import { cn } from "@/lib/utils"

interface IllustrationPlaceholderProps {
  className?: string
  height?: string
}

export function IllustrationPlaceholder({ className, height = "h-64 md:h-80" }: IllustrationPlaceholderProps) {
  return (
    <div
      className={cn(
        "relative w-full rounded-2xl overflow-hidden",
        height,
        className
      )}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-accent/10 to-transparent" />
      <div className="absolute inset-0 backdrop-blur-[1px]" />
      <svg
        className="absolute inset-0 w-full h-full opacity-20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <pattern
            id="grid"
            width="40"
            height="40"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 40 0 L 0 0 0 40"
              fill="none"
              stroke="rgba(0, 102, 255, 0.15)"
              strokeWidth="0.5"
            />
          </pattern>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(0, 102, 255, 0.3)" />
            <stop offset="100%" stopColor="rgba(0, 102, 255, 0)" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        <circle cx="50%" cy="50%" r="30%" fill="url(#glow)" />
      </svg>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full bg-primary/20 border border-primary/30 backdrop-blur-xl" />
      <div className="absolute top-1/4 right-1/4 w-8 h-8 rounded-full bg-accent/20 border border-accent/30 backdrop-blur-xl" />
      <div className="absolute bottom-1/4 left-1/4 w-6 h-6 rounded-full bg-secondary/20 border border-secondary/30 backdrop-blur-xl" />
    </div>
  )
}

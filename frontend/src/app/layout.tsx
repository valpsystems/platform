import type { Metadata } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"
import { Navbar } from "@/components/layout/Navbar"
import { Footer } from "@/components/layout/Footer"

const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
})

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
})

export const metadata: Metadata = {
  title: {
    default: "VALP SYSTEMS | Engineering Intelligent Enterprise Platforms",
    template: "%s | VALP SYSTEMS",
  },
  description:
    "Enterprise cloud engineering, platform engineering, DevSecOps, AI engineering, automation, managed services, and cloud modernization.",
  keywords: [
    "cloud engineering",
    "platform engineering",
    "DevSecOps",
    "AI engineering",
    "enterprise cloud",
    "managed services",
    "cloud modernization",
  ],
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "VALP SYSTEMS",
    title: "VALP SYSTEMS | Engineering Intelligent Enterprise Platforms",
    description:
      "Enterprise cloud engineering, platform engineering, DevSecOps, AI engineering, automation, managed services, and cloud modernization.",
  },
  twitter: {
    card: "summary_large_image",
    title: "VALP SYSTEMS | Engineering Intelligent Enterprise Platforms",
    description:
      "Enterprise cloud engineering, platform engineering, DevSecOps, AI engineering, automation, managed services, and cloud modernization.",
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  )
}

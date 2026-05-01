"use client"

import { useEffect } from "react"

import { applyFontSize, getStoredFontSize } from "@/lib/preferences"

export function PreferencesProvider({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  useEffect(() => {
    applyFontSize(getStoredFontSize())
  }, [])

  return <>{children}</>
}

"use client";

import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

const THEME_OPTIONS = ["light", "dark", "system"] as const;

export function ModeToggleSettings() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex flex-wrap gap-2 rounded-2xl border p-2">
      {THEME_OPTIONS.map((option) => (
        <Button
          key={option}
          type="button"
          variant={theme === option ? "default" : "outline"}
          onClick={() => setTheme(option)}
          className="min-w-24"
        >
          {option.charAt(0).toUpperCase() + option.slice(1)}
        </Button>
      ))}
    </div>
  );
}

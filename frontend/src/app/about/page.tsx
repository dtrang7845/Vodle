"use client";

import Globe from "@/components/ui/globe";

export default function AboutPage() {
  return (
    <main className="min-h-screen px-6 py-12">
      <section className="mx-auto max-w-5xl">
        <h1 className="text-3xl font-bold mb-4">About</h1>
        <p className="text-muted-foreground mb-8">
          Temporary test page for the globe component.
        </p>

        <div className="h-[500px] w-full overflow-hidden rounded-2xl border">
          <Globe />
        </div>
      </section>
    </main>
  );
}

"use client";

import { Footer } from "@/components/custom/footer";
import { Navbar } from "@/components/custom/navbar";

export function LayoutShell({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="min-h-[calc(100vh-141px)] px-6 py-10">
        <div className="mx-auto w-full max-w-6xl">{children}</div>
      </main>
      <Footer />
    </div>
  );
}

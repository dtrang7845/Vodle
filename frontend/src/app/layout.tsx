import type { Metadata } from "next";
import { Playfair_Display } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/custom/navbar";

const playfair = Playfair_Display({
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "Vodle",
  description: "Daily Opinions. Global Perspective.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={playfair.className}>
        <div className="min-h-screen">
          <Navbar />

          <main className="px-6 py-10">
            <div className="mx-auto w-full max-w-2xl">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}

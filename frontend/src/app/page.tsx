import Link from "next/link";
import { VodleLogo } from "@/components/custom/vodle-logo";
import Globe from "@/components/ui/globe";

export default function Home() {
  return (
    <main className="flex min-h-[80vh] items-center justify-center px-6">
      <section className="w-full max-w-md text-center">
        <div className="space-y-8">
          <div className="flex justify-center">
            <Globe width={100} height={100} className="rounded-lg border" />
          </div>

          <div className="space-y-3">
            <div className="flex justify-center">
              <VodleLogo size="large" />
            </div>

            <p className="text-sm text-muted-foreground">
              Daily opinions. Global perspective.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            <Link
              href="/login"
              className="rounded-md bg-black px-4 py-2 font-medium text-white transition hover:opacity-90"
            >
              Log In
            </Link>

            <Link
              href="/signup"
              className="rounded-md border px-4 py-2 font-medium transition hover:bg-muted"
            >
              Sign Up
            </Link>

            <Link
              href="/vote"
              className="text-sm text-muted-foreground underline hover:text-black"
            >
              Continue without account
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

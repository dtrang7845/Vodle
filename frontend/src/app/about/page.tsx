import { BackHomeLink } from "@/components/custom/back-home-link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AboutPage() {
  return (
    <div className="flex flex-col bg-background px-6 py-8">
      <div className="mx-auto mb-8 w-full max-w-2xl">
        <BackHomeLink className="mb-6" />
        <h1 className="text-[2rem] font-semibold tracking-tight">About Vodle</h1>
      </div>

      <div className="mx-auto flex w-full max-w-2xl flex-col gap-6">
        <Card>
          <CardHeader>
            <CardTitle>What is Vodle</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed text-muted-foreground">
              Vodle is a daily question platform built around one central idea:
              one simple prompt each day has the power to give us clearer
              insight into the opinions of people around the world, showing
              where we may be surprisingly similar or meaningfully different.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>How It Works</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed text-muted-foreground">
              Each day, a new question is released. You choose your answer,
              submit your vote, and immediately see how other people responded.
              Over time, you can track your streak, revisit past questions, and
              explore how opinion shifts from day to day.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Our Mission</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed text-muted-foreground">
              We want to make public opinion feel lightweight, welcoming, and
              easy to return to every day. Vodle is meant to create a calmer,
              more curious kind of shared conversation.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Contact Us</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="leading-relaxed text-muted-foreground">
              Reach the team at{" "}
              <a
                className="text-primary hover:underline"
                href="mailto:vodle@sdsu.edu"
              >
                vodle@sdsu.edu
              </a>{" "}
              for feedback, bugs, or collaboration ideas.
            </p>
          </CardContent>
        </Card>

        <div className="border-t pt-6">
          <p className="text-sm text-muted-foreground">
            © 2026 Vodle. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type Option = {
  id: number;
  question_id: number;
  option_text: string;
  created_at: string;
};

type TodayQuestion = {
  id: number;
  title: string;
  description: string | null;
  question_text: string;
  publish_date: string;
  created_at: string;
  options: Option[];
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function VotePage() {
  const [question, setQuestion] = useState<TodayQuestion | null>(null);
  const [selectedOptionId, setSelectedOptionId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchTodayQuestion = async () => {
      try {
        setErrorMessage(null);
        const res = await fetch(`${API_BASE_URL}/api/v1/question/today`);
        if (res.status === 404) {
          setQuestion(null);
          return;
        }
        if (!res.ok) {
          throw new Error("Failed to fetch today's question");
        }
        const data: TodayQuestion = await res.json();
        setQuestion(data);
      } catch (error) {
        console.error(error);
        setErrorMessage("We couldn't load today's question. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchTodayQuestion();
  }, []);

  const formattedDate = question
    ? new Date(question.publish_date).toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric",
      })
    : "";

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <p className="text-sm text-muted-foreground">Loading today’s question...</p>
      </main>
    );
  }

  if (errorMessage) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="space-y-3 text-center">
          <p className="text-sm text-muted-foreground">{errorMessage}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </main>
    );
  }

  if (!question) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="space-y-2 text-center">
          <p className="text-sm text-muted-foreground">
            No question is scheduled for today yet.
          </p>
          <p className="text-xs text-muted-foreground">
            Add one from the admin flow or seed script and this page will pick it up.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <section className="w-full max-w-2xl">
        <div className="mb-6 text-center">
          <h1 className="text-4xl font-bold tracking-tight">Vodle</h1>
          <p className="mt-2 text-sm text-muted-foreground">{formattedDate}</p>
        </div>

        <Card>
          <CardHeader>
            <p className="text-center text-sm uppercase tracking-[0.2em] text-muted-foreground">
              {question.title}
            </p>
            <CardTitle className="text-center text-2xl">
              {question.question_text}
            </CardTitle>
            {question.description ? (
              <p className="text-center text-sm text-muted-foreground">
                {question.description}
              </p>
            ) : null}
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="flex flex-col gap-3">
              {question.options.map((option) => {
                const isSelected = selectedOptionId === option.id;

                return (
                  <button
                    key={option.id}
                    onClick={() => setSelectedOptionId(option.id)}
                    className={`w-full rounded-md border px-4 py-3 text-base font-medium transition ${
                      isSelected
                        ? "bg-black text-white"
                        : "bg-white text-black hover:bg-muted"
                    }`}
                  >
                    {option.option_text}
                  </button>
                );
              })}
            </div>

            <Button className="w-full" disabled={selectedOptionId === null}>
              Vote submission coming soon
            </Button>
            <p className="text-center text-xs text-muted-foreground">
              Frontend selection is live. Authenticated vote submission is the next
              backend/frontend step.
            </p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}

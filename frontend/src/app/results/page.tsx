"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import { API_BASE_URL } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type TodayQuestion = {
  id: number;
};

type ResultItem = {
  option_id: number;
  option_text: string;
  votes: number;
};

type QuestionResults = {
  id: number;
  title: string;
  description: string | null;
  question_text: string;
  publish_date: string;
  created_at: string;
  results: ResultItem[];
};

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const [results, setResults] = useState<QuestionResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        setErrorMessage(null);

        let questionId = searchParams.get("questionId");
        if (!questionId) {
          const todayResponse = await fetch(`${API_BASE_URL}/api/v1/question/today`);
          if (todayResponse.status === 404) {
            setResults(null);
            return;
          }
          if (!todayResponse.ok) {
            throw new Error("Failed to load today's question.");
          }

          const todayQuestion = (await todayResponse.json()) as TodayQuestion;
          questionId = String(todayQuestion.id);
        }

        const resultsResponse = await fetch(
          `${API_BASE_URL}/api/v1/question/${questionId}/results`,
        );
        if (!resultsResponse.ok) {
          throw new Error("Failed to load results.");
        }

        const data = (await resultsResponse.json()) as QuestionResults;
        setResults(data);
      } catch (error) {
        console.error(error);
        setErrorMessage("We couldn't load the results right now.");
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [searchParams]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <p className="text-sm text-muted-foreground">Loading results...</p>
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

  if (!results) {
    return (
      <main className="flex min-h-screen items-center justify-center px-6">
        <p className="text-sm text-muted-foreground">
          No results are available yet because there is no scheduled question.
        </p>
      </main>
    );
  }

  const totalVotes = results.results.reduce(
    (sum, optionResult) => sum + optionResult.votes,
    0,
  );

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-2xl items-center justify-center px-6 py-12">
      <section className="w-full space-y-6">
        <div className="space-y-2 text-center">
          <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">
            {results.title}
          </p>
          <h1 className="text-3xl font-semibold">{results.question_text}</h1>
          {results.description ? (
            <p className="text-sm text-muted-foreground">{results.description}</p>
          ) : null}
          <p className="text-xs text-muted-foreground">
            {totalVotes} total vote{totalVotes === 1 ? "" : "s"}
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-center">Current Results</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {results.results.map((result) => {
              const percentage =
                totalVotes === 0 ? 0 : Math.round((result.votes / totalVotes) * 100);

              return (
                <div key={result.option_id} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{result.option_text}</span>
                    <span className="text-muted-foreground">
                      {result.votes} vote{result.votes === 1 ? "" : "s"} • {percentage}%
                    </span>
                  </div>
                  <div className="h-3 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full rounded-full bg-primary transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </CardContent>
        </Card>
      </section>
    </main>
  );
}

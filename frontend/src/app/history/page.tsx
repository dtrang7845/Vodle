"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { format } from "date-fns";

import { API_BASE_URL } from "@/lib/api";
import { formatDateOnly, parseDateOnly } from "@/lib/dates";
import { BackHomeLink } from "@/components/custom/back-home-link";
import { buttonVariants } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type Question = {
  id: number;
  title: string;
  description: string | null;
  question_text: string;
  publish_date: string;
  created_at: string;
};

type ResultItem = {
  option_id: number;
  option_text: string;
  votes: number;
};

type HistoryResult = {
  id: number;
  title: string;
  description: string | null;
  question_text: string;
  publish_date: string;
  results: ResultItem[];
  yourAnswer: string | null;
  topAnswer: string | null;
  totalVotes: number;
};

export default function HistoryPage() {
  const [historyItems, setHistoryItems] = useState<HistoryResult[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/question/`);
        if (!response.ok) {
          throw new Error("Unable to load question history.");
        }

        const data = (await response.json()) as Question[];
        const sortedQuestions = data.sort(
          (left, right) =>
            parseDateOnly(right.publish_date).getTime() -
            parseDateOnly(left.publish_date).getTime(),
        );

        const historyResults = await Promise.all(
          sortedQuestions.map(async (question) => {
            const [resultsResponse, voteResponse] = await Promise.all([
              fetch(`${API_BASE_URL}/api/v1/question/${question.id}/results`),
              fetch(`${API_BASE_URL}/api/v1/vote/me/question/${question.id}`, {
                credentials: "include",
              }),
            ]);

            if (!resultsResponse.ok) {
              throw new Error("Unable to load question results.");
            }

            const resultsData = (await resultsResponse.json()) as {
              results: ResultItem[];
            };
            const voteData = voteResponse.ok
              ? ((await voteResponse.json()) as { option_id: number } | null)
              : null;

            const topResult = [...resultsData.results].sort(
              (left, right) => right.votes - left.votes,
            )[0];
            const yourResult = resultsData.results.find(
              (result) => result.option_id === voteData?.option_id,
            );
            const totalVotes = resultsData.results.reduce(
              (sum, result) => sum + result.votes,
              0,
            );

            return {
              ...question,
              results: resultsData.results,
              yourAnswer: yourResult?.option_text ?? null,
              topAnswer: topResult?.option_text ?? null,
              totalVotes,
            } satisfies HistoryResult;
          }),
        );

        setHistoryItems(historyResults);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Unable to load question history.";
        setErrorMessage(message);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const firstQuestionDate = useMemo(() => {
    if (historyItems.length === 0) {
      return undefined;
    }

    return parseDateOnly(historyItems[historyItems.length - 1].publish_date);
  }, [historyItems]);

  const todayKey = format(new Date(), "yyyy-MM-dd");

  const todayResult = useMemo(
    () => historyItems.find((item) => item.publish_date === todayKey) ?? null,
    [historyItems, todayKey],
  );

  const filteredQuestions = useMemo(() => {
    if (!selectedDate) {
      return historyItems.filter((item) => item.publish_date < todayKey);
    }

    const selectedKey = format(selectedDate, "yyyy-MM-dd");
    return historyItems
      .filter((item) => item.publish_date < todayKey)
      .filter((question) => question.publish_date === selectedKey);
  }, [historyItems, selectedDate, todayKey]);

  if (loading) {
    return <p className="text-sm text-muted-foreground">Loading history...</p>;
  }

  if (errorMessage) {
    return <p className="text-sm text-destructive">{errorMessage}</p>;
  }

  return (
    <section className="space-y-6">
      <div className="space-y-4">
        <BackHomeLink />
        <h1 className="text-3xl font-semibold">History</h1>
        <p className="text-sm text-muted-foreground">
          Browse previously published questions and jump straight to their results.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
        <Card className="h-fit">
          <CardHeader>
            <CardTitle className="text-lg">Search By Date</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Calendar
              mode="single"
              selected={selectedDate}
              onSelect={setSelectedDate}
              disabled={{
                after: parseDateOnly(todayKey),
                before: firstQuestionDate,
              }}
            />
            <div className="flex gap-2">
              <button
                type="button"
                className="text-sm text-muted-foreground underline"
                onClick={() => setSelectedDate(undefined)}
              >
                Clear date filter
              </button>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Today&apos;s Results</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {todayResult ? (
                <>
                  <div className="space-y-2">
                    <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
                      {formatDateOnly(todayResult.publish_date, {
                        month: "long",
                        day: "numeric",
                        year: "numeric",
                      })}
                    </p>
                    <h2 className="text-xl font-semibold">
                      {todayResult.question_text}
                    </h2>
                    {todayResult.yourAnswer ? (
                      <p className="text-sm text-muted-foreground">
                        You voted for:{" "}
                        <span className="font-medium text-foreground">
                          {todayResult.yourAnswer}
                        </span>
                      </p>
                    ) : null}
                  </div>
                  <div className="space-y-3">
                    {todayResult.results.map((result) => {
                      const percentage =
                        todayResult.totalVotes === 0
                          ? 0
                          : Math.round((result.votes / todayResult.totalVotes) * 100);
                      const isUserChoice = result.option_text === todayResult.yourAnswer;

                      return (
                        <div key={result.option_id} className="space-y-2">
                          <div className="flex items-center justify-between text-sm">
                            <span className={isUserChoice ? "font-medium" : undefined}>
                              {result.option_text}
                            </span>
                            <span className="text-muted-foreground">{percentage}%</span>
                          </div>
                          <div className="h-2 overflow-hidden rounded-full bg-muted">
                            <div
                              className={`h-full ${
                                isUserChoice ? "bg-primary" : "bg-primary/50"
                              }`}
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {todayResult.totalVotes.toLocaleString()} total votes
                  </p>
                </>
              ) : (
                <p className="text-sm text-muted-foreground">
                  Today&apos;s question has not been answered yet.
                </p>
              )}
            </CardContent>
          </Card>

          <div className="space-y-3">
            <h2 className="text-xl font-semibold">Past Results</h2>
          </div>
          {filteredQuestions.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No published question matched that date.
            </p>
          ) : (
            filteredQuestions.map((question) => (
              <Card key={question.id}>
                <CardHeader>
                  <CardTitle className="text-xl">{question.title}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-muted-foreground">
                    {formatDateOnly(question.publish_date, {
                      weekday: "long",
                      month: "long",
                      day: "numeric",
                      year: "numeric",
                    })}
                  </p>
                  <p className="font-medium">{question.question_text}</p>
                  {question.description ? (
                    <p className="text-sm text-muted-foreground">
                      {question.description}
                    </p>
                  ) : null}
                  <div className="space-y-1 text-sm text-muted-foreground">
                    {question.yourAnswer ? (
                      <p>
                        Your answer:{" "}
                        <span className="text-foreground">{question.yourAnswer}</span>
                      </p>
                    ) : null}
                    {question.topAnswer ? (
                      <p>
                        Top answer:{" "}
                        <span className="text-foreground">{question.topAnswer}</span>
                      </p>
                    ) : null}
                    <p>{question.totalVotes.toLocaleString()} votes</p>
                  </div>
                  <Link
                    href={
                      question.yourAnswer
                        ? `/results?questionId=${question.id}`
                        : `/vote?questionId=${question.id}`
                    }
                    className={cn(buttonVariants({ variant: "outline" }))}
                  >
                    {question.yourAnswer ? "Open Result" : "Answer Question"}
                  </Link>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </section>
  );
}

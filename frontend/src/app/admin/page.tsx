"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

import { API_BASE_URL } from "@/lib/api"
import { BackHomeLink } from "@/components/custom/back-home-link"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

type CurrentUser = {
  id: number
  username: string
  email: string
  role?: "user" | "admin"
}

type QuestionDraftResponse = {
  title: string
  description: string | null
  question_text: string
  options: { option_text: string }[]
}

const EMPTY_OPTIONS = ["", ""]

export default function AdminPage() {
  const router = useRouter()
  const [checkingAccess, setCheckingAccess] = useState(true)
  const [accessError, setAccessError] = useState<string | null>(null)
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [questionText, setQuestionText] = useState("")
  const [publishDate, setPublishDate] = useState("")
  const [topicHint, setTopicHint] = useState("")
  const [options, setOptions] = useState<string[]>(EMPTY_OPTIONS)
  const [submitting, setSubmitting] = useState(false)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    const verifyAdmin = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/user/me`, {
          credentials: "include",
        })

        if (response.status === 401) {
          router.push("/login")
          return
        }

        if (!response.ok) {
          throw new Error("Unable to verify your account.")
        }

        const user = (await response.json()) as CurrentUser
        if (user.role !== "admin") {
          setAccessError("This page is only available to admin users.")
          return
        }
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "Unable to verify your account."
        setAccessError(message)
      } finally {
        setCheckingAccess(false)
      }
    }

    verifyAdmin()
  }, [router])

  const setOptionValue = (index: number, value: string) => {
    setOptions((currentOptions) =>
      currentOptions.map((option, optionIndex) =>
        optionIndex === index ? value : option,
      ),
    )
  }

  const addOption = () => {
    setOptions((currentOptions) => [...currentOptions, ""])
  }

  const handleGenerateDraft = async () => {
    setGenerating(true)
    setFormError(null)
    setSuccessMessage(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/question/generate-draft`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic_hint: topicHint || null,
        }),
      })

      if (response.status === 401) {
        router.push("/login")
        return
      }

      if (!response.ok) {
        const errorData = (await response.json().catch(() => null)) as {
          detail?: string
        } | null
        throw new Error(errorData?.detail ?? "Unable to load a question-bank draft.")
      }

      const draft = (await response.json()) as QuestionDraftResponse
      setTitle(draft.title)
      setDescription(draft.description ?? "")
      setQuestionText(draft.question_text)
      setOptions(draft.options.map((option) => option.option_text))
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to load a question-bank draft."
      setFormError(message)
    } finally {
      setGenerating(false)
    }
  }

  const handleCreateQuestion = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    const cleanedOptions = options.map((option) => option.trim()).filter(Boolean)
    if (cleanedOptions.length < 2) {
      setFormError("Please provide at least two answer options.")
      return
    }

    setSubmitting(true)
    setFormError(null)
    setSuccessMessage(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/question/with-options`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          description: description || null,
          question_text: questionText,
          publish_date: publishDate,
          options: cleanedOptions.map((option_text) => ({ option_text })),
        }),
      })

      if (response.status === 401) {
        router.push("/login")
        return
      }

      if (!response.ok) {
        const errorData = (await response.json().catch(() => null)) as {
          detail?: string
        } | null
        throw new Error(errorData?.detail ?? "Unable to create the scheduled question.")
      }

      setSuccessMessage("Scheduled question created successfully.")
      setTitle("")
      setDescription("")
      setQuestionText("")
      setPublishDate("")
      setTopicHint("")
      setOptions(EMPTY_OPTIONS)
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to create the scheduled question."
      setFormError(message)
    } finally {
      setSubmitting(false)
    }
  }

  if (checkingAccess) {
    return <p className="text-sm text-muted-foreground">Checking admin access...</p>
  }

  if (accessError) {
    return <p className="text-sm text-destructive">{accessError}</p>
  }

  return (
    <section className="space-y-6">
      <div className="space-y-4">
        <BackHomeLink />
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold">Admin</h1>
          <p className="text-sm text-muted-foreground">
            Load from the question bank, review drafts, and schedule upcoming questions.
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Admin Question Tools</CardTitle>
          <CardDescription>
            Load a draft from the local question bank or manually schedule a question for a future date.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="topic-hint">Topic Hint</FieldLabel>
              <Input
                id="topic-hint"
                type="text"
                value={topicHint}
                onChange={(event) => setTopicHint(event.target.value)}
                placeholder="Optional theme like sports, food, music, travel"
              />
              <FieldDescription>
                Use this if you want the draft to lean toward a topic like travel, food, music, or fitness.
              </FieldDescription>
            </Field>
            <Field>
              <Button type="button" variant="outline" onClick={handleGenerateDraft} disabled={generating}>
                {generating ? "Loading Draft..." : "Load Suggested Draft"}
              </Button>
            </Field>
          </FieldGroup>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Create Scheduled Question</CardTitle>
          <CardDescription>
            Review or edit the fields below before saving the question.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreateQuestion}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="title">Title</FieldLabel>
                <Input
                  id="title"
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="description">Description</FieldLabel>
                <Input
                  id="description"
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="question-text">Question</FieldLabel>
                <Input
                  id="question-text"
                  value={questionText}
                  onChange={(event) => setQuestionText(event.target.value)}
                  required
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="publish-date">Publish Date</FieldLabel>
                <Input
                  id="publish-date"
                  type="date"
                  value={publishDate}
                  onChange={(event) => setPublishDate(event.target.value)}
                  required
                />
              </Field>
              {options.map((option, index) => (
                <Field key={`${index}-${option}`}>
                  <FieldLabel htmlFor={`option-${index + 1}`}>
                    Option {index + 1}
                  </FieldLabel>
                  <Input
                    id={`option-${index + 1}`}
                    value={option}
                    onChange={(event) => setOptionValue(index, event.target.value)}
                    required={index < 2}
                  />
                </Field>
              ))}
              <Field>
                <Button type="button" variant="outline" onClick={addOption}>
                  Add Another Option
                </Button>
              </Field>
              <Field>
                <Button type="submit" disabled={submitting}>
                  {submitting ? "Creating..." : "Create Scheduled Question"}
                </Button>
                {formError ? (
                  <p className="text-sm text-destructive">{formError}</p>
                ) : null}
                {successMessage ? (
                  <p className="text-sm text-foreground">{successMessage}</p>
                ) : null}
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </section>
  )
}

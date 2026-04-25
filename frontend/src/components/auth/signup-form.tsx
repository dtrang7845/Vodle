"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { useState } from "react"

import { API_BASE_URL } from "@/lib/api"
import {
  getPasswordValidationError,
  PASSWORD_REQUIREMENTS,
} from "@/lib/password-validation"
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

export function SignupForm({ ...props }: React.ComponentProps<typeof Card>) {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const validationError = getPasswordValidationError(password)
    if (validationError) {
      setError(validationError)
      return
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.")
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/user/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      })

      if (!response.ok) {
        const errorData = (await response.json().catch(() => null)) as {
          detail?: string | { msg?: string }[]
        } | null
        const detail = errorData?.detail
        if (Array.isArray(detail) && detail[0]?.msg) {
          throw new Error(detail[0].msg)
        }
        throw new Error(
          typeof detail === "string" ? detail : "Unable to create account.",
        )
      }

      router.push("/login")
    } catch (submitError) {
      const message =
        submitError instanceof Error
          ? submitError.message
          : "Unable to create account."
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>Create an account</CardTitle>
        <CardDescription>
          Enter your information below to create your account
        </CardDescription>
        </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="email">Email</FieldLabel>
              <Input
                id="email"
                type="email"
                placeholder="email@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
              <FieldDescription>
                We&apos;ll use this to contact you. We will not share your email
                with anyone else.
              </FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
                minLength={8}
              />
              <FieldDescription>
                {PASSWORD_REQUIREMENTS.join(" • ")}
              </FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor="confirm-password">
                Confirm Password
              </FieldLabel>
              <Input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                required
              />
              <FieldDescription>Please confirm your password.</FieldDescription>
            </Field>
            <FieldGroup>
              <Field>
                <Button type="submit" disabled={loading}>
                  {loading ? "Creating Account..." : "Create Account"}
                </Button>
                <Button variant="outline" type="button" disabled>
                  Sign up with Google
                </Button>
                <FieldDescription className="px-6 text-center">
                  Already have an account? <Link href="/login">Sign in</Link>
                </FieldDescription>
                {error ? (
                  <p className="text-center text-sm text-destructive">{error}</p>
                ) : null}
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  )
}

"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

import { API_BASE_URL } from "@/lib/api"
import { logoutUser } from "@/lib/auth"
import { BackHomeLink } from "@/components/custom/back-home-link"
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

type CurrentUser = {
  id: number
  username: string
  email: string
  role?: "user" | "admin"
  created_at: string
}

export default function AccountPage() {
  const router = useRouter()
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [updateError, setUpdateError] = useState<string | null>(null)
  const [updateSuccess, setUpdateSuccess] = useState<string | null>(null)
  const [updating, setUpdating] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/user/me`, {
          credentials: "include",
        })

        if (response.status === 401) {
          router.push("/login")
          return
        }

        if (!response.ok) {
          throw new Error("Unable to load your account.")
        }

        const data = (await response.json()) as CurrentUser
        setUser(data)
      } catch (accountError) {
        const message =
          accountError instanceof Error
            ? accountError.message
            : "Unable to load your account."
        setError(message)
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [router])

  const handlePasswordUpdate = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    if (!user) {
      return
    }

    const validationError = getPasswordValidationError(password)
    if (validationError) {
      setUpdateError(validationError)
      return
    }

    if (password !== confirmPassword) {
      setUpdateError("Passwords do not match.")
      return
    }

    setUpdating(true)
    setUpdateError(null)
    setUpdateSuccess(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/user/${user.id}`, {
        method: "PUT",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
      })

      if (response.status === 401) {
        router.push("/login")
        return
      }

      if (!response.ok) {
        const errorData = (await response.json().catch(() => null)) as {
          detail?: string | { msg?: string }[]
        } | null

        const detail = errorData?.detail
        if (Array.isArray(detail) && detail[0]?.msg) {
          throw new Error(detail[0].msg)
        }

        throw new Error(
          typeof detail === "string"
            ? detail
            : "Unable to update your password.",
        )
      }

      setPassword("")
      setConfirmPassword("")
      setUpdateSuccess("Your password was updated successfully.")
    } catch (passwordError) {
      const message =
        passwordError instanceof Error
          ? passwordError.message
          : "Unable to update your password."
      setUpdateError(message)
    } finally {
      setUpdating(false)
    }
  }

  const handleDeleteAccount = async () => {
    if (!user) {
      return
    }

    const confirmed = window.confirm(
      "Delete your account permanently? This will remove your login and voting history.",
    )
    if (!confirmed) {
      return
    }

    setDeleting(true)
    setUpdateError(null)
    setUpdateSuccess(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/user/${user.id}`, {
        method: "DELETE",
        credentials: "include",
      })

      if (response.status === 401) {
        router.push("/login")
        return
      }

      if (!response.ok) {
        throw new Error("Unable to delete your account.")
      }

      await logoutUser(API_BASE_URL)
      router.push("/")
    } catch (deleteError) {
      const message =
        deleteError instanceof Error
          ? deleteError.message
          : "Unable to delete your account."
      setUpdateError(message)
    } finally {
      setDeleting(false)
    }
  }

  if (loading) {
    return <p className="text-sm text-muted-foreground">Loading account...</p>
  }

  if (error) {
    return (
      <div className="space-y-3 text-center">
        <p className="text-sm text-destructive">{error}</p>
        <Button onClick={() => window.location.reload()}>Try Again</Button>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <section className="space-y-6">
      <div className="space-y-4">
        <BackHomeLink />
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold">Account</h1>
          <p className="text-sm text-muted-foreground">
            Review your profile, update your password, and manage account access.
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your Account</CardTitle>
          <CardDescription>
            Manage your profile details and account access.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Username</p>
            <p className="font-medium">{user.username}</p>
          </div>
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Email</p>
            <p className="font-medium">{user.email}</p>
          </div>
          {user.role ? (
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Role</p>
              <p className="font-medium capitalize">{user.role}</p>
            </div>
          ) : null}
          {user.role === "admin" ? (
            <Button variant="outline" onClick={() => router.push("/admin")}>
              Open Admin Tools
            </Button>
          ) : null}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Update Password</CardTitle>
          <CardDescription>
            Use a strong password that follows the current backend rules.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handlePasswordUpdate}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="new-password">New Password</FieldLabel>
                <Input
                  id="new-password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
                <FieldDescription>
                  {PASSWORD_REQUIREMENTS.join(" • ")}
                </FieldDescription>
              </Field>
              <Field>
                <FieldLabel htmlFor="confirm-new-password">
                  Confirm New Password
                </FieldLabel>
                <Input
                  id="confirm-new-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                />
              </Field>
              <Field>
                <Button type="submit" disabled={updating}>
                  {updating ? "Updating..." : "Update Password"}
                </Button>
                {updateError ? (
                  <p className="text-sm text-destructive">{updateError}</p>
                ) : null}
                {updateSuccess ? (
                  <p className="text-sm text-foreground">{updateSuccess}</p>
                ) : null}
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Danger Zone</CardTitle>
          <CardDescription>
            Deleting your account removes your access and your saved voting activity.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button
            variant="destructive"
            onClick={handleDeleteAccount}
            disabled={deleting}
          >
            {deleting ? "Deleting..." : "Delete Account"}
          </Button>
          <p className="text-sm text-muted-foreground">
            This action is permanent and should be used carefully.
          </p>
        </CardContent>
      </Card>
    </section>
  )
}

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { API_BASE_URL } from "@/lib/api";
import { BackHomeLink } from "@/components/custom/back-home-link";
import { ModeToggleSettings } from "@/components/custom/mode-toggle-settings";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  applyFontSize,
  getStoredFontSize,
  getStoredNotificationsPreference,
  setStoredFontSize,
  setStoredNotificationsPreference,
  type FontSizePreference,
} from "@/lib/preferences";

const fontSizeOptions: FontSizePreference[] = ["small", "medium", "large"];

export default function SettingsPage() {
  const router = useRouter();
  const [fontSize, setFontSize] = useState<FontSizePreference>("medium");
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/user/me`, {
          credentials: "include",
        });

        if (response.status === 401) {
          router.push("/login");
          return;
        }

        if (!response.ok) {
          throw new Error("Unable to load your settings.");
        }

        setFontSize(getStoredFontSize());
        setNotificationsEnabled(getStoredNotificationsPreference());
      } catch (settingsError) {
        const message =
          settingsError instanceof Error
            ? settingsError.message
            : "Unable to load your settings.";
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, [router]);

  const handleFontSizeChange = (nextFontSize: FontSizePreference) => {
    setFontSize(nextFontSize);
    setStoredFontSize(nextFontSize);
    applyFontSize(nextFontSize);
  };

  const handleNotificationsChange = () => {
    const nextValue = !notificationsEnabled;
    setNotificationsEnabled(nextValue);
    setStoredNotificationsPreference(nextValue);
  };

  if (loading) {
    return <p className="text-sm text-muted-foreground">Loading settings...</p>;
  }

  if (error) {
    return <p className="text-sm text-destructive">{error}</p>;
  }

  return (
    <section className="space-y-6">
      <div className="space-y-4">
        <BackHomeLink />
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold">Settings</h1>
          <p className="text-sm text-muted-foreground">
            Adjust your appearance preferences and save a few lightweight browsing defaults.
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
          <CardDescription>
            Adjust the way Vodle looks and feels while you browse.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="space-y-3">
            <p className="text-sm font-medium">Theme</p>
            <ModeToggleSettings />
          </div>
          <div className="space-y-3">
            <p className="text-sm font-medium">Font Size</p>
            <div className="flex flex-wrap gap-2">
              {fontSizeOptions.map((option) => (
                <Button
                  key={option}
                  type="button"
                  variant={fontSize === option ? "default" : "outline"}
                  onClick={() => handleFontSizeChange(option)}
                >
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Notifications</CardTitle>
          <CardDescription>
            Save simple preferences now and leave room for backend-powered notifications later.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between gap-4 rounded-2xl border p-4">
            <div className="space-y-1">
              <p className="font-medium">Daily vote reminders</p>
              <p className="text-sm text-muted-foreground">
                This preference is saved locally for now. Delivery is not wired to the backend yet.
              </p>
            </div>
            <Button
              type="button"
              variant={notificationsEnabled ? "default" : "outline"}
              onClick={handleNotificationsChange}
            >
              {notificationsEnabled ? "On" : "Off"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}

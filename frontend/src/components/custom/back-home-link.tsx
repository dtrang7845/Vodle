import Link from "next/link";
import { ArrowLeft } from "lucide-react";

type BackHomeLinkProps = {
  className?: string;
  label?: string;
};

export function BackHomeLink({
  className = "",
  label = "Back to Home",
}: BackHomeLinkProps) {
  return (
    <div className={`w-full max-w-none ${className}`.trim()}>
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground md:-ml-6"
      >
        <ArrowLeft className="h-4 w-4" />
        {label}
      </Link>
    </div>
  );
}

import * as React from "react"
import { cn } from "@/utils/cn"

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-slate-200/80", className)}
      aria-hidden="true"
      {...props}
    />
  )
}

export { Skeleton }

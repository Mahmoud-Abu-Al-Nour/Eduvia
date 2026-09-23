import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/utils/cn"

const alertVariants = cva(
  "relative w-full rounded-xl border p-4 text-sm [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-slate-950 [&>svg~*]:pl-7",
  {
    variants: {
      variant: {
        default: "bg-slate-50 border-slate-200 text-slate-800 [&>svg]:text-slate-700",
        info: "bg-teal-50/70 border-teal-200/80 text-teal-900 [&>svg]:text-teal-700",
        warning: "bg-amber-50/70 border-amber-200 text-amber-900 [&>svg]:text-amber-700",
        destructive: "bg-rose-50/70 border-rose-200 text-rose-900 [&>svg]:text-rose-700",
        success: "bg-emerald-50/70 border-emerald-200 text-emerald-900 [&>svg]:text-emerald-700",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
))
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-semibold leading-none tracking-tight", className)}
    {...props}
  />
))
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-xs [&_p]:leading-relaxed text-slate-600", className)}
    {...props}
  />
))
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }

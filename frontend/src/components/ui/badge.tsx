import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/utils/cn"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-brand-800 text-white shadow-2xs hover:bg-brand-900",
        secondary:
          "border-brand-200/80 bg-brand-50 text-brand-900 hover:bg-brand-100",
        destructive:
          "border-transparent bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100",
        success:
          "border-transparent bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100",
        warning:
          "border-transparent bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100",
        outline:
          "border-slate-300 text-slate-700",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }

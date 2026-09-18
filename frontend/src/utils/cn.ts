/**
 * Utility for merging Tailwind CSS class names with conflict resolution.
 * Re-exports the clsx + tailwind-merge pattern used throughout shadcn/ui.
 */
import { clsx, type ClassValue } from 'clsx'

export function cn(...inputs: ClassValue[]): string {
  return clsx(inputs)
}

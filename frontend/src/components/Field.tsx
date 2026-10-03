import type { ReactNode } from "react"

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="mt-3 block text-sm font-medium">
      <span>{label}</span>
      {children}
    </label>
  )
}

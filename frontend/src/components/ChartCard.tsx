import type { ReactElement, ReactNode } from "react"
import { ResponsiveContainer } from "recharts"
import { text } from "../i18n/text"

export function ChartFrame({ children }: { children: ReactElement }) {
  return <ResponsiveContainer width="100%" height="100%">{children}</ResponsiveContainer>
}

export function ChartCard({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="card">
      <h2 className="mb-3 text-lg font-semibold">{title}</h2>
      <div className="h-64">{children}</div>
    </section>
  )
}

export function EmptyChart({ title }: { title: string }) {
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mt-2 text-sm">{text("season.empty")}</p>
    </section>
  )
}

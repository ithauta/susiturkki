import type { ReactNode } from "react"
import { text } from "../i18n/text"

type ShellProps = { title: string; subtitle?: string; action?: ReactNode; children: ReactNode }

export function Shell({ title, subtitle, action, children }: ShellProps) {
  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col gap-4 px-4 py-6">
      <TopBar action={action} />
      <PageTitle title={title} subtitle={subtitle} />
      {children}
    </div>
  )
}

function TopBar({ action }: { action?: ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <p className="text-sm uppercase tracking-widest text-aurora">{text("app.title")}</p>
      {action}
    </div>
  )
}

function PageTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div>
      <h1 className="text-3xl font-semibold text-snow">{title}</h1>
      {subtitle ? <p className="text-ice">{subtitle}</p> : null}
    </div>
  )
}

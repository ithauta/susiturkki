import type { ReactNode } from "react"
import { text } from "../i18n/text"

type ShellProps = {
  title: string
  subtitle?: string
  action?: ReactNode
  trailing?: ReactNode
  head?: ReactNode
  children: ReactNode
}

export function Shell({ title, subtitle, action, trailing, head, children }: ShellProps) {
  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col gap-4 px-4 py-6">
      <Heading trailing={trailing} action={action} title={title} subtitle={subtitle} head={head} />
      {children}
    </div>
  )
}

function Heading({ trailing, action, title, subtitle, head }: Omit<ShellProps, "children">) {
  return (
    <div className="flex items-stretch gap-4">
      <HeadingText action={action} title={title} subtitle={subtitle} head={head} />
      {trailing}
    </div>
  )
}

function HeadingText({ action, title, subtitle, head }: Omit<ShellProps, "children" | "trailing">) {
  return (
    <div className="flex min-w-0 flex-1 flex-col gap-4">
      <TopBar action={action} />
      <PageTitle title={title} subtitle={subtitle} />
      {head}
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

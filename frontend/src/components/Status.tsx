import { text } from "../i18n/text"
import type { LoadState } from "../hooks/useAsync"

export function Status({ state }: { state: LoadState<unknown> }) {
  if (state.kind === "loading") return <p className="text-snow">{text("status.loading")}</p>
  if (state.kind === "error") return <p className="text-snow">{text(`error.${state.code}`)}</p>
  return null
}

export function ErrorText({ code }: { code: string }) {
  if (!code) return null
  return <p className="mt-3 text-berry">{text(`error.${code}`)}</p>
}

import type { ReactNode } from "react"
import type { Entry } from "../api/types"
import { finnishKilometers } from "../format/labels"
import { finnishMoment } from "../format/time"
import { text } from "../i18n/text"

export function EntryRow({ entry, actions }: { entry: Entry; actions?: ReactNode }) {
  return (
    <li className="mt-3 border-t border-ice pt-3">
      <EntryFacts entry={entry} />
      {actions}
    </li>
  )
}

function EntryFacts({ entry }: { entry: Entry }) {
  return (
    <div className="flex flex-wrap justify-between gap-2">
      <span>{finnishMoment(entry.performed_at)}</span>
      <span>{finnishKilometers(entry.kilometers)} {text("entry.unit")}</span>
      <span>{entry.place ?? ""}</span>
      <EntryChoices entry={entry} />
    </div>
  )
}

function EntryChoices({ entry }: { entry: Entry }) {
  return (
    <>
      <span>{text(`style.${entry.style}`)}</span>
      <span>{text(`conditions.${entry.conditions}`)}</span>
    </>
  )
}

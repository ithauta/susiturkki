import { useState } from "react"
import { deleteEntry, updateEntry } from "../api/participant"
import type { Entry, EntryBody } from "../api/types"
import { ConfirmButton } from "../components/ConfirmButton"
import { EntryForm } from "../components/EntryForm"
import { EntryRow } from "../components/EntryRow"
import { inputFromIso } from "../format/time"
import { text } from "../i18n/text"

type OwnProps = { token: string; entry: Entry; places: string[]; onChanged: () => void }

export function OwnEntry({ token, entry, places, onChanged }: OwnProps) {
  const [editing, setEditing] = useState(false)
  if (editing) return <EditOwn token={token} entry={entry} places={places} onChanged={onChanged} onClose={() => setEditing(false)} />
  return <EntryRow entry={entry} actions={<OwnActions token={token} entry={entry} onEdit={() => setEditing(true)} onChanged={onChanged} />} />
}

function OwnActions({ token, entry, onEdit, onChanged }: { token: string; entry: Entry; onEdit: () => void; onChanged: () => void }) {
  if (!entry.can_edit) return null
  return (
    <div className="mt-3 flex gap-2">
      <button className="btn-quiet" type="button" onClick={onEdit}>{text("entry.edit")}</button>
      <ConfirmButton label={text("entry.delete")} confirm={text("entry.confirmDelete")} onConfirm={() => remove(token, entry.id, onChanged)} />
    </div>
  )
}

function EditOwn({ token, entry, places, onChanged, onClose }: OwnProps & { onClose: () => void }) {
  return (
    <li className="mt-3">
      <EntryForm listId={`edit-${entry.id}`} places={places} submitLabel={text("entry.update")} initial={draft(entry)} onSubmit={(body) => save(token, entry.id, body, onChanged, onClose)} />
    </li>
  )
}

function draft(entry: Entry) {
  return { performed_at: inputFromIso(entry.performed_at), distance_km: entry.kilometers, place: entry.place ?? "" }
}

async function remove(token: string, entryId: number, onChanged: () => void) {
  await deleteEntry(token, entryId)
  onChanged()
}

async function save(token: string, entryId: number, body: EntryBody, onChanged: () => void, onClose: () => void) {
  await updateEntry(token, entryId, body)
  onChanged()
  onClose()
}

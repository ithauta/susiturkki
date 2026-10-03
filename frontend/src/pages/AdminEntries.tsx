import { useState } from "react"
import { deleteAdminEntry, updateAdminEntry } from "../api/admin"
import type { Entry, EntryBody, Group, Participant } from "../api/types"
import { ConfirmButton } from "../components/ConfirmButton"
import { EntryForm } from "../components/EntryForm"
import { EntryRow } from "../components/EntryRow"
import { Status } from "../components/Status"
import { AdminCreate } from "./AdminCreate"
import { uniquePlaces } from "../format/labels"
import { inputFromIso } from "../format/time"
import type { LoadState } from "../hooks/useAsync"
import { text } from "../i18n/text"

type LogProps = { group: Group; state: LoadState<Entry[]>; reload: () => void }

export function AdminEntries({ group, state, reload }: LogProps) {
  const entries = state.kind === "ready" ? state.data : []
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{text("entries.all")}</h2>
      <EntryItems group={group} state={state} reload={reload} />
      <AdminCreate key={entries.length} group={group} places={uniquePlaces(entries)} reload={reload} />
    </section>
  )
}

function EntryItems({ group, state, reload }: LogProps) {
  if (state.kind !== "ready") return <Status state={state} />
  if (state.data.length === 0) return <p className="mt-2 text-sm">{text("entries.empty")}</p>
  return <ul>{state.data.map((entry) => <AdminEntry key={entry.id} entry={entry} members={group.participants} places={uniquePlaces(state.data)} reload={reload} />)}</ul>
}

function AdminEntry({ entry, members, places, reload }: { entry: Entry; members: Participant[]; places: string[]; reload: () => void }) {
  const [editing, setEditing] = useState(false)
  if (editing) return <EditAdmin entry={entry} places={places} reload={reload} onClose={() => setEditing(false)} />
  return <EntryRow entry={entry} actions={<AdminActions entry={entry} members={members} onEdit={() => setEditing(true)} reload={reload} />} />
}

function AdminActions({ entry, members, onEdit, reload }: { entry: Entry; members: Participant[]; onEdit: () => void; reload: () => void }) {
  return (
    <div className="mt-3 flex flex-wrap items-center gap-2">
      <span className="text-sm">{memberName(members, entry.participant_id)}</span>
      <button className="btn-quiet" type="button" onClick={onEdit}>{text("entry.edit")}</button>
      <ConfirmButton label={text("entry.delete")} confirm={text("entry.confirmDelete")} onConfirm={() => remove(entry.id, reload)} />
    </div>
  )
}

function memberName(members: Participant[], participantId: number): string {
  return members.find((member) => member.id === participantId)?.name ?? ""
}

function EditAdmin({ entry, places, reload, onClose }: { entry: Entry; places: string[]; reload: () => void; onClose: () => void }) {
  return <li className="mt-3"><EntryForm listId={`admin-${entry.id}`} places={places} submitLabel={text("entry.update")} initial={draft(entry)} onSubmit={(body) => save(entry.id, body, reload, onClose)} /></li>
}

function draft(entry: Entry) {
  return { performed_at: inputFromIso(entry.performed_at), distance_km: entry.kilometers, place: entry.place ?? "" }
}

async function remove(entryId: number, reload: () => void) {
  await deleteAdminEntry(entryId)
  reload()
}

async function save(entryId: number, body: EntryBody, reload: () => void, onClose: () => void) {
  await updateAdminEntry(entryId, body)
  reload()
  onClose()
}

import { useCallback, useState } from "react"
import { useParams } from "react-router-dom"
import { createEntry, readEntries, readHome, readStats } from "../api/participant"
import type { Entry, EntryBody, Home, Named } from "../api/types"
import { EntryForm } from "../components/EntryForm"
import { Shell } from "../components/Shell"
import { StatsBoard } from "../components/StatsBoard"
import { Status } from "../components/Status"
import { helsinkiInput } from "../format/time"
import { OwnEntry } from "./OwnEntry"
import { useAsync } from "../hooks/useAsync"
import type { LoadState } from "../hooks/useAsync"
import { useSeasonBrowse } from "../hooks/useSeasonBrowse"
import { text } from "../i18n/text"

type FormKey = (update: (value: number) => number) => void
type ParticipantBodyProps = {
  token: string
  home: Home
  formKey: number
  revision: number
  refresh: () => void
  entries: LoadState<Entry[]>
}

export function ParticipantPage() {
  const token = useParams().token ?? ""
  const load = useCallback(() => readHome(token), [token])
  const home = useAsync(load)
  if (home.state.kind !== "ready") return <Shell title={text("app.title")}><Status state={home.state} /></Shell>
  return <ParticipantView key={token} token={token} home={home.state.data} reloadHome={home.reload} />
}

function ParticipantView({ token, home, reloadHome }: { token: string; home: Home; reloadHome: () => void }) {
  const entries = useEntries(token)
  const [formKey, setFormKey] = useState(0)
  const [revision, setRevision] = useState(0)
  const refresh = () => refreshAll(entries.reload, reloadHome, setFormKey, setRevision)
  return <ParticipantBody token={token} home={home} formKey={formKey} revision={revision} refresh={refresh} entries={entries.state} />
}

function useEntries(token: string) {
  const load = useCallback(() => readEntries(token), [token])
  return useAsync(load)
}

function ParticipantBody({ token, home, formKey, revision, refresh, entries }: ParticipantBodyProps) {
  return (
    <Shell title={home.name} subtitle={home.group_name}>
      <Logging key={`${formKey}-${home.default_place ?? ""}`} token={token} home={home} onSaved={refresh} />
      <OwnList token={token} state={entries} places={home.places} onChanged={refresh} />
      <GroupBoards token={token} groups={home.groups} revision={revision} />
    </Shell>
  )
}

function GroupBoards({ token, groups, revision }: { token: string; groups: Named[]; revision: number }) {
  return <>{groups.map((group) => <GroupBoard key={group.id} token={token} group={group} revision={revision} />)}</>
}

function GroupBoard({ token, group, revision }: { token: string; group: Named; revision: number }) {
  const browse = useGroupStats(token, group.id, revision)
  return (
    <section>
      <h2 className="mt-2 text-lg font-semibold">{group.name}</h2>
      <StatsBoard browse={browse} />
    </section>
  )
}

function useGroupStats(token: string, groupId: number, revision: number) {
  const loadFor = useCallback((season: number | undefined) => readStats(token, season, groupId), [token, groupId, revision])
  return useSeasonBrowse(loadFor)
}

function refreshAll(reloadEntries: () => void, reloadHome: () => void, setFormKey: FormKey, setRevision: FormKey) {
  reloadEntries()
  reloadHome()
  setFormKey((value) => value + 1)
  setRevision((value) => value + 1)
}

function Logging({ token, home, onSaved }: { token: string; home: Home; onSaved: () => void }) {
  if (!home.can_create) return <p className="card">{text("season.closed")}</p>
  return <EntryForm listId="new-entry" places={home.places} submitLabel={text("entry.save")} initial={draft(home)} onSubmit={(body) => saveNew(token, body, onSaved)} />
}

function draft(home: Home) {
  return { performed_at: helsinkiInput(), distance_km: "", place: home.default_place ?? "" }
}

async function saveNew(token: string, body: EntryBody, onSaved: () => void) {
  await createEntry(token, body)
  onSaved()
}

function OwnList({ token, state, places, onChanged }: { token: string; state: LoadState<Entry[]>; places: string[]; onChanged: () => void }) {
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{text("entries.own")}</h2>
      <OwnItems token={token} state={state} places={places} onChanged={onChanged} />
    </section>
  )
}

function OwnItems({ token, state, places, onChanged }: { token: string; state: LoadState<Entry[]>; places: string[]; onChanged: () => void }) {
  if (state.kind !== "ready") return <Status state={state} />
  if (state.data.length === 0) return <p className="mt-2 text-sm">{text("entries.empty")}</p>
  return <ul>{state.data.map((entry) => <OwnEntry key={entry.id} token={token} entry={entry} places={places} onChanged={onChanged} />)}</ul>
}

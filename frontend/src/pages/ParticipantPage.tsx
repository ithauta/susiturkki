import { useCallback, useState } from "react"
import { useParams } from "react-router-dom"
import { createEntry, readEntries, readHome, readStats } from "../api/participant"
import type { Entry, EntryBody, Home } from "../api/types"
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
  refresh: () => void
  entries: LoadState<Entry[]>
  stats: ReturnType<typeof useStats>
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
  const stats = useStats(token)
  const [formKey, setFormKey] = useState(0)
  const refresh = () => refreshAll(entries.reload, reloadHome, stats.reload, setFormKey)
  return <ParticipantBody token={token} home={home} formKey={formKey} refresh={refresh} entries={entries.state} stats={stats} />
}

function useEntries(token: string) {
  const load = useCallback(() => readEntries(token), [token])
  return useAsync(load)
}

function useStats(token: string) {
  const loadFor = useCallback((season: number | undefined) => readStats(token, season), [token])
  return useSeasonBrowse(loadFor)
}

function ParticipantBody({ token, home, formKey, refresh, entries, stats }: ParticipantBodyProps) {
  return (
    <Shell title={home.name} subtitle={home.group_name}>
      <Logging key={`${formKey}-${home.default_place ?? ""}`} token={token} home={home} onSaved={refresh} />
      <OwnList token={token} state={entries} places={home.places} onChanged={refresh} />
      <StatsBoard browse={stats} />
    </Shell>
  )
}

function refreshAll(reloadEntries: () => void, reloadHome: () => void, reloadStats: () => void, setFormKey: FormKey) {
  reloadEntries()
  reloadHome()
  reloadStats()
  setFormKey((value) => value + 1)
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

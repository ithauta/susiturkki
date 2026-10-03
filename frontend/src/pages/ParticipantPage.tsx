import { useCallback, useLayoutEffect, useRef, useState } from "react"
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
import logo from "../assets/logo.jpg"

type FormKey = (update: (value: number) => number) => void
type Pane = "log" | "standings"
type Desk = {
  pane: Pane
  setPane: (pane: Pane) => void
  groups: Named[]
  groupId: number | undefined
  setGroupId: (id: number) => void
  browse: ReturnType<typeof useGroupStats>
}
type LogProps = {
  token: string
  home: Home
  formKey: number
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
  const desk = useDesk(token, home.groups, revision)
  const log = { token, home, formKey, refresh, entries: entries.state }
  return <ParticipantBody home={home} desk={desk} log={log} />
}

function useEntries(token: string) {
  const load = useCallback(() => readEntries(token), [token])
  return useAsync(load)
}

function useDesk(token: string, groups: Named[], revision: number): Desk {
  const [pane, setPane] = useState<Pane>("log")
  const [groupId, setGroupId] = useState<number | undefined>(soleGroup(groups))
  const browse = useGroupStats(token, groupId, revision)
  return { pane, setPane, groups, groupId, setGroupId, browse }
}

function soleGroup(groups: Named[]): number | undefined {
  if (groups.length === 1) return groups[0].id
  return undefined
}

function useGroupStats(token: string, groupId: number | undefined, revision: number) {
  const loadFor = useCallback((season: number | undefined) => readStats(token, season, requiredGroup(groupId)), [token, groupId, revision])
  return useSeasonBrowse(loadFor, groupId !== undefined)
}

function requiredGroup(groupId: number | undefined): number {
  if (groupId === undefined) throw new Error("missing group")
  return groupId
}

function ParticipantBody({ home, desk, log }: { home: Home; desk: Desk; log: LogProps }) {
  return (
    <Shell title={home.name} subtitle={home.group_name} trailing={<Logo />} head={<ViewTabs pane={desk.pane} onPane={desk.setPane} />}>
      <Shown pane={desk.pane} desk={desk} log={log} />
    </Shell>
  )
}

const logoWidthCap = 0.46

function Logo() {
  const ref = useRef<HTMLImageElement>(null)
  useLayoutEffect(() => trackLogo(ref.current), [])
  return <img ref={ref} className="h-0 w-auto self-end rounded-2xl" style={{ maxWidth: `${logoWidthCap * 100}%` }} src={logo} alt={text("app.title")} />
}

function trackLogo(img: HTMLImageElement | null) {
  const text = logoText(img)
  if (!img || !text) return
  const fit = () => sizeLogo(img, text)
  fit()
  img.addEventListener("load", fit)
  const observer = new ResizeObserver(fit)
  observer.observe(text)
  return () => stopLogo(img, observer, fit)
}

function logoText(img: HTMLImageElement | null) {
  const text = img?.parentElement?.firstElementChild
  if (text instanceof HTMLElement) return text
  return null
}

function stopLogo(img: HTMLImageElement, observer: ResizeObserver, fit: () => void) {
  img.removeEventListener("load", fit)
  observer.disconnect()
}

function sizeLogo(img: HTMLImageElement, text: HTMLElement) {
  const next = `${Math.round(fittedHeight(img, text))}px`
  if (img.style.height !== next) img.style.height = next
}

function fittedHeight(img: HTMLImageElement, text: HTMLElement) {
  const height = text.getBoundingClientRect().height
  const rowWidth = text.parentElement?.getBoundingClientRect().width ?? 0
  return withinCap(height, rowWidth, imageRatio(img))
}

function imageRatio(img: HTMLImageElement) {
  if (img.naturalHeight === 0) return 1.5
  return img.naturalWidth / img.naturalHeight
}

function withinCap(height: number, rowWidth: number, ratio: number) {
  const cap = rowWidth * logoWidthCap
  if (height * ratio <= cap) return height
  return cap / ratio
}

function ViewTabs({ pane, onPane }: { pane: Pane; onPane: (pane: Pane) => void }) {
  return (
    <div className="flex gap-2">
      <PaneButton label={text("view.log")} active={pane === "log"} onClick={() => onPane("log")} />
      <PaneButton label={text("view.standings")} active={pane === "standings"} onClick={() => onPane("standings")} />
    </div>
  )
}

function PaneButton({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return <button className={active ? "btn" : "btn-quiet"} type="button" onClick={onClick}>{label}</button>
}

function Shown({ pane, desk, log }: { pane: Pane; desk: Desk; log: LogProps }) {
  if (pane === "log") return <LogPane log={log} />
  return <Standings desk={desk} />
}

function LogPane({ log }: { log: LogProps }) {
  return (
    <>
      <Logging key={`${log.formKey}-${log.home.default_place ?? ""}`} token={log.token} home={log.home} onSaved={log.refresh} />
      <OwnList token={log.token} state={log.entries} places={log.home.places} onChanged={log.refresh} />
    </>
  )
}

function Standings({ desk }: { desk: Desk }) {
  return (
    <>
      <MaybePicker desk={desk} />
      <Chosen desk={desk} />
    </>
  )
}

function MaybePicker({ desk }: { desk: Desk }) {
  if (desk.groups.length < 2) return null
  return <GroupPicker groups={desk.groups} selected={desk.groupId} onSelect={desk.setGroupId} />
}

function Chosen({ desk }: { desk: Desk }) {
  if (desk.groupId === undefined) return <p className="card">{text("standings.choose")}</p>
  return <StatsBoard browse={desk.browse} />
}

function GroupPicker({ groups, selected, onSelect }: { groups: Named[]; selected?: number; onSelect: (id: number) => void }) {
  return (
    <div className="flex gap-2 overflow-x-auto">
      {groups.map((group) => <GroupButton key={group.id} group={group} selected={selected} onSelect={onSelect} />)}
    </div>
  )
}

function GroupButton({ group, selected, onSelect }: { group: Named; selected?: number; onSelect: (id: number) => void }) {
  const className = group.id === selected ? "btn" : "btn-quiet"
  return <button className={className} type="button" onClick={() => onSelect(group.id)}>{group.name}</button>
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

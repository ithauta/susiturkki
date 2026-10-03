import { useCallback, useState } from "react"
import { createGroup, logout, readGroups } from "../api/admin"
import type { Group } from "../api/types"
import { NameForm } from "../components/NameForm"
import { Shell } from "../components/Shell"
import { Status } from "../components/Status"
import { useAsync } from "../hooks/useAsync"
import { text } from "../i18n/text"
import { GroupPanel } from "./GroupPanel"
import { LoginForm } from "./LoginForm"

export function AdminPage() {
  const load = useCallback(() => readGroups(), [])
  const groups = useAsync(load)
  if (groups.state.kind === "error" && groups.state.code === "not_authenticated") return <LoginForm onSuccess={groups.reload} />
  if (groups.state.kind !== "ready") return <Shell title={text("groups.title")}><Status state={groups.state} /></Shell>
  return <GroupDesk groups={groups.state.data} reload={groups.reload} />
}

function GroupDesk({ groups, reload }: { groups: Group[]; reload: () => void }) {
  const [selected, setSelected] = useState(groups[0]?.id)
  const group = groups.find((item) => item.id === selected) ?? groups[0]
  return <Shell title={text("groups.title")} action={<Logout onDone={reload} />}><Desk groups={groups} group={group} reload={reload} onSelect={setSelected} /></Shell>
}

function Desk({ groups, group, reload, onSelect }: { groups: Group[]; group?: Group; reload: () => void; onSelect: (id: number) => void }) {
  return (
    <>
      <NameForm label={text("groups.name")} submitLabel={text("groups.create")} onSubmit={(name) => addGroup(name, onSelect, reload)} />
      <GroupChoices groups={groups} selected={group?.id} onSelect={onSelect} />
      {group ? <GroupPanel key={group.id} group={group} reload={reload} /> : null}
    </>
  )
}

function GroupChoices({ groups, selected, onSelect }: { groups: Group[]; selected?: number; onSelect: (id: number) => void }) {
  return (
    <div className="flex gap-2 overflow-x-auto">
      {groups.map((group) => <GroupChoice key={group.id} group={group} selected={selected} onSelect={onSelect} />)}
    </div>
  )
}

function GroupChoice({ group, selected, onSelect }: { group: Group; selected?: number; onSelect: (id: number) => void }) {
  const className = group.id === selected ? "btn" : "btn-quiet"
  return <button className={className} type="button" onClick={() => onSelect(group.id)}>{group.name}</button>
}

async function addGroup(name: string, setSelected: (id: number) => void, reload: () => void) {
  const created = await createGroup(name)
  setSelected(created.id)
  reload()
}

function Logout({ onDone }: { onDone: () => void }) {
  return <button className="btn-quiet" type="button" onClick={() => leave(onDone)}>{text("login.out")}</button>
}

async function leave(onDone: () => void) {
  await logout()
  onDone()
}

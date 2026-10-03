import { useCallback } from "react"
import { deleteGroup, readAdminEntries, readAdminStats, renameGroup } from "../api/admin"
import type { Group } from "../api/types"
import { ConfirmButton } from "../components/ConfirmButton"
import { RenameForm } from "../components/NameForm"
import { StatsBoard } from "../components/StatsBoard"
import { useAsync } from "../hooks/useAsync"
import { useSeasonBrowse } from "../hooks/useSeasonBrowse"
import { text } from "../i18n/text"
import { AdminEntries } from "./AdminEntries"
import { Members } from "./Members"

export function GroupPanel({ group, reload }: { group: Group; reload: () => void }) {
  return (
    <>
      <GroupTitle group={group} reload={reload} />
      <Members group={group} reload={reload} />
      <GroupLog group={group} />
    </>
  )
}

function GroupTitle({ group, reload }: { group: Group; reload: () => void }) {
  return (
    <section className="card">
      <RenameForm key={group.name} name={group.name} label={text("groups.name")} onSubmit={(name) => rename(group.id, name, reload)} />
      <div className="mt-3"><DeleteGroup groupId={group.id} reload={reload} /></div>
    </section>
  )
}

function DeleteGroup({ groupId, reload }: { groupId: number; reload: () => void }) {
  return <ConfirmButton label={text("groups.delete")} confirm={text("groups.confirmDelete")} onConfirm={() => remove(groupId, reload)} />
}

function GroupLog({ group }: { group: Group }) {
  const entries = useEntries(group.id)
  const stats = useStats(group.id)
  return (
    <>
      <AdminEntries group={group} state={entries.state} reload={entries.reload} />
      <StatsBoard browse={stats} />
    </>
  )
}

function useEntries(groupId: number) {
  const load = useCallback(() => readAdminEntries(groupId), [groupId])
  return useAsync(load)
}

function useStats(groupId: number) {
  const loadFor = useCallback((season: number | undefined) => readAdminStats(groupId, season), [groupId])
  return useSeasonBrowse(loadFor)
}

async function rename(groupId: number, name: string, reload: () => void) {
  await renameGroup(groupId, name)
  reload()
}

async function remove(groupId: number, reload: () => void) {
  await deleteGroup(groupId)
  reload()
}

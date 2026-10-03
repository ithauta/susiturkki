import { type FocusEvent, useState } from "react"
import { createMember, deleteMember, renameMember, renewLink } from "../api/admin"
import { participantLink } from "../api/paths"
import type { Group, Participant } from "../api/types"
import { ConfirmButton } from "../components/ConfirmButton"
import { NameForm, RenameForm } from "../components/NameForm"
import { text } from "../i18n/text"

export function Members({ group, reload }: { group: Group; reload: () => void }) {
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{text("members.title")}</h2>
      <ul>{group.participants.map((member) => <MemberRow key={member.id} member={member} reload={reload} />)}</ul>
      <NameForm label={text("members.name")} submitLabel={text("members.add")} onSubmit={(name) => add(group.id, name, reload)} />
    </section>
  )
}

function MemberRow({ member, reload }: { member: Participant; reload: () => void }) {
  return (
    <li className="mt-4 border-t border-ice pt-4">
      <RenameForm key={member.name} name={member.name} label={text("members.name")} onSubmit={(name) => rename(member.id, name, reload)} />
      <MemberLink token={member.token} />
      <MemberActions memberId={member.id} reload={reload} />
    </li>
  )
}

function MemberActions({ memberId, reload }: { memberId: number; reload: () => void }) {
  return (
    <div className="mt-3 flex flex-wrap gap-2">
      <button className="btn-quiet" type="button" onClick={() => renew(memberId, reload)}>{text("members.renew")}</button>
      <ConfirmButton label={text("members.delete")} confirm={text("members.confirmDelete")} onConfirm={() => remove(memberId, reload)} />
    </div>
  )
}

function MemberLink({ token }: { token: string }) {
  const link = participantLink(token)
  const [note, setNote] = useState("")
  return (
    <div className="mt-2">
      <LinkValue link={link} />
      <CopyLink link={link} note={note} setNote={setNote} />
    </div>
  )
}

function LinkValue({ link }: { link: string }) {
  return <input className="field" readOnly value={link} onFocus={selectInput} aria-label={text("members.link")} />
}

function CopyLink({ link, note, setNote }: { link: string; note: string; setNote: (note: string) => void }) {
  return (
    <>
      <button className="btn-quiet mt-2" type="button" onClick={() => copy(link, setNote)}>{text("members.link")}</button>
      <p className="mt-1 text-sm">{note}</p>
    </>
  )
}

function selectInput(event: FocusEvent<HTMLInputElement>) {
  event.currentTarget.select()
}

async function copy(link: string, setNote: (note: string) => void) {
  try {
    await navigator.clipboard.writeText(link)
    setNote(text("members.copied"))
  } catch {
    setNote(text("members.copyFailed"))
  }
}

async function add(groupId: number, name: string, reload: () => void) {
  await createMember(groupId, name)
  reload()
}

async function rename(participantId: number, name: string, reload: () => void) {
  await renameMember(participantId, name)
  reload()
}

async function renew(participantId: number, reload: () => void) {
  await renewLink(participantId)
  reload()
}

async function remove(participantId: number, reload: () => void) {
  await deleteMember(participantId)
  reload()
}

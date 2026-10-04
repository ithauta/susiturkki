import { type FocusEvent, type FormEvent, useCallback, useState } from "react"
import { attachMember, createMember, deleteMember, readPersons, renameMember, renewLink } from "../api/admin"
import { errorCode } from "../api/client"
import { participantLink } from "../api/paths"
import type { Group, Participant, Person } from "../api/types"
import { ConfirmButton } from "../components/ConfirmButton"
import { Field } from "../components/Field"
import { PersonNameForm, PersonRenameForm } from "../components/PersonNameForm"
import { ErrorText } from "../components/Status"
import { useAsync } from "../hooks/useAsync"
import type { LoadState } from "../hooks/useAsync"
import { text } from "../i18n/text"

export function Members({ group, reload }: { group: Group; reload: () => void }) {
  const people = usePeople()
  const refresh = () => refreshMembers(reload, people.reload)
  return <MemberSection group={group} people={people.state} refresh={refresh} />
}

function MemberSection({ group, people, refresh }: { group: Group; people: LoadState<Person[]>; refresh: () => void }) {
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{text("members.title")}</h2>
      <MemberRows group={group} refresh={refresh} />
      <PersonNameForm submitLabel={text("members.add")} onSubmit={(given, family) => add(group.id, given, family, refresh)} />
      <AttachPerson group={group} people={people} reload={refresh} />
    </section>
  )
}

function MemberRows({ group, refresh }: { group: Group; refresh: () => void }) {
  return <ul>{group.participants.map((member) => <MemberRow key={member.id} member={member} reload={refresh} />)}</ul>
}

function usePeople() {
  const load = useCallback(() => readPersons(), [])
  return useAsync(load)
}

function refreshMembers(reload: () => void, reloadPeople: () => void) {
  reload()
  reloadPeople()
}

function AttachPerson({ group, people, reload }: { group: Group; people: LoadState<Person[]>; reload: () => void }) {
  if (people.kind !== "ready") return null
  const choices = outside(group, people.data)
  if (choices.length === 0) return null
  return <AttachForm key={choiceKey(choices)} groupId={group.id} choices={choices} reload={reload} />
}

function outside(group: Group, people: Person[]): Person[] {
  const ids = new Set(group.participants.map((member) => member.person_id))
  return people.filter((person) => !ids.has(person.id))
}

function choiceKey(choices: Person[]): string {
  return choices.map((person) => person.id).join("-")
}

function MemberRow({ member, reload }: { member: Participant; reload: () => void }) {
  return (
    <li className="mt-4 border-t border-ice pt-4">
      <PersonRenameForm key={`${member.given_name}-${member.family_name}`} given={member.given_name} family={member.family_name} onSubmit={(given, family) => rename(member.id, given, family, reload)} />
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

async function add(groupId: number, given: string, family: string, reload: () => void) {
  await createMember(groupId, given, family)
  reload()
}

async function rename(participantId: number, given: string, family: string, reload: () => void) {
  await renameMember(participantId, given, family)
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

function AttachForm({ groupId, choices, reload }: { groupId: number; choices: Person[]; reload: () => void }) {
  const [personId, setPersonId] = useState(choices[0].id)
  const [code, setCode] = useState("")
  const save = (event: FormEvent) => submitAttach(event, groupId, personId, reload, setCode)
  return <AttachFields choices={choices} personId={personId} code={code} onChange={setPersonId} onSubmit={save} />
}

function AttachFields({ choices, personId, code, onChange, onSubmit }: { choices: Person[]; personId: number; code: string; onChange: (id: number) => void; onSubmit: (event: FormEvent) => void }) {
  return (
    <form className="mt-4" onSubmit={onSubmit}>
      <PersonChoice choices={choices} personId={personId} onChange={onChange} />
      <button className="btn mt-3" type="submit">{text("members.attach")}</button>
      <ErrorText code={code} />
    </form>
  )
}

function PersonChoice({ choices, personId, onChange }: { choices: Person[]; personId: number; onChange: (id: number) => void }) {
  return (
    <Field label={text("members.existing")}>
      <select className="field" value={personId} onChange={(event) => onChange(Number(event.target.value))}>
        {choices.map((person) => <option key={person.id} value={person.id}>{person.name}</option>)}
      </select>
    </Field>
  )
}

async function submitAttach(event: FormEvent, groupId: number, personId: number, reload: () => void, setCode: (code: string) => void) {
  event.preventDefault()
  try {
    await attachMember(groupId, personId)
    setCode("")
    reload()
  } catch (error) {
    setCode(errorCode(error))
  }
}

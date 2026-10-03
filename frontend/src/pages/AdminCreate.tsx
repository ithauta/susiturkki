import { useState } from "react"
import { createAdminEntry } from "../api/admin"
import type { EntryBody, Group } from "../api/types"
import { EntryForm } from "../components/EntryForm"
import { text } from "../i18n/text"

export function AdminCreate({ group, places, reload }: { group: Group; places: string[]; reload: () => void }) {
  const [participantId, setParticipantId] = useState(group.participants[0]?.id ?? 0)
  if (group.participants.length === 0) return null
  return (
    <div className="mt-4">
      <MemberSelect members={group.participants} value={participantId} onChange={setParticipantId} />
      <EntryForm listId={`new-${group.id}`} places={places} submitLabel={text("entry.save")} onSubmit={(body) => save(group.id, participantId, body, reload)} />
    </div>
  )
}

function MemberSelect({ members, value, onChange }: { members: Group["participants"]; value: number; onChange: (id: number) => void }) {
  return (
    <label className="block text-sm font-medium">
      <span>{text("members.name")}</span>
      <select className="field" value={value} onChange={(event) => onChange(Number(event.target.value))}>
        {members.map((member) => <option key={member.id} value={member.id}>{member.name}</option>)}
      </select>
    </label>
  )
}

async function save(groupId: number, participantId: number, body: EntryBody, reload: () => void) {
  await createAdminEntry(groupId, { ...body, participant_id: participantId })
  reload()
}

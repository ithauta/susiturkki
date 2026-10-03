import type { MemberRecent, RecentSki } from "../api/types"
import { finnishKilometers } from "../format/labels"
import { finnishDate } from "../format/time"
import { text } from "../i18n/text"

export function RecentList({ recent }: { recent: MemberRecent[] }) {
  return (
    <section className="card">
      <h2 className="text-lg font-semibold">{text("season.recent")}</h2>
      {recent.map((member) => <RecentMember key={member.participant_id} member={member} />)}
    </section>
  )
}

function RecentMember({ member }: { member: MemberRecent }) {
  return (
    <div className="mt-4">
      <h3 className="font-medium">{member.name}</h3>
      <RecentRows entries={member.entries} />
    </div>
  )
}

function RecentRows({ entries }: { entries: RecentSki[] }) {
  if (entries.length === 0) return <p className="text-sm">{text("entries.empty")}</p>
  return <ul>{entries.map((entry, index) => <RecentRow key={index} entry={entry} />)}</ul>
}

function RecentRow({ entry }: { entry: RecentSki }) {
  return (
    <li className="mt-1 flex justify-between gap-3 text-sm">
      <span>{finnishDate(entry.performed_on)}</span>
      <span>{finnishKilometers(entry.kilometers)} {text("entry.unit")}</span>
      <span className="truncate">{entry.place ?? ""}</span>
    </li>
  )
}

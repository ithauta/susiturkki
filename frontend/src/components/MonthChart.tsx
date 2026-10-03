import { Bar, BarChart, Legend, Tooltip, XAxis, YAxis } from "recharts"
import type { MemberKilometers, PeriodStats } from "../api/types"
import { memberColor } from "../charts/colors"
import { kilometersTip } from "../charts/tip"
import { monthLabel } from "../format/labels"
import { periodRows } from "../format/rows"
import { text } from "../i18n/text"
import { ChartCard, ChartFrame, EmptyChart } from "./ChartCard"

type PeriodProps = { periods: PeriodStats[]; members: MemberKilometers[] }

export function MonthChart({ periods, members }: PeriodProps) {
  if (members.length === 0) return <EmptyChart title={text("season.months")} />
  return <ChartCard title={text("season.months")}><MonthBars periods={periods} members={members} /></ChartCard>
}

function MonthBars({ periods, members }: PeriodProps) {
  return (
    <ChartFrame>
      <BarChart data={periodRows(periods, monthLabel)}>
        <XAxis dataKey="label" /><YAxis /><Tooltip formatter={kilometersTip} /><Legend />
        {members.map(memberBar)}
      </BarChart>
    </ChartFrame>
  )
}

function memberBar(member: MemberKilometers, index: number) {
  return <Bar key={member.participant_id} dataKey={String(member.participant_id)} name={member.name} fill={memberColor(index)} radius={4} />
}

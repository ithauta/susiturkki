import { Legend, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts"
import type { MemberKilometers, PeriodStats } from "../api/types"
import { memberColor } from "../charts/colors"
import { kilometersTip } from "../charts/tip"
import { weekLabel } from "../format/labels"
import { periodRows } from "../format/rows"
import { text } from "../i18n/text"
import { ChartCard, ChartFrame, EmptyChart } from "./ChartCard"

type PeriodProps = { periods: PeriodStats[]; members: MemberKilometers[] }

export function WeekChart({ periods, members }: PeriodProps) {
  if (members.length === 0) return <EmptyChart title={text("season.weeks")} />
  return <ChartCard title={text("season.weeks")}><WeekScroll periods={periods} members={members} /></ChartCard>
}

function WeekScroll({ periods, members }: PeriodProps) {
  return (
    <div className="h-full overflow-x-auto">
      <div className="h-full" style={{ width: chartWidth(periods.length) }}>
        <WeekLines periods={periods} members={members} />
      </div>
    </div>
  )
}

function chartWidth(count: number): number {
  return Math.max(count * 36, 280)
}

function WeekLines({ periods, members }: PeriodProps) {
  return (
    <ChartFrame>
      <LineChart data={periodRows(periods, weekLabel)}>
        <XAxis dataKey="label" /><YAxis /><Tooltip formatter={kilometersTip} /><Legend />
        {members.map(memberLine)}
      </LineChart>
    </ChartFrame>
  )
}

function memberLine(member: MemberKilometers, index: number) {
  return <Line key={member.participant_id} type="monotone" dataKey={String(member.participant_id)} name={member.name} stroke={memberColor(index)} dot={false} />
}

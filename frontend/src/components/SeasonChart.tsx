import { Bar, BarChart, Tooltip, XAxis, YAxis } from "recharts"
import type { MemberKilometers } from "../api/types"
import { memberColor } from "../charts/colors"
import { kilometersTip } from "../charts/tip"
import { totalRows } from "../format/rows"
import { text } from "../i18n/text"
import { ChartCard, ChartFrame, EmptyChart } from "./ChartCard"

export function SeasonChart({ totals }: { totals: MemberKilometers[] }) {
  if (totals.length === 0) return <EmptyChart title={text("season.totals")} />
  return <ChartCard title={text("season.totals")}><TotalBars totals={totals} /></ChartCard>
}

function TotalBars({ totals }: { totals: MemberKilometers[] }) {
  return (
    <ChartFrame>
      <BarChart data={totalRows(totals)} layout="vertical" margin={{ left: 16, right: 8 }}>
        <XAxis type="number" /><YAxis type="category" dataKey="label" width={104} />
        <Tooltip formatter={kilometersTip} /><Bar dataKey="kilometers" fill={memberColor(0)} radius={6} />
      </BarChart>
    </ChartFrame>
  )
}

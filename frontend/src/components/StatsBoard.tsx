import type { SeasonStats } from "../api/types"
import type { LoadState } from "../hooks/useAsync"
import { Status } from "./Status"
import { MonthChart } from "./MonthChart"
import { RecentList } from "./RecentList"
import { SeasonChart } from "./SeasonChart"
import { SeasonNav } from "./SeasonNav"
import { WeekChart } from "./WeekChart"

type Browse = { state: LoadState<SeasonStats>; limit: number | undefined; setSeason: (season: number) => void }

export function StatsBoard({ browse }: { browse: Browse }) {
  if (browse.state.kind !== "ready") return <Status state={browse.state} />
  return <SeasonView stats={browse.state.data} limit={browse.limit} onSeason={browse.setSeason} />
}

function SeasonView({ stats, limit, onSeason }: { stats: SeasonStats; limit: number | undefined; onSeason: (season: number) => void }) {
  return (
    <>
      <SeasonNav shown={stats.season} limit={limit} onSeason={onSeason} />
      <SeasonChart totals={stats.season_totals} />
      <PeriodCharts stats={stats} />
      <RecentList recent={stats.recent} />
    </>
  )
}

function PeriodCharts({ stats }: { stats: SeasonStats }) {
  return (
    <>
      <MonthChart periods={stats.months} members={stats.season_totals} />
      <WeekChart periods={stats.weeks} members={stats.season_totals} />
    </>
  )
}

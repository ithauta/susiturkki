import type { MemberKilometers, PeriodStats } from "../api/types"

export type ChartRow = { label: string; [key: string]: string | number }

export function periodRows(periods: PeriodStats[], labelFor: (key: string) => string): ChartRow[] {
  return periods.map((period) => periodRow(period, labelFor))
}

export function totalRows(totals: MemberKilometers[]): ChartRow[] {
  return totals.map(totalRow)
}

function periodRow(period: PeriodStats, labelFor: (key: string) => string): ChartRow {
  return period.members.reduce(addMember, { label: labelFor(period.key) })
}

function addMember(row: ChartRow, member: MemberKilometers): ChartRow {
  return { ...row, [member.participant_id]: Number(member.kilometers) }
}

function totalRow(member: MemberKilometers): ChartRow {
  return { label: member.name, kilometers: Number(member.kilometers) }
}

import type { Entry } from "../api/types"
import { fill, text } from "../i18n/text"

export function finnishKilometers(value: string): string {
  return value.replace(".", ",")
}

export function distanceForApi(value: string): string {
  return value.trim().replace(",", ".")
}

export function monthLabel(key: string): string {
  return text(`month.${Number(key.slice(5, 7))}`)
}

export function weekLabel(key: string): string {
  return fill("week.of", { day: String(Number(key.slice(8, 10))), month: text(`month.short.${Number(key.slice(5, 7))}`) })
}

export function seasonLabel(start: number): string {
  return fill("season.range", { start: String(start), end: String(start + 1) })
}

export function uniquePlaces(entries: Entry[]): string[] {
  return entries.reduce(addPlace, [] as string[])
}

function addPlace(seen: string[], entry: Entry): string[] {
  if (entry.place && !seen.includes(entry.place)) seen.push(entry.place)
  return seen
}

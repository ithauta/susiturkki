import { finnishKilometers } from "../format/labels"
import { text } from "../i18n/text"

export function kilometersTip(value: unknown): string {
  const number = typeof value === "number" ? value : Number(value)
  return `${finnishKilometers(number.toFixed(1))} ${text("entry.unit")}`
}

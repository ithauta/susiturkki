export function helsinkiInput(moment = new Date()): string {
  return inputFrom(helsinkiParts(moment))
}

export function inputFromIso(iso: string): string {
  return inputFrom(helsinkiParts(new Date(iso)))
}

export function finnishMoment(iso: string): string {
  return new Intl.DateTimeFormat("fi-FI", momentOptions()).format(new Date(iso))
}

export function finnishDate(isoDate: string): string {
  const [year, month, day] = isoDate.split("-")
  return `${Number(day)}.${Number(month)}.${year}`
}

function inputFrom(parts: Intl.DateTimeFormatPart[]): string {
  const date = `${piece(parts, "year")}-${piece(parts, "month")}-${piece(parts, "day")}`
  return `${date}T${piece(parts, "hour")}:${piece(parts, "minute")}`
}

function piece(parts: Intl.DateTimeFormatPart[], type: string): string {
  return parts.find((item) => item.type === type)?.value ?? ""
}

function helsinkiParts(moment: Date): Intl.DateTimeFormatPart[] {
  return new Intl.DateTimeFormat("sv-SE", helsinkiOptions()).formatToParts(moment)
}

function helsinkiOptions(): Intl.DateTimeFormatOptions {
  return { timeZone: "Europe/Helsinki", ...clockParts(), hourCycle: "h23" }
}

function clockParts(): Intl.DateTimeFormatOptions {
  return { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }
}

function momentOptions(): Intl.DateTimeFormatOptions {
  return {
    timeZone: "Europe/Helsinki",
    day: "numeric",
    month: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }
}

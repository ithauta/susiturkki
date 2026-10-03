import { fi } from "./fi"

export function text(key: string): string {
  if (key in fi) return fi[key as keyof typeof fi]
  return fi["error.unknown"]
}

export function fill(key: string, values: Record<string, string>): string {
  return Object.entries(values).reduce(replace, text(key))
}

function replace(template: string, entry: [string, string]): string {
  return template.replace(`{${entry[0]}}`, entry[1])
}

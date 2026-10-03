export function participantPath(token: string, suffix = ""): string {
  return `/api/p/${encodeURIComponent(token)}${suffix}`
}

export function groupPath(groupId: number, suffix = ""): string {
  return `/api/admin/groups/${groupId}${suffix}`
}

export function seasonQuery(season: number | undefined): string {
  if (season === undefined) return ""
  return `?season=${season}`
}

export function participantLink(token: string): string {
  return `${window.location.origin}/p/${encodeURIComponent(token)}`
}

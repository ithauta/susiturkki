export function participantPath(token: string, suffix = ""): string {
  return `/api/p/${encodeURIComponent(token)}${suffix}`
}

export function groupPath(groupId: number, suffix = ""): string {
  return `/api/admin/groups/${groupId}${suffix}`
}

export function seasonQuery(season: number | undefined): string {
  return queryString(season, undefined)
}

export function statsQuery(season: number | undefined, groupId: number | undefined): string {
  return queryString(season, groupId)
}

function queryString(season: number | undefined, groupId: number | undefined): string {
  const params = new URLSearchParams()
  setNumber(params, "season", season)
  setNumber(params, "group_id", groupId)
  const query = params.toString()
  return query ? `?${query}` : ""
}

function setNumber(params: URLSearchParams, key: string, value: number | undefined) {
  if (value !== undefined) params.set(key, String(value))
}

export function participantLink(token: string): string {
  return `${window.location.origin}/p/${encodeURIComponent(token)}`
}

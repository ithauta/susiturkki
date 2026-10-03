import { readJson, sendJson } from "./client"
import { participantPath, statsQuery } from "./paths"
import type { Entry, EntryBody, Home, SeasonStats } from "./types"

export function readHome(token: string): Promise<Home> {
  return readJson(participantPath(token))
}

export function readEntries(token: string): Promise<Entry[]> {
  return readJson(participantPath(token, "/entries"))
}

export function readStats(token: string, season: number | undefined, groupId: number): Promise<SeasonStats> {
  return readJson(participantPath(token, `/stats${statsQuery(season, groupId)}`))
}

export async function createEntry(token: string, body: EntryBody): Promise<Entry> {
  const response = await sendJson(participantPath(token, "/entries"), "POST", body)
  return response.json() as Promise<Entry>
}

export async function updateEntry(token: string, entryId: number, body: EntryBody): Promise<Entry> {
  const response = await sendJson(participantPath(token, `/entries/${entryId}`), "PATCH", body)
  return response.json() as Promise<Entry>
}

export function deleteEntry(token: string, entryId: number): Promise<Response> {
  return sendJson(participantPath(token, `/entries/${entryId}`), "DELETE")
}

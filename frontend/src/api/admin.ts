import { readJson, sendJson } from "./client"
import { groupPath, seasonQuery } from "./paths"
import type { Entry, EntryBody, Group, Named, Participant, SeasonStats } from "./types"

export function login(password: string): Promise<Response> {
  return sendJson("/api/admin/login", "POST", { password })
}

export function logout(): Promise<Response> {
  return sendJson("/api/admin/logout", "POST")
}

export function readGroups(): Promise<Group[]> {
  return readJson("/api/admin/groups")
}

export async function createGroup(name: string): Promise<Named> {
  const response = await sendJson("/api/admin/groups", "POST", { name })
  return response.json() as Promise<Named>
}

export function renameGroup(groupId: number, name: string): Promise<Response> {
  return sendJson(groupPath(groupId), "PATCH", { name })
}

export function deleteGroup(groupId: number): Promise<Response> {
  return sendJson(groupPath(groupId), "DELETE")
}

export async function createMember(groupId: number, name: string): Promise<Participant> {
  const response = await sendJson(groupPath(groupId, "/participants"), "POST", { name })
  return response.json() as Promise<Participant>
}

export function renameMember(participantId: number, name: string): Promise<Response> {
  return sendJson(`/api/admin/participants/${participantId}`, "PATCH", { name })
}

export function deleteMember(participantId: number): Promise<Response> {
  return sendJson(`/api/admin/participants/${participantId}`, "DELETE")
}

export async function renewLink(participantId: number): Promise<Participant> {
  const response = await sendJson(`/api/admin/participants/${participantId}/link`, "POST")
  return response.json() as Promise<Participant>
}

export function readAdminEntries(groupId: number): Promise<Entry[]> {
  return readJson(groupPath(groupId, "/entries"))
}

export function createAdminEntry(groupId: number, body: EntryBody & { participant_id: number }): Promise<Response> {
  return sendJson(groupPath(groupId, "/entries"), "POST", body)
}

export function updateAdminEntry(entryId: number, body: EntryBody): Promise<Response> {
  return sendJson(`/api/admin/entries/${entryId}`, "PATCH", body)
}

export function deleteAdminEntry(entryId: number): Promise<Response> {
  return sendJson(`/api/admin/entries/${entryId}`, "DELETE")
}

export function readAdminStats(groupId: number, season?: number): Promise<SeasonStats> {
  return readJson(`${groupPath(groupId, "/stats")}${seasonQuery(season)}`)
}

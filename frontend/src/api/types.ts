export type Home = {
  group_id: number
  group_name: string
  groups: Named[]
  participant_id: number
  name: string
  default_place: string | null
  places: string[]
  can_create: boolean
}

export type Entry = {
  id: number
  participant_id: number
  performed_at: string
  kilometers: string
  place: string | null
  created_at: string
  style: string
  conditions: string
  can_edit?: boolean
}

export type EntryBody = {
  performed_at: string
  distance_km: string
  place: string | null
  style: string
  conditions: string
}

export type ProfileBody = {
  birth_year: number | null
  distance_km: string | null
  target_on: string | null
}

export type Profile = {
  birth_year: number | null
  season: number
  kilometers: string | null
  target_on: string | null
  kilometers_editable: boolean
}

export type MemberKilometers = {
  participant_id: number
  name: string
  kilometers: string
}

export type PeriodStats = {
  key: string
  members: MemberKilometers[]
}

export type RecentSki = {
  performed_on: string
  kilometers: string
  place: string | null
  style: string
  conditions: string
}

export type MemberRecent = {
  participant_id: number
  name: string
  entries: RecentSki[]
}

export type SeasonStats = {
  season: number
  can_create: boolean
  season_totals: MemberKilometers[]
  months: PeriodStats[]
  weeks: PeriodStats[]
  recent: MemberRecent[]
}

export type Person = {
  id: number
  given_name: string
  family_name: string
  name: string
  token: string
}

export type Participant = {
  id: number
  group_id: number
  person_id: number
  given_name: string
  family_name: string
  name: string
  token: string
}

export type Group = {
  id: number
  name: string
  participants: Participant[]
}

export type Named = {
  id: number
  name: string
}

import { type FormEvent, useState } from "react"
import { errorCode } from "../api/client"
import type { EntryBody } from "../api/types"
import { distanceForApi } from "../format/labels"
import { helsinkiInput } from "../format/time"
import { text } from "../i18n/text"
import { ErrorText } from "./Status"
import { Field } from "./Field"

export type EntryDraft = { performed_at: string; distance_km: string; place: string }

type EntryFormProps = {
  initial?: EntryDraft
  places: string[]
  listId: string
  submitLabel: string
  onSubmit: (body: EntryBody) => Promise<void>
}

export function EntryForm({ initial, places, listId, submitLabel, onSubmit }: EntryFormProps) {
  const form = useDraft(initial)
  return (
    <form className="card" onSubmit={(event) => saveDraft(event, form, onSubmit)}>
      <EntryFields form={form} places={places} listId={listId} />
      <button className="btn mt-4 w-full" type="submit">{submitLabel}</button>
    </form>
  )
}

function EntryFields({ form, places, listId }: { form: ReturnType<typeof useDraft>; places: string[]; listId: string }) {
  return (
    <>
      <WhenField value={form.performed} onChange={form.setPerformed} />
      <DistanceField value={form.distance} onChange={form.setDistance} />
      <PlaceField value={form.place} places={places} listId={listId} onChange={form.setPlace} />
      <ErrorText code={form.code} />
    </>
  )
}

export function entryDraft(performed: string, distance: string, place: string): EntryBody {
  return { performed_at: performed, distance_km: distanceForApi(distance), place: place.trim() || null }
}

function useDraft(initial?: EntryDraft) {
  const [performed, setPerformed] = useState(initial?.performed_at ?? helsinkiInput())
  const [distance, setDistance] = useState(initial?.distance_km ?? "")
  const [place, setPlace] = useState(initial?.place ?? "")
  const [code, setCode] = useState("")
  return { performed, setPerformed, distance, setDistance, place, setPlace, code, setCode }
}

async function saveDraft(event: FormEvent, form: ReturnType<typeof useDraft>, onSubmit: (body: EntryBody) => Promise<void>) {
  event.preventDefault()
  form.setCode("")
  try {
    await onSubmit(entryDraft(form.performed, form.distance, form.place))
  } catch (error) {
    form.setCode(errorCode(error))
  }
}

function WhenField({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <Field label={text("entry.when")}>
      <input className="field" type="datetime-local" value={value} onChange={(event) => onChange(event.target.value)} required />
    </Field>
  )
}

function DistanceField({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <Field label={text("entry.distance")}>
      <input className="field" inputMode="decimal" value={value} onChange={(event) => onChange(event.target.value)} required />
    </Field>
  )
}

function PlaceField({ value, places, listId, onChange }: { value: string; places: string[]; listId: string; onChange: (value: string) => void }) {
  return (
    <Field label={text("entry.place")}>
      <input className="field" list={listId} value={value} onChange={(event) => onChange(event.target.value)} autoComplete="off" />
      <PlaceOptions listId={listId} places={places} />
    </Field>
  )
}

function PlaceOptions({ listId, places }: { listId: string; places: string[] }) {
  return <datalist id={listId}>{places.map((place) => <option key={place} value={place} />)}</datalist>
}

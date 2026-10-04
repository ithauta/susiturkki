import { type FormEvent, useCallback, useState } from "react"
import { errorCode } from "../api/client"
import { readProfile, saveProfile } from "../api/participant"
import type { Profile } from "../api/types"
import { Field } from "../components/Field"
import { ErrorText, Status } from "../components/Status"
import { distanceForApi } from "../format/labels"
import { useAsync } from "../hooks/useAsync"
import { text } from "../i18n/text"

export function DetailsPane({ token }: { token: string }) {
  const load = useCallback(() => readProfile(token), [token])
  const profile = useAsync(load)
  if (profile.state.kind !== "ready") return <Status state={profile.state} />
  return <DetailsForm key={formKey(profile.state.data)} token={token} profile={profile.state.data} reload={profile.reload} />
}

function formKey(profile: Profile): string {
  return `${profile.birth_year ?? ""}-${profile.kilometers ?? ""}-${profile.target_on ?? ""}`
}

function DetailsForm({ token, profile, reload }: { token: string; profile: Profile; reload: () => void }) {
  const form = useDetails(profile)
  return (
    <form className="card" onSubmit={(event) => saveDetails(event, token, form, reload)}>
      <DetailFields form={form} editable={profile.kilometers_editable} />
      <button className="btn mt-4 w-full" type="submit">{text("profile.save")}</button>
    </form>
  )
}

function useDetails(profile: Profile) {
  const [birthYear, setBirthYear] = useState(profile.birth_year === null ? "" : String(profile.birth_year))
  const [kilometers, setKilometers] = useState(profile.kilometers ?? "")
  const [targetOn, setTargetOn] = useState(profile.target_on ?? "")
  const [code, setCode] = useState("")
  return { birthYear, setBirthYear, kilometers, setKilometers, targetOn, setTargetOn, code, setCode }
}

function DetailFields({ form, editable }: { form: ReturnType<typeof useDetails>; editable: boolean }) {
  return (
    <>
      <BirthField value={form.birthYear} onChange={form.setBirthYear} />
      <GoalFields form={form} editable={editable} />
      <ErrorText code={form.code} />
    </>
  )
}

function GoalFields({ form, editable }: { form: ReturnType<typeof useDetails>; editable: boolean }) {
  return (
    <>
      <KmField value={form.kilometers} editable={editable} onChange={form.setKilometers} />
      <LockedNote editable={editable} />
      <DateField value={form.targetOn} required={hasKilometers(form)} disabled={dateLocked(form, editable)} onChange={form.setTargetOn} />
    </>
  )
}

function BirthField({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <Field label={text("profile.birthYear")}>
      <input className="field" inputMode="numeric" value={value} onChange={(event) => onChange(event.target.value)} />
    </Field>
  )
}

function KmField({ value, editable, onChange }: { value: string; editable: boolean; onChange: (value: string) => void }) {
  return (
    <Field label={text("profile.goal")}>
      <input className="field" inputMode="decimal" value={value} disabled={!editable} onChange={(event) => onChange(event.target.value)} />
    </Field>
  )
}

function DateField({ value, required, disabled, onChange }: { value: string; required: boolean; disabled: boolean; onChange: (value: string) => void }) {
  return (
    <Field label={text("profile.target")}>
      <input className="field" type="date" value={value} required={required} disabled={disabled} onChange={(event) => onChange(event.target.value)} />
    </Field>
  )
}

function LockedNote({ editable }: { editable: boolean }) {
  if (editable) return null
  return <p className="mt-2 text-sm text-ice">{text("profile.kmClosed")}</p>
}

function hasKilometers(form: ReturnType<typeof useDetails>): boolean {
  return form.kilometers.trim() !== ""
}

function dateLocked(form: ReturnType<typeof useDetails>, editable: boolean): boolean {
  return !editable && !hasKilometers(form)
}

async function saveDetails(event: FormEvent, token: string, form: ReturnType<typeof useDetails>, reload: () => void) {
  event.preventDefault()
  form.setCode("")
  try {
    await saveProfile(token, bodyOf(form))
    reload()
  } catch (error) {
    form.setCode(errorCode(error))
  }
}

function bodyOf(form: ReturnType<typeof useDetails>) {
  return {
    birth_year: form.birthYear === "" ? null : Number(form.birthYear),
    distance_km: form.kilometers.trim() === "" ? null : distanceForApi(form.kilometers),
    target_on: form.targetOn === "" ? null : form.targetOn,
  }
}

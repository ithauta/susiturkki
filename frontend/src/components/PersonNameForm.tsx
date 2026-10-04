import { type FormEvent, useState } from "react"
import { errorCode } from "../api/client"
import { text } from "../i18n/text"
import { Field } from "./Field"
import { ErrorText } from "./Status"

export function PersonNameForm({ submitLabel, onSubmit }: { submitLabel: string; onSubmit: (given: string, family: string) => Promise<void> }) {
  const form = useNames("", "")
  return <NamesForm form={form} className="card" submitLabel={submitLabel} onSubmit={onSubmit} />
}

export function PersonRenameForm({ given, family, onSubmit }: { given: string; family: string; onSubmit: (given: string, family: string) => Promise<void> }) {
  const form = useNames(given, family)
  return <NamesForm form={form} className="" submitLabel={text("groups.rename")} onSubmit={onSubmit} />
}

function useNames(given: string, family: string) {
  const [givenName, setGivenName] = useState(given)
  const [familyName, setFamilyName] = useState(family)
  const [code, setCode] = useState("")
  return { givenName, setGivenName, familyName, setFamilyName, code, setCode }
}

function NamesForm({ form, className, submitLabel, onSubmit }: { form: ReturnType<typeof useNames>; className: string; submitLabel: string; onSubmit: (given: string, family: string) => Promise<void> }) {
  return (
    <form className={className} onSubmit={(event) => saveNames(event, form, onSubmit)}>
      <NamePair form={form} />
      <button className="btn mt-3" type="submit">{submitLabel}</button>
      <ErrorText code={form.code} />
    </form>
  )
}

function NamePair({ form }: { form: ReturnType<typeof useNames> }) {
  return (
    <>
      <NameInput label={text("members.given")} value={form.givenName} required onChange={form.setGivenName} />
      <NameInput label={text("members.family")} value={form.familyName} required={false} onChange={form.setFamilyName} />
    </>
  )
}

function NameInput({ label, value, required, onChange }: { label: string; value: string; required: boolean; onChange: (value: string) => void }) {
  return (
    <Field label={label}>
      <input className="field" value={value} required={required} onChange={(event) => onChange(event.target.value)} />
    </Field>
  )
}

async function saveNames(event: FormEvent, form: ReturnType<typeof useNames>, onSubmit: (given: string, family: string) => Promise<void>) {
  event.preventDefault()
  form.setCode("")
  try {
    await onSubmit(form.givenName, form.familyName)
  } catch (error) {
    form.setCode(errorCode(error))
  }
}

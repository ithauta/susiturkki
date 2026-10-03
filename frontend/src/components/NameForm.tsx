import { type FormEvent, useState } from "react"
import { errorCode } from "../api/client"
import { text } from "../i18n/text"
import { ErrorText } from "./Status"
import { Field } from "./Field"

type NameFormProps = { label: string; submitLabel: string; onSubmit: (name: string) => Promise<void> }

export function NameForm({ label, submitLabel, onSubmit }: NameFormProps) {
  const [name, setName] = useState("")
  const [code, setCode] = useState("")
  return (
    <form className="card" onSubmit={(event) => saveName(event, name, onSubmit, setName, setCode)}>
      <NameField label={label} value={name} onChange={setName} />
      <FormEnd code={code} label={submitLabel} />
    </form>
  )
}

export function RenameForm({ name, label, onSubmit }: { name: string; label: string; onSubmit: (name: string) => Promise<void> }) {
  const [value, setValue] = useState(name)
  const [code, setCode] = useState("")
  return (
    <form onSubmit={(event) => saveRename(event, value, onSubmit, setCode)}>
      <NameField label={label} value={value} onChange={setValue} />
      <FormEnd code={code} label={text("groups.rename")} />
    </form>
  )
}

function NameField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <Field label={label}>
      <input className="field" value={value} onChange={(event) => onChange(event.target.value)} required />
    </Field>
  )
}

function FormEnd({ code, label }: { code: string; label: string }) {
  return (
    <>
      <ErrorText code={code} />
      <button className="btn mt-3" type="submit">{label}</button>
    </>
  )
}

async function saveName(
  event: FormEvent,
  name: string,
  onSubmit: (name: string) => Promise<void>,
  setName: (name: string) => void,
  setCode: (code: string) => void,
) {
  event.preventDefault()
  await run(onSubmit(name), setCode, () => setName(""))
}

async function saveRename(event: FormEvent, name: string, onSubmit: (name: string) => Promise<void>, setCode: (code: string) => void) {
  event.preventDefault()
  await run(onSubmit(name), setCode)
}

async function run(action: Promise<void>, setCode: (code: string) => void, after?: () => void) {
  setCode("")
  try {
    await action
    after?.()
  } catch (error) {
    setCode(errorCode(error))
  }
}

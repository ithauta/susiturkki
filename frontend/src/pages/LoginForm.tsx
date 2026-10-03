import { type FormEvent, useState } from "react"
import { login } from "../api/admin"
import { errorCode } from "../api/client"
import { Field } from "../components/Field"
import { Shell } from "../components/Shell"
import { ErrorText } from "../components/Status"
import { text } from "../i18n/text"

type LoginFieldsProps = {
  password: string
  code: string
  onChange: (value: string) => void
  onSuccess: () => void
  setCode: (code: string) => void
}

export function LoginForm({ onSuccess }: { onSuccess: () => void }) {
  const [password, setPassword] = useState("")
  const [code, setCode] = useState("")
  return <Shell title={text("login.title")}><LoginFields password={password} code={code} onChange={setPassword} onSuccess={onSuccess} setCode={setCode} /></Shell>
}

function LoginFields({ password, code, onChange, onSuccess, setCode }: LoginFieldsProps) {
  return (
    <form className="card" onSubmit={(event) => submitLogin(event, password, onSuccess, setCode)}>
      <PasswordField value={password} onChange={onChange} />
      <ErrorText code={code} />
      <button className="btn mt-4 w-full" type="submit">{text("login.submit")}</button>
    </form>
  )
}

function PasswordField({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <Field label={text("login.password")}>
      <input className="field" type="password" autoComplete="current-password" value={value} onChange={(event) => onChange(event.target.value)} required />
    </Field>
  )
}

async function submitLogin(event: FormEvent, password: string, onSuccess: () => void, setCode: (code: string) => void) {
  event.preventDefault()
  setCode("")
  try {
    await login(password)
    onSuccess()
  } catch (error) {
    setCode(errorCode(error))
  }
}

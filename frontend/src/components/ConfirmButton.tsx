import { useState } from "react"
import { errorCode } from "../api/client"
import { text } from "../i18n/text"
import { ErrorText } from "./Status"

type ConfirmProps = { label: string; confirm: string; onConfirm: () => Promise<void> }

export function ConfirmButton({ label, confirm, onConfirm }: ConfirmProps) {
  const [open, setOpen] = useState(false)
  const [code, setCode] = useState("")
  if (open) return <Confirming label={confirm} code={code} onCancel={() => setOpen(false)} onConfirm={() => run(onConfirm, setCode, setOpen)} />
  return <button className="btn-danger" type="button" onClick={() => setOpen(true)}>{label}</button>
}

function Confirming({ label, code, onCancel, onConfirm }: { label: string; code: string; onCancel: () => void; onConfirm: () => void }) {
  return (
    <div>
      <ConfirmActions label={label} onConfirm={onConfirm} onCancel={onCancel} />
      <ErrorText code={code} />
    </div>
  )
}

function ConfirmActions({ label, onConfirm, onCancel }: { label: string; onConfirm: () => void; onCancel: () => void }) {
  return (
    <div className="flex gap-2">
      <button className="btn-danger" type="button" onClick={onConfirm}>{label}</button>
      <button className="btn-quiet" type="button" onClick={onCancel}>{text("action.cancel")}</button>
    </div>
  )
}

async function run(action: () => Promise<void>, setCode: (code: string) => void, setOpen: (open: boolean) => void) {
  setCode("")
  try {
    await action()
    setOpen(false)
  } catch (error) {
    setCode(errorCode(error))
  }
}

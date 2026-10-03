import { useCallback, useEffect, useState } from "react"
import { errorCode } from "../api/client"

export type LoadState<T> = { kind: "loading" } | { kind: "ready"; data: T } | { kind: "error"; code: string }

export function useAsync<T>(load: () => Promise<T>, active = true) {
  const [tick, setTick] = useState(0)
  const [state, setState] = useState<LoadState<T>>({ kind: "loading" })
  useEffect(() => track(active, load, setState), [load, tick, active])
  const reload = useCallback(() => setTick((value) => value + 1), [])
  return { state, reload }
}

function track<T>(active: boolean, load: () => Promise<T>, setState: (state: LoadState<T>) => void) {
  if (!active) return
  return watch(load, setState)
}

function watch<T>(load: () => Promise<T>, setState: (state: LoadState<T>) => void) {
  let live = true
  setState({ kind: "loading" })
  load().then((data) => accept(live, { kind: "ready", data }, setState)).catch((error) => fail(live, error, setState))
  return () => {
    live = false
  }
}

function accept<T>(live: boolean, state: LoadState<T>, setState: (state: LoadState<T>) => void) {
  if (live) setState(state)
}

function fail<T>(live: boolean, error: unknown, setState: (state: LoadState<T>) => void) {
  if (live) setState({ kind: "error", code: errorCode(error) })
}

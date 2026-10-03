import { useCallback, useEffect, useState } from "react"
import type { LoadState } from "./useAsync"
import { useAsync } from "./useAsync"

type Seasoned = { season: number }

export function useSeasonBrowse<T extends Seasoned>(loadFor: (season: number | undefined) => Promise<T>, active = true) {
  const [season, setSeason] = useState<number | undefined>(undefined)
  const [limit, setLimit] = useState<number | undefined>(undefined)
  const load = useCallback(() => loadFor(season), [loadFor, season])
  const result = useAsync(load, active)
  useEffect(() => rememberLimit(active, season, limit, result.state, setLimit), [active, season, limit, result.state])
  return { ...result, setSeason, limit }
}

function rememberLimit<T extends Seasoned>(
  active: boolean,
  season: number | undefined,
  limit: number | undefined,
  state: LoadState<T>,
  setLimit: (value: number) => void,
) {
  if (active) storeLimit(season, limit, state, setLimit)
}

function storeLimit<T extends Seasoned>(
  season: number | undefined,
  limit: number | undefined,
  state: LoadState<T>,
  setLimit: (value: number) => void,
) {
  if (season === undefined && limit === undefined && state.kind === "ready") setLimit(state.data.season)
}

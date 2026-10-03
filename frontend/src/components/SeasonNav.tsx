import { seasonLabel } from "../format/labels"
import { text } from "../i18n/text"

type NavProps = { shown: number; limit: number | undefined; onSeason: (season: number) => void }

export function SeasonNav({ shown, limit, onSeason }: NavProps) {
  return (
    <div className="card flex items-center justify-between gap-2">
      <SeasonStep label={text("season.previous")} onClick={() => onSeason(shown - 1)} />
      <h2 className="text-center text-lg font-semibold">{seasonLabel(shown)}</h2>
      <SeasonStep label={text("season.next")} disabled={limit === undefined || shown >= limit} onClick={() => onSeason(shown + 1)} />
    </div>
  )
}

function SeasonStep({ label, disabled, onClick }: { label: string; disabled?: boolean; onClick: () => void }) {
  return <button className="btn-quiet" type="button" disabled={disabled} onClick={onClick}>{label}</button>
}

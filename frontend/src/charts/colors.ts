const series = ["#1f4d3a", "#c44536", "#3d6f99", "#c47b2b", "#2f6f62", "#6b4c9a"]

export function memberColor(index: number): string {
  return series[index % series.length]
}

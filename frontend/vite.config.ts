import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv, type ProxyOptions } from "vite"

export default defineConfig(({ command, mode }) => ({
  plugins: [react(), tailwindcss()],
  server: { proxy: proxyFor(loadEnv(mode, process.cwd(), "").API_ORIGIN, command) },
}))

function proxyFor(origin: string | undefined, command: string): Record<string, ProxyOptions> | undefined {
  if (command !== "serve") return undefined
  if (!origin) throw new Error("missing API_ORIGIN")
  return { "/api": { target: origin, changeOrigin: true } }
}

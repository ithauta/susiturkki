export class ApiError extends Error {
  readonly code: string

  constructor(code: string) {
    super(code)
    this.code = code
  }
}

export function errorCode(error: unknown): string {
  if (error instanceof ApiError) return error.code
  return "request_failed"
}

export async function readJson<T>(path: string): Promise<T> {
  const response = await request(path)
  return response.json() as Promise<T>
}

export function sendJson(path: string, method: string, body?: unknown): Promise<Response> {
  return request(path, jsonInit(method, body))
}

export async function request(path: string, init?: RequestInit): Promise<Response> {
  const response = await fetch(path, { ...init, credentials: "same-origin" })
  if (!response.ok) throw await failed(response)
  return response
}

function jsonInit(method: string, body?: unknown): RequestInit {
  return { method, headers: { "Content-Type": "application/json" }, body: encoded(body) }
}

function encoded(body: unknown): string | undefined {
  if (body === undefined) return undefined
  return JSON.stringify(body)
}

async function failed(response: Response): Promise<ApiError> {
  return new ApiError(await codeFrom(response))
}

async function codeFrom(response: Response): Promise<string> {
  const body = await response.json().catch(() => ({ code: "request_failed" }))
  return body.code ?? "request_failed"
}

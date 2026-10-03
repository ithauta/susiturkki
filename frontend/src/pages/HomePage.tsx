import { Link } from "react-router-dom"
import { Shell } from "../components/Shell"
import { text } from "../i18n/text"

export function HomePage() {
  return (
    <Shell title={text("app.title")}>
      <section className="card">
        <p>{text("home.lead")}</p>
        <Link className="btn mt-4" to="/admin">{text("home.admin")}</Link>
      </section>
    </Shell>
  )
}

import { BrowserRouter, Route, Routes } from "react-router-dom"
import { AdminPage } from "./pages/AdminPage"
import { HomePage } from "./pages/HomePage"
import { ParticipantPage } from "./pages/ParticipantPage"

export function App() {
  return <BrowserRouter><AppRoutes /></BrowserRouter>
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/admin" element={<AdminPage />} />
      <Route path="/p/:token" element={<ParticipantPage />} />
      <Route path="*" element={<HomePage />} />
    </Routes>
  )
}

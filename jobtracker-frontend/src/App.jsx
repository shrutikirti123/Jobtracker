import { BrowserRouter, Routes, Route } from "react-router-dom"

import Sidebar from "./components/Sidebar"
import Topbar from "./components/Topbar"

import Login from "./pages/Login"
import Register from "./pages/Register"

import Dashboard from "./pages/Dashboard"
import Discover from "./pages/Discover"
import Jobs from "./pages/Jobs"
import ResumeUpload from "./pages/ResumeUpload"
import JobDetails from "./pages/JobDetails"
import Profile from "./pages/Profile"
import ResumeInsights from "./pages/ResumeInsights"
import CreateJob from "./pages/CreateJob"
import ProtectedRoute from "./components/ProtectedRoute"

function Layout() {

return (

<div className="flex h-screen bg-slate-100">

<Sidebar />

<div className="flex flex-col flex-1">

<Topbar />

<main className="p-8 overflow-auto">

<Routes>

<Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />

<Route path="/discover" element={<ProtectedRoute><Discover /></ProtectedRoute>} />

<Route path="/jobs" element={<ProtectedRoute><Jobs /></ProtectedRoute>} />

<Route path="/create-job" element={<ProtectedRoute><CreateJob /></ProtectedRoute>} />

<Route path="/jobs/:id" element={<ProtectedRoute><JobDetails /></ProtectedRoute>} />

<Route path="/resume" element={<ProtectedRoute><ResumeUpload /></ProtectedRoute>} />

<Route path="/resume-insights" element={<ProtectedRoute><ResumeInsights /></ProtectedRoute>} />

<Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />

</Routes>

</main>

</div>

</div>
)

}

function App() {

return (

<BrowserRouter>

<Routes>

{/* Public pages */}

<Route path="/" element={<Login />} />

<Route path="/login" element={<Login />} />

<Route path="/register" element={<Register />} />

{/* App pages */}

<Route path="/*" element={<Layout />} />

</Routes>

</BrowserRouter>

)

}

export default App
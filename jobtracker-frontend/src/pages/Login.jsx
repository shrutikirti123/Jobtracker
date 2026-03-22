import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/api"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import logo from "../assets/logo.jpg"

function Login(){

const navigate = useNavigate()

const [email,setEmail] = useState("")
const [password,setPassword] = useState("")
const [error,setError] = useState(null)

const handleLogin = async (e) => {

e.preventDefault()

try{

const form = new URLSearchParams()

form.append("username",email)
form.append("password",password)

const res = await api.post(
"/auth/login",
form,
{
headers:{
"Content-Type":"application/x-www-form-urlencoded"
}
}
)

localStorage.setItem("token",res.data.access_token)

navigate("/dashboard")

}catch(err){

setError("Invalid credentials")

}

}

return(

<div className="h-screen grid md:grid-cols-2">

{/* LEFT HERO SECTION */}

<div className="bg-slate-950 text-white flex flex-col justify-center px-16">

<h1 className="text-6xl font-bold text-center mb-6 text-blue-400">
JobTracker
</h1>

<h1 className="text-4xl font-bold mb-6">
Track your job search like a pro
</h1>

<p className="text-slate-400 mb-10 max-w-md">
Discover jobs, track applications, and analyze your hiring progress with AI-powered insights.
</p>

<ul className="space-y-3 text-sm text-slate-400">

<li>• AI powered job matching</li>
<li>• Track your job pipeline</li>
<li>• Resume skill insights</li>
<li>• Hiring analytics dashboard</li>

</ul>

</div>

{/* RIGHT LOGIN SECTION */}

<div className="flex items-center justify-center bg-gray-50">

<div className="w-full max-w-sm">

{/* BRAND */}

<div className="text-center mb-8">

<div className="flex justify-center mb-3">

<img src={logo} className="w-55 h-25"/>

</div>

<p className="text-gray-500 text-sm">
Track, analyze, and optimize your job search
</p>

</div>

{/* LOGIN CARD */}

<form
onSubmit={handleLogin}
className="bg-white p-8 rounded-xl shadow-md border space-y-6"
>

<h2 className="text-xl font-semibold text-center">
Login to your account
</h2>

{error && (
<p className="text-red-500 text-sm text-center">
{error}
</p>
)}

<Input
placeholder="Email address"
value={email}
onChange={(e)=>setEmail(e.target.value)}
className="h-11"
/>

<Input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
className="h-11"
/>

<Button className="w-full h-11">
Sign In
</Button>

<p className="text-sm text-gray-500 text-center">

Don't have an account?

<button
type="button"
onClick={()=>navigate("/register")}
className="text-blue-600 ml-1"
>
Sign Up
</button>

</p>

</form>

</div>

</div>

</div>

)

}

export default Login
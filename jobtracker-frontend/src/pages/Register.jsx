import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/api"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

function Register(){

const navigate = useNavigate()

const [name,setName] = useState("")
const [email,setEmail] = useState("")
const [password,setPassword] = useState("")
const [error,setError] = useState(null)

const register = async(e)=>{

e.preventDefault()
setError(null)

try{

await api.post("/auth/signup",{
email,
password
})

alert("Signup successful")
navigate("/")

}catch(err){

setError(err.response?.data?.detail || "Signup failed")
navigate("/")
}

}

return(



<div className="h-screen grid md:grid-cols-2">

{/* LEFT PANEL */}

<div className="bg-slate-950 text-white flex flex-col justify-center px-16">

<h1 className="text-6xl font-bold text-center mb-6 text-blue-400">
JobTracker
</h1>

<h1 className="text-4xl font-bold mb-6">
Track your job search like a pro
</h1>

<p className="text-slate-400 mb-8">
Discover jobs, track applications, and analyze your hiring progress with AI powered insights.
</p>

<ul className="space-y-2 text-sm text-slate-400">

<li>• AI powered job matching</li>
<li>• Track your job pipeline</li>
<li>• Resume skill insights</li>
<li>• Hiring analytics dashboard</li>

</ul>

</div>

{/* SIGNUP FORM */}

<div className="flex items-center justify-center bg-gray-50">

<form
onSubmit={register}
className="w-full max-w-sm bg-white p-8 rounded-xl shadow-sm space-y-6"
>

<h2 className="text-2xl font-semibold text-center">
Sign Up
</h2>

{error && (
<p className="text-red-500 text-sm">
{error}
</p>
)}

<Input
placeholder="Name"
value={name}
onChange={(e)=>setName(e.target.value)}
/>

<Input
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>

<Input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
/>

<Button className="w-full">
Create Account
</Button>

<p className="text-sm text-gray-500 text-center">

Already have an account?

<button
type="button"
onClick={()=>navigate("/")}
className="text-blue-600 ml-1"
>
Log In
</button>

</p>

</form>

</div>

</div>

)

}

export default Register
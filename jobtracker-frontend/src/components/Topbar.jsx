import { useState, useRef, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Bell, User } from "lucide-react"
import { useNavigate } from "react-router-dom"

function Topbar(){

const [open,setOpen] = useState(false)
const [search,setSearch] = useState("")
const navigate = useNavigate()

const dropdownRef = useRef()

const logout = () => {

localStorage.removeItem("token")
navigate("/login")

}

const searchJobs = (e) => {

if(e.key === "Enter" && search.trim()){

navigate(`/discover?q=${search}`)

}

}

useEffect(()=>{

const handleClickOutside = (event)=>{

if(dropdownRef.current && !dropdownRef.current.contains(event.target)){
setOpen(false)
}

}

document.addEventListener("mousedown",handleClickOutside)

return ()=>{
document.removeEventListener("mousedown",handleClickOutside)
}

},[])

return(

<div className="h-16 border-b bg-white flex items-center justify-between px-8">

<Input
placeholder="Search jobs..."
className="w-64"
value={search}
onChange={(e)=>setSearch(e.target.value)}
onKeyDown={searchJobs}
/>

<div className="flex items-center gap-6">

<Bell size={20} className="text-gray-500"/>

<div className="relative" ref={dropdownRef}>

<div
onClick={()=>setOpen(!open)}
className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center cursor-pointer"
>

<User size={16}/>

</div>

{open && (

<div className="absolute right-0 mt-2 w-44 bg-white border rounded shadow">

<button
className="block w-full text-left px-4 py-2 hover:bg-gray-100"
onClick={()=>navigate("/profile")}
>
Profile
</button>

<button
className="block w-full text-left px-4 py-2 hover:bg-gray-100"
onClick={()=>navigate("/resume-insights")}
>
Resume Insights
</button>

<button
className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-red-500"
onClick={logout}
>
Logout
</button>

</div>

)}

</div>

</div>

</div>

)

}

export default Topbar
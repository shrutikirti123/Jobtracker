import { Link, useLocation } from "react-router-dom"
import { User } from "lucide-react"
import {
LayoutDashboard,
Search,
Briefcase,
BarChart3,
FileText
} from "lucide-react"

function Sidebar() {

const location = useLocation()

const menu = [
{
name:"Dashboard",
icon:LayoutDashboard,
path:"/dashboard"
},
{
name:"Discover Jobs",
icon:Search,
path:"/discover"
},
{
name:"My Jobs",
icon:Briefcase,
path:"/jobs"
},
{
name:"Upload Resume",
icon:FileText,
path:"/resume"
}
]

return (

<div className="w-64 h-screen bg-slate-950 text-slate-200 flex flex-col border-r border-slate-800">

<div className="text-xl font-semibold p-6 border-b border-slate-800">
JobTracker
</div>

<nav className="flex flex-col gap-1 p-4">

{menu.map((item)=>{

const Icon = item.icon
const active = location.pathname === item.path

return(

<Link
key={item.path}
to={item.path}
className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition
${active
? "bg-slate-800 text-white"
: "text-slate-400 hover:bg-slate-800 hover:text-white"
}`}
>

<Icon size={18}/>
{item.name}

</Link>

)

})}

</nav>

</div>

)

}

export default Sidebar
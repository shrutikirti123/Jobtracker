import { useEffect,useState } from "react"
import api from "../api/api"

import {
Card,
CardHeader,
CardTitle,
CardContent
} from "@/components/ui/card"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import {
PieChart,
Pie,
Cell,
Tooltip,
ResponsiveContainer
} from "recharts"

const COLORS = [
"#2563eb",
"#16a34a",
"#f59e0b",
"#ef4444"
]

function Dashboard(){


const [stats,setStats] = useState(null)
const [recentJobs,setRecentJobs] = useState([])
const [loading,setLoading] = useState(true)
const navigate = useNavigate()

useEffect(()=>{

const load = async()=>{

try{

const res = await api.get("/analytics/dashboard")
setStats(res.data)

const jobs = await api.get("/jobs",{ params:{ limit:5 } })
setRecentJobs(jobs.data)

}catch(err){

console.error(err)

}

setLoading(false)

}

load()

},[])

if(loading){
return <p className="text-gray-500">Loading dashboard...</p>
}

if(!stats){
return <p className="text-red-500">Failed to load stats</p>
}

const chartData = [
{ name:"Applied", value:stats.applied || 0 },
{ name:"Interview", value:stats.interview || 0 },
{ name:"Offer", value:stats.offer || 0 },
{ name:"Rejected", value:stats.rejected || 0 }
]

return(

<div className="space-y-10">

<h1 className="text-3xl font-semibold">Dashboard</h1>
<Button onClick={()=>navigate("/create-job")}>
+ Add Job
</Button>

<div className="grid md:grid-cols-4 gap-6">

<Card>
<CardHeader>
<CardTitle>Total Jobs</CardTitle>
</CardHeader>
<CardContent>
<p className="text-3xl font-bold">{stats.total_jobs}</p>
</CardContent>
</Card>

<Card>
<CardHeader>
<CardTitle>Applied</CardTitle>
</CardHeader>
<CardContent>
<p className="text-3xl font-bold text-blue-600">{stats.applied}</p>
</CardContent>
</Card>

<Card>
<CardHeader>
<CardTitle>Interviews</CardTitle>
</CardHeader>
<CardContent>
<p className="text-3xl font-bold text-green-600">{stats.interview}</p>
</CardContent>
</Card>

<Card>
<CardHeader>
<CardTitle>Offers</CardTitle>
</CardHeader>
<CardContent>
<p className="text-3xl font-bold text-purple-600">{stats.offer}</p>
</CardContent>
</Card>

</div>

<div className="grid md:grid-cols-2 gap-8">

<Card>

<CardHeader>
<CardTitle>Application Status</CardTitle>
</CardHeader>

<CardContent>

<div style={{ width:"100%", height:300 }}>

<ResponsiveContainer width="100%" height="100%">

<PieChart>

<Pie data={chartData} dataKey="value" outerRadius={90}>

{chartData.map((entry,index)=>(
<Cell key={index} fill={COLORS[index]}/>
))}

</Pie>

<Tooltip/>

</PieChart>

</ResponsiveContainer>

</div>

</CardContent>

</Card>

<Card>

<CardHeader>
<CardTitle>Recent Applications</CardTitle>
</CardHeader>

<CardContent>

<ul className="space-y-2 text-sm text-gray-600">

{recentJobs.map(job=>(
<li key={job.id}>
{job.title} — {job.status}
</li>
))}

</ul>

</CardContent>

</Card>

</div>

</div>

)

}

export default Dashboard
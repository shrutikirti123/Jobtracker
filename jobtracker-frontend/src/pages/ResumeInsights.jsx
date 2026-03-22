import { useEffect, useState } from "react"
import api from "../api/api"

import {
Card,
CardHeader,
CardTitle,
CardContent
} from "@/components/ui/card"

function ResumeInsights(){

const [data,setData] = useState(null)
const [loading,setLoading] = useState(true)

useEffect(()=>{

const load = async()=>{

try{

const res = await api.get("/resume/insights")
setData(res.data)

}catch(err){

console.error(err)

}

setLoading(false)

}

load()

},[])

if(loading){
return <p className="text-gray-500">Analyzing resume...</p>
}

if(!data){
return <p className="text-red-500">Resume not found</p>
}

return(

<div className="space-y-8 max-w-3xl">

<h1 className="text-3xl font-semibold">
Resume Insights
</h1>

<Card>

<CardHeader>
<CardTitle>
Detected Skills
</CardTitle>
</CardHeader>

<CardContent>

<div className="flex flex-wrap gap-2">

{data?.detected_skills?.map((skill,i)=>(
<span
key={i}
className="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm"
>
{skill}
</span>
))}

</div>

</CardContent>

</Card>

<Card>

<CardHeader>
<CardTitle>
Improvement Suggestions
</CardTitle>
</CardHeader>

<CardContent>

<ul className="space-y-2">

{data?.top_missing_skills?.map((item,i)=>(
<li key={i}>
{item.skill} ({item.jobs} jobs)
</li>
))}

</ul>

</CardContent>

</Card>

</div>

)

}

export default ResumeInsights
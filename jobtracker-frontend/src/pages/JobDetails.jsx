import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import api from "../api/api"

import { Button } from "@/components/ui/button"

import {
Card,
CardHeader,
CardTitle,
CardContent
} from "@/components/ui/card"

function JobDetails(){

const { id } = useParams()
const navigate = useNavigate()

const [data,setData] = useState(null)
const [loading,setLoading] = useState(true)

useEffect(()=>{

const load = async()=>{

try{

const res = await api.get(`/jobs/${id}/match`)
setData(res.data)

}catch(err){

console.error(err)


}

setLoading(false)

}

load()

},[id])

if(loading){
return <p className="text-gray-500">Analyzing job match...</p>
}

if(!data){
return <p className="text-red-500">Failed to load job analysis</p>
}

return(

<div className="space-y-8 max-w-3xl">

<Button
variant="outline"
onClick={()=>navigate(-1)}
>
← Back
</Button>

<div>

<h1 className="text-3xl font-semibold">
{data.title}
</h1>

<p className="text-gray-500">
{data.company}
</p>

</div>

<Card>

<CardHeader>
<CardTitle>Match Score</CardTitle>
</CardHeader>

<CardContent>

<p className="text-4xl font-bold text-blue-600">
{data.match_score}%
</p>

</CardContent>

</Card>

<Card>

<CardHeader>
<CardTitle>Matching Skills</CardTitle>
</CardHeader>

<CardContent>

<div className="flex flex-wrap gap-2">

{data.matching_skills?.map((skill,i)=>(
<span
key={i}
className="px-3 py-1 bg-green-100 text-green-700 rounded text-sm"
>
{skill}
</span>
))}

</div>

</CardContent>

</Card>

<Card>

<CardHeader>
<CardTitle>Missing Skills</CardTitle>
</CardHeader>

<CardContent>

<div className="flex flex-wrap gap-2">

{data.missing_skills?.map((skill,i)=>(
<span
key={i}
className="px-3 py-1 bg-red-100 text-red-700 rounded text-sm"
>
{skill}
</span>
))}

</div>

</CardContent>

</Card>

</div>

)

}

export default JobDetails
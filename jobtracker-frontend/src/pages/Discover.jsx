import { useState, useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import api from "../api/api"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

import JobCard from "../components/JobCard"

function Discover(){

const [keyword,setKeyword] = useState("")
const [jobs,setJobs] = useState([])
const [loading,setLoading] = useState(false)
const [searched,setSearched] = useState(false)
const [error,setError] = useState(null)

const [params] = useSearchParams()

// 🔹 search function FIRST
const searchJobs = async (query = keyword) => {

const cleanKeyword = query.trim()

if(!cleanKeyword){
return
}

setLoading(true)
setError(null)

try{

const res = await api.get("/jobs/discover",{
params:{ keyword: cleanKeyword }
})

setJobs(res.data)
setSearched(true)

}catch(err){

console.error("Discover jobs error:",err)
setError("Failed to load jobs")

}

setLoading(false)

}

// 🔹 then useEffect
useEffect(()=>{

const q = params.get("q")

if(q){
setKeyword(q)
searchJobs(q)
}

},[])

return(

<div className="space-y-8 max-w-6xl">

<h1 className="text-3xl font-semibold">
Discover Jobs
</h1>

<div className="flex gap-3">

<Input
placeholder="Search jobs (python, devops, backend...)"
value={keyword}
onChange={(e)=>setKeyword(e.target.value)}
onKeyDown={(e)=>{
if(e.key === "Enter") searchJobs()
}}
/>

<Button onClick={()=>searchJobs()}>
Search
</Button>

</div>

{loading && <p className="text-gray-500">Searching jobs...</p>}

{error && <p className="text-red-500">{error}</p>}

{searched && !loading && jobs.length === 0 && (
<p className="text-gray-500">No jobs found</p>
)}

<div className="grid md:grid-cols-2 gap-6">

{jobs.map((job,i)=>(
<JobCard key={i} job={job}/>
))}

</div>

</div>

)

}

export default Discover
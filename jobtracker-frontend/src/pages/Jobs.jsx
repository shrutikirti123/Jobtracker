import { useEffect, useState } from "react"
import api from "../api/api"
import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import {
DragDropContext,
Droppable,
Draggable
} from "@hello-pangea/dnd"

import { Card, CardContent } from "@/components/ui/card"

const columns = ["Saved", "Applied", "Interview", "Offer", "Rejected"]

function Jobs(){

const [jobs,setJobs] = useState([])
const [loading,setLoading] = useState(true)
const navigate = useNavigate()


useEffect(()=>{
fetchJobs()
},[])

const fetchJobs = async () => {

try{

const res = await api.get("/jobs")
setJobs(res.data)

}catch(err){

console.error(err)

}

setLoading(false)

}

const updateStatus = async(jobId,status)=>{

try{

await api.patch(`/jobs/${jobId}?status=${status}`)

setJobs(prev =>
prev.map(job =>
job.id === jobId ? {...job,status:status} : job
)
)

}catch(err){

console.error(err)

}

}

const deleteJob = async(id)=>{

try{

await api.delete(`/jobs/${id}`)

setJobs(prev => prev.filter(j => j.id !== id))

}catch(err){

console.error(err)

}

}

const onDragEnd = (result)=>{

if(!result.destination) return

const jobId = parseInt(result.draggableId)
const newStatus = result.destination.droppableId

updateStatus(jobId,newStatus)

}

if(loading){

return <p className="text-gray-500">Loading jobs...</p>

}

return(

<div className="space-y-8">

{/* PAGE HEADER */}

<div>

<h1 className="text-3xl font-semibold">
My Job Pipeline
</h1>

<Button onClick={() => navigate("/create-job")} className="mt-4" align="right">
+ Add Job
</Button>

<p className="text-gray-500">
Drag jobs between stages to track applications
</p>

</div>

<DragDropContext onDragEnd={onDragEnd}>

<div className="grid grid-cols-5 gap-6">

{columns.map(status =>{

const columnJobs = jobs.filter(job => job.status === status)

return(

<Droppable droppableId={status} key={status}>

{(provided)=>(

<div
ref={provided.innerRef}
{...provided.droppableProps}
className="bg-slate-100 p-4 rounded-lg min-h-[420px]"
>

<h2 className="font-semibold mb-4 text-sm text-gray-600">
{status}
</h2>

<div className="flex flex-col gap-3">

{columnJobs.map((job,index)=>(

<Draggable
draggableId={job.id.toString()}
index={index}
key={job.id}
>

{(provided)=>(

<Card
ref={provided.innerRef}
{...provided.draggableProps}
{...provided.dragHandleProps}
className="shadow-sm hover:shadow-md transition"
>

<CardContent className="p-4 space-y-3">
<Link
to={`/jobs/${job.id}`}
className="text-sm text-blue-600 hover:underline"
>
View Details
</Link>
<div>

<p className="font-semibold">
{job.title}
</p>

<p className="text-sm text-gray-500">
{job.company}
</p>

</div>

<div className="flex gap-2">

<Button
size="sm"
variant="destructive"
onClick={()=>deleteJob(job.id)}
>

Delete

</Button>

</div>

</CardContent>

</Card>

)}

</Draggable>

))}

{provided.placeholder}

</div>

</div>

)}

</Droppable>

)

})}

</div>

</DragDropContext>

</div>

)

}

export default Jobs
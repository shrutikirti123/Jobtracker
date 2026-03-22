import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api/api"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

function CreateJob(){

const navigate = useNavigate()

const [title,setTitle] = useState("")
const [company,setCompany] = useState("")
const [description,setDescription] = useState("")
const [status,setStatus] = useState("Saved")

const createJob = async (e)=>{

e.preventDefault()

try{

await api.post("/jobs",{
title,
company,
description,
status
})

navigate("/jobs")

}catch(err){

console.error(err)

}

}

return(

<div className="max-w-xl space-y-8">

<h1 className="text-3xl font-semibold">
Add Job
</h1>

<form
onSubmit={createJob}
className="space-y-6 bg-white p-6 rounded-xl shadow"
>

<Input
placeholder="Job title"
value={title}
onChange={(e)=>setTitle(e.target.value)}
/>

<Input
placeholder="Company"
value={company}
onChange={(e)=>setCompany(e.target.value)}
/>

<Textarea
placeholder="Job description"
value={description}
onChange={(e)=>setDescription(e.target.value)}
/>

<select
value={status}
onChange={(e)=>setStatus(e.target.value)}
className="border p-2 rounded w-full"
>

<option>Saved</option>
<option>Applied</option>
<option>Interview</option>
<option>Offer</option>
<option>Rejected</option>

</select>

<Button className="w-full">
Create Job
</Button>

</form>

</div>

)

}

export default CreateJob
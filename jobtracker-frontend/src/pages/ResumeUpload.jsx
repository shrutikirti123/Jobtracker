import { useState } from "react"
import api from "../api/api"

function ResumeUpload(){

const [file,setFile] = useState(null)
const [loading,setLoading] = useState(false)

const uploadResume = async () => {

if(!file){
alert("Please select a resume")
return
}

const formData = new FormData()
formData.append("file",file)

try{

setLoading(true)

await api.post("/resume/upload-resume",formData,{
headers:{
"Content-Type":"multipart/form-data"
}
})

alert("Resume uploaded successfully")

}catch(err){

console.log(err)
alert("Upload failed")

}finally{

setLoading(false)

}

}

return(

<div>

<h1 className="text-3xl font-bold mb-6">
Upload Resume
</h1>

<div className="bg-white p-6 rounded shadow w-96">

<input
type="file"
accept=".pdf"
onChange={(e)=>setFile(e.target.files[0])}
className="mb-4"
/>

<button
className="bg-blue-500 text-white px-4 py-2 rounded"
onClick={uploadResume}
>
{loading ? "Uploading..." : "Upload Resume"}
</button>

</div>

</div>

)

}

export default ResumeUpload
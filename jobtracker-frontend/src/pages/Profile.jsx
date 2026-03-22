import { useEffect, useState } from "react"
import api from "../api/api"

import {
Card,
CardHeader,
CardTitle,
CardContent
} from "@/components/ui/card"

function Profile(){

const [user,setUser] = useState(null)

useEffect(()=>{

const loadProfile = async () => {

try{

const res = await api.get("/users/me")
setUser(res.data)

}catch(err){

console.error("Profile error:",err)

}

}

loadProfile()

},[])

if(!user){
return <p className="text-gray-500">Loading profile...</p>
}

return(

<div className="max-w-xl space-y-6">

<h1 className="text-3xl font-semibold">
Account Profile
</h1>

<Card>

<CardHeader>
<CardTitle>
Account Details
</CardTitle>
</CardHeader>

<CardContent className="space-y-4">

<div>

<p className="text-sm text-gray-500">
Name
</p>

<p className="font-medium">
{user.name}
</p>

</div>

<div>

<p className="text-sm text-gray-500">
Email
</p>

<p className="font-medium">
{user.email}
</p>

</div>

<div>

<p className="text-sm text-gray-500">
Account Role
</p>

<p className="font-medium">
{user.role}
</p>

</div>

</CardContent>

</Card>

</div>

)

}

export default Profile
import { Link } from "react-router-dom"

function Navbar(){

return(

<div className="bg-white shadow-md p-4 flex justify-between">

<div className="font-bold text-xl text-blue-600">
JobTracker
</div>

<div className="flex gap-6">

<Link to="/dashboard">Dashboard</Link>

<Link to="/discover">Discover</Link>

<Link to="/jobs">My Jobs</Link>

<Link to="/analytics">Analytics</Link>

</div>

</div>

)

}

export default Navbar
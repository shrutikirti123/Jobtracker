import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import api from "../api/api"

function JobCard({ job }) {


const saveJob = async () => {

try{

await api.post("/jobs/save-external",{
title: job.title,
company: job.company,
description: job.description
})

alert("Job saved")

}catch(err){

console.error(err)
alert("Failed to save job")

}

}

return(

    <Card className="shadow-sm hover:shadow-md transition">

            <CardHeader>

                <CardTitle className="text-lg">
                    {job.title}
                </CardTitle>

                <p className="text-sm text-gray-500">
                    {job.company}
                </p>

            </CardHeader>

            <CardContent className="space-y-4">

                <div className="text-sm">

                    <span className="font-medium">
                        Match Score:
                    </span>

                    <span className="ml-2 text-blue-600 font-semibold">
                        {job.match_score}%
                    </span>

                </div>

                {job.missing_skills?.length > 0 && (

                    <div className="text-xs text-gray-500">

                        Missing Skills:

                        <div className="flex flex-wrap gap-2 mt-1">

                            {job.missing_skills.map((skill, i) => (
                                <span
                                    key={i}
                                    className="px-2 py-1 bg-gray-100 rounded"
                                >
                                    {skill}
                                </span>
                            ))}

                        </div>

                    </div>

                )}

                <div className="flex gap-3">

                    <Button
                        onClick={saveJob}
                        size="sm"
                    >
                        Save Job
                    </Button>

                    <a
                        href={job.url}
                        target="_blank"
                        className="text-sm text-blue-600 hover:underline"
                    >
                        View Job
                    </a>

                </div>

            </CardContent>

        </Card>

)

}

export default JobCard
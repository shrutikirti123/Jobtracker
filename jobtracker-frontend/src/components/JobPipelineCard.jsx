import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import api from "../api/api"

function JobPipelineCard({ job, reload }) {

const updateStatus = async (status) => {

try {

await api.patch(`/jobs/${job.id}?status=${status}`)

reload()

} catch (err) {

console.error(err)

}

}

const deleteJob = async () => {

try {

await api.delete(`/jobs/${job.id}`)

reload()

} catch (err) {

console.error(err)

}

}

return (
    <><Card className="shadow-sm">

            <CardContent className="space-y-3 p-4">

                <div>
                    <h3 className="font-medium">{job.title}</h3>
                    <p className="text-xs text-gray-500">{job.company}</p>
                </div>

                <div className="flex flex-wrap gap-2">

                    <Button size="sm" onClick={() => updateStatus("Saved")}>
                        Saved
                    </Button>

                    <Button size="sm" onClick={() => updateStatus("Applied")}>
                        Applied
                    </Button>

                    <Button size="sm" onClick={() => updateStatus("Interview")}>
                        Interview
                    </Button>

                    <Button size="sm" onClick={() => updateStatus("Offer")}>
                        Offer
                    </Button>

                    <Button size="sm" variant="destructive" onClick={deleteJob}>
                        Delete
                    </Button>

                </div>

            </CardContent>

        </Card></>

)

}

export default JobPipelineCard
import { BriefcaseIcon, MapPinIcon, DollarSignIcon, ClockIcon } from 'lucide-react';
import { Navbar } from './Navbar';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { JobDetails } from './JobDetails';


export function JobOpenings() {
    const [jobOpenings, setJobOpenings] = useState([]);
    const [viewJob, setViewJob] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const api = import.meta.env.VITE_SERVER_URL + '/api/jobs';
    const jobTitle = 'Software Engineer';
    const location = 'United States';

    useEffect(() => {
        axios.get(api + `?query=${jobTitle}&location=${location}`)
            .then(response => {
                setJobOpenings(response.data.status == "success" ? response.data.jobs : []);
            });
    }, [api]);

    const handleViewJob = (job: any) => {
        setSelectedJob(job);
        setViewJob(true);
    }

    return (
        <>
            {viewJob && selectedJob ? (
                <JobDetails job={selectedJob} onClose={() => setViewJob(false)} />
            ) : (
                <div className="min-h-screen w-full bg-gray-50">
                    <Navbar />
                    <div className="max-w-6xl mx-auto px-4 py-8">
                        <div className="mb-8">
                            <h1 className="text-3xl font-bold text-gray-900 mb-2">
                                Job Openings
                            </h1>
                            <p className="text-gray-600">
                                Browse available positions and apply with your tailored resume
                            </p>
                        </div>

                        {jobOpenings.length === 0 ? (
                            <p className="text-gray-600 text-center font-bold">No job openings found.</p>
                        ) : (
                            <div className="space-y-4">
                                {jobOpenings.map((job) => (
                                    <div
                                        key={job['id']}
                                        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition cursor-pointer"
                                        onClick={() => handleViewJob(job)}
                                    >
                                        <div className="flex items-start justify-between">
                                            <img src={job['logo']} alt="" className="w-16 h-16 object-contain mr-2" />
                                            <div className="flex-1">
                                                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                                    {job['title']}
                                                </h3>
                                                <p className="text-gray-700 font-medium mb-4">
                                                    {job['company']}
                                                </p>
                                                <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                                                    <div className="flex items-center gap-2">
                                                        <MapPinIcon className="w-4 h-4" />
                                                        {job['location']}
                                                    </div>
                                                    {/* <div className="flex items-center gap-2">
                                            <DollarSignIcon className="w-4 h-4" />
                                            {job['salary']}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <BriefcaseIcon className="w-4 h-4" />
                                            {job['type']}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <ClockIcon className="w-4 h-4" />
                                            {job['postedDate']}
                                        </div> */}
                                                </div>
                                            </div>
                                            <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 transition">
                                                Apply
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

        </>
    )
}

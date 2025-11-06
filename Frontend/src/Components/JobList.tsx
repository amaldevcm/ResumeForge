import { useNavigate } from 'react-router-dom'
import {
    BriefcaseIcon,
    MapPinIcon,
    DollarSignIcon,
    ClockIcon,
} from 'lucide-react'
import { Navbar } from './Navbar'
const jobOpenings = [
    {
        id: 1,
        title: 'Senior Frontend Developer',
        company: 'TechCorp Inc.',
        location: 'San Francisco, CA',
        salary: '$120k - $180k',
        type: 'Full-time',
        postedDate: '2 days ago',
    },
    {
        id: 2,
        title: 'Product Designer',
        company: 'Design Studio',
        location: 'Remote',
        salary: '$90k - $130k',
        type: 'Full-time',
        postedDate: '1 week ago',
    },
    {
        id: 3,
        title: 'Backend Engineer',
        company: 'StartupXYZ',
        location: 'New York, NY',
        salary: '$110k - $160k',
        type: 'Full-time',
        postedDate: '3 days ago',
    },
]
export function JobOpenings() {
    const navigate = useNavigate()
    return (
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
                <div className="space-y-4">
                    {jobOpenings.map((job) => (
                        <div
                            key={job.id}
                            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition cursor-pointer"
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                        {job.title}
                                    </h3>
                                    <p className="text-gray-700 font-medium mb-4">
                                        {job.company}
                                    </p>
                                    <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                                        <div className="flex items-center gap-2">
                                            <MapPinIcon className="w-4 h-4" />
                                            {job.location}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <DollarSignIcon className="w-4 h-4" />
                                            {job.salary}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <BriefcaseIcon className="w-4 h-4" />
                                            {job.type}
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <ClockIcon className="w-4 h-4" />
                                            {job.postedDate}
                                        </div>
                                    </div>
                                </div>
                                <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 transition">
                                    Apply
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

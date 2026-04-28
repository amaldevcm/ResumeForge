import { ArrowLeftIcon, BriefcaseIcon, MapPinIcon, DollarSignIcon, ClockIcon, CheckCircleIcon, BuildingIcon } from 'lucide-react'
import { Navbar } from '../Components/Navbar'
// import axios from 'axios'

interface JobDetailsProps {
    // jobURL: string;
    job: any;
    onClose: () => void;
}

export function JobDetails({ job, onClose }: JobDetailsProps) {
    // const api = import.meta.env.VITE_SERVER_URL + '/api/jobDetails?url=' + encodeURIComponent(jobURL);
    // const [job, setJob] = useState<any>(null);

    // useEffect(() => {
    //     // Fetch job details using the jobURL
    //     axios.get(api).then((response) => {
    //         if (response.data.status === "success") {
    //             setJob(response.data.details);
    //         } else {
    //             setJob(null);
    //         }
    //     }).catch((error) => {
    //         console.error('Error fetching job details:', error);
    //         setJob(null);
    //     });
    // }, [api]);

    if (job === null) {
        return (
            <div className="min-h-screen w-full bg-gray-50">
                <Navbar />
                <div className="max-w-6xl mx-auto px-4 py-16 text-center">
                    <h1 className="text-2xl font-bold text-gray-900 mb-4">
                        Job Not Found
                    </h1>
                    <p className="text-gray-600 mb-6">
                        The job listing you're looking for doesn't exist.
                    </p>
                    <button
                        onClick={onClose}
                        className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
                    >
                        Back to Job Openings
                    </button>
                </div>
            </div>
        )
    }


    //   const job = jobOpenings.find((j) => j.id === Number(id))
    //   if (!job) {
    //     return (
    //       <div className="min-h-screen w-full bg-gray-50">
    //         <Navbar />
    //         <div className="max-w-6xl mx-auto px-4 py-16 text-center">
    //           <h1 className="text-2xl font-bold text-gray-900 mb-4">
    //             Job Not Found
    //           </h1>
    //           <p className="text-gray-600 mb-6">
    //             The job listing you're looking for doesn't exist.
    //           </p>
    //           <button
    //             onClick={() => navigate('/job-openings')}
    //             className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
    //           >
    //             Back to Job Openings
    //           </button>
    //         </div>
    //       </div>
    //     )
    //   }
    return (
        <div className="min-h-screen w-full bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 py-8">
                <button
                    onClick={onClose}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition"
                >
                    <ArrowLeftIcon className="w-5 h-5" />
                    Back to Job Openings
                </button>

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-6">
                    <div className="flex items-start justify-between mb-6">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 mb-2">
                                {job.title}
                            </h1>
                            <div className="flex items-center gap-2 text-lg text-gray-700 font-medium">
                                <BuildingIcon className="w-5 h-5 text-gray-500" />
                                {job.company}
                            </div>
                        </div>
                        <button
                            onClick={onClose}
                            className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
                        >
                            Apply Now
                        </button>
                    </div>

                    <div className="flex flex-wrap gap-4 mb-8">
                        <span className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-sm font-medium text-gray-700">
                            <MapPinIcon className="w-4 h-4 text-gray-500" />
                            {job.location}
                        </span>
                        <span className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-sm font-medium text-gray-700">
                            <DollarSignIcon className="w-4 h-4 text-gray-500" />
                            {job.salary}
                        </span>
                        <span className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-sm font-medium text-gray-700">
                            <BriefcaseIcon className="w-4 h-4 text-gray-500" />
                            {job.type}
                        </span>
                        <span className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-lg text-sm font-medium text-gray-700">
                            <ClockIcon className="w-4 h-4 text-gray-500" />
                            Posted {job.postedDate}
                        </span>
                    </div>

                    <div className="border-t border-gray-200 pt-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4">
                            About This Role
                        </h2>
                        <p className="text-gray-700 leading-relaxed">{job.description.summary}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-5">
                            Requirements
                        </h2>
                        <ul className="space-y-3">
                            {job.description.requirements.map((req: string, index: number) => (
                                <li key={index} className="flex items-start gap-3">
                                    <CheckCircleIcon className="w-5 h-5 text-indigo-600 mt-0.5 flex-shrink-0" />
                                    <span className="text-gray-700 text-sm leading-relaxed">
                                        {req}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-5">
                            Responsibilities
                        </h2>
                        <ul className="space-y-3">
                            {job.description.responsibilities.map((resp: string, index: number) => (
                                <li key={index} className="flex items-start gap-3">
                                    <CheckCircleIcon className="w-5 h-5 text-indigo-600 mt-0.5 flex-shrink-0" />
                                    <span className="text-gray-700 text-sm leading-relaxed">
                                        {resp}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-5">
                        Benefits & Perks
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {job.description.benefits.map((benefit: string, index: number) => (
                            <div
                                key={index}
                                className="flex items-center gap-3 px-4 py-3 bg-indigo-50 rounded-lg"
                            >
                                <CheckCircleIcon className="w-5 h-5 text-indigo-600 flex-shrink-0" />
                                <span className="text-gray-800 text-sm font-medium">
                                    {benefit}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 text-center">
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                        Interested in this role?
                    </h2>
                    <p className="text-gray-600 mb-6">
                        Create a tailored resume and apply today.
                    </p>
                    <button
                        onClick={onClose}
                        className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
                    >
                        Apply Now
                    </button>
                </div>
            </div>
        </div>
    )
}

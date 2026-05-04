import {
    ArrowLeftIcon,
    BriefcaseIcon,
    MapPinIcon,
    DollarSignIcon,
    ClockIcon,
    CheckCircleIcon,
    BuildingIcon,
    ZapIcon,
    SparklesIcon,
    FileTextIcon
} from 'lucide-react';
import { Navbar } from '../Components/Navbar'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useEffect } from 'react';

interface JobDetailsProps {
    job: any;
    onClose: () => void;
}

export function JobDetails({ job, onClose }: JobDetailsProps) {
    // Function to determine color based on ATS score
    function getScoreColor(score: number) {
        if (score >= 80)
            return {
                bar: 'bg-emerald-500',
                text: 'text-emerald-700',
                bg: 'bg-emerald-50',
                label: 'Excellent',
            }
        if (score >= 60)
            return {
                bar: 'bg-amber-500',
                text: 'text-amber-700',
                bg: 'bg-amber-50',
                label: 'Good',
            }
        return {
            bar: 'bg-red-400',
            text: 'text-red-700',
            bg: 'bg-red-50',
            label: 'Low',
        }
    }

    const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
    const [topResumes, setTopResumes] = useState<any[]>([]);

    const navigate = useNavigate();
    const api = import.meta.env.VITE_SERVER_URL + '/api/bestResume?job_id=' + job.id;
    // const [job, setJob] = useState<any>(null);

    useEffect(() => {
        // Fetch job details using the jobURL
        axios.get(api).then((response) => {
            if (response.data.status === "success") {
                setTopResumes(response.data);
            } else {
                setTopResumes([]);
            }
        }).catch((error) => {
            console.error('Error fetching job details:', error);
            setTopResumes([]);
        });
    }, [api]);

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

                {/* Job Details Section */}
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
                        <p className="text-gray-700 leading-relaxed">{job.parsed_desc.summary}</p>
                    </div>
                </div>

                {/* Requirements & Responsibilities Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-5">
                            Requirements
                        </h2>
                        <ul className="space-y-3">
                            {job.parsed_desc.requirements.map((req: string, index: number) => (
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
                            {job.parsed_desc.responsibilities.map((resp: string, index: number) => (
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

                {/* Best Matching Resumes Section */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-6">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="bg-amber-100 p-2.5 rounded-lg">
                            <ZapIcon className="w-5 h-5 text-amber-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                Best Matching Resumes
                            </h2>
                            <p className="text-sm text-gray-500 mt-0.5">
                                Ranked by ATS compatibility score for this role
                            </p>
                        </div>
                    </div>

                    {topResumes.length === 0 ? (
                        <div className="text-center py-8">
                            <FileTextIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                            <p className="text-gray-500 mb-4">
                                No resumes found. Create one to see your match score.
                            </p>
                            <button
                                onClick={() => navigate('/resumes/create')}
                                className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-indigo-700 transition"
                            >
                                Create Resume
                            </button>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {topResumes.map((resume, index) => {
                                const score = resume.atsScores[job.id] ?? 0
                                const colors = getScoreColor(score)
                                const isSelected = selectedResumeId === resume.id
                                return (
                                    <div
                                        key={resume.id}
                                        onClick={() =>
                                            setSelectedResumeId(isSelected ? null : resume.id)
                                        }
                                        className={`relative rounded-xl border-2 p-5 cursor-pointer transition-all ${isSelected ? 'border-indigo-600 bg-indigo-50/40 shadow-sm' : 'border-gray-200 hover:border-gray-300 bg-white'}`}
                                    >
                                        {index === 0 && (
                                            <span className="absolute -top-2.5 left-4 px-2.5 py-0.5 bg-amber-500 text-white text-xs font-semibold rounded-full">
                                                Best Match
                                            </span>
                                        )}

                                        <div className="flex items-center gap-4">
                                            <div
                                                className={`p-2.5 rounded-lg flex-shrink-0 ${isSelected ? 'bg-indigo-100' : 'bg-gray-100'}`}
                                            >
                                                <FileTextIcon
                                                    className={`w-5 h-5 ${isSelected ? 'text-indigo-600' : 'text-gray-500'}`}
                                                />
                                            </div>

                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center justify-between mb-2">
                                                    <h3 className="font-semibold text-gray-900 truncate pr-4">
                                                        {resume.name}
                                                    </h3>
                                                    <div
                                                        className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${colors.bg} ${colors.text}`}
                                                    >
                                                        {score}% — {colors.label}
                                                    </div>
                                                </div>

                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className={`h-2 rounded-full transition-all duration-500 ${colors.bar}`}
                                                        style={{
                                                            width: `${score}%`,
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        {isSelected && (
                                            <div className="mt-4 pt-4 border-t border-indigo-200 flex items-center justify-between">
                                                <p className="text-sm text-gray-600">
                                                    Tailor this resume to improve your ATS score for this
                                                    role.
                                                </p>
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation()
                                                        navigate(
                                                            `/resumes/create?tailorFrom=${resume.id}&jobId=${job.id}`,
                                                        )
                                                    }}
                                                    className="flex items-center gap-2 bg-indigo-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-indigo-700 transition flex-shrink-0"
                                                >
                                                    <SparklesIcon className="w-4 h-4" />
                                                    Tailor Resume
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                )
                            })}
                        </div>
                    )}
                </div>

                {/* Benefits & Perks Section */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-5">
                        Benefits & Perks
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {job.parsed_desc.benefits.map((benefit: string, index: number) => (
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

                {/* Final Section */}
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

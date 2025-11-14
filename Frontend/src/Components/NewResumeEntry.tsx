import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UploadIcon, FileTextIcon, ArrowLeftIcon } from 'lucide-react'
import { Navbar } from '../Components/Navbar'
import axios from 'axios'

export function CreateResume() {
    const navigate = useNavigate()
    const [title, setTitle] = useState('')
    const [resumeFile, setResumeFile] = useState<File | null>(null)
    const [jobDescription, setJobDescription] = useState<File | null>(null)

    const api = import.meta.env.VITE_SERVER_URL + '/api/grade';

    const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setResumeFile(e.target.files[0])
        }
    }

    const handleJDUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setJobDescription(e.target.files[0])
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        // Handle form submission logic here
        e.preventDefault()
        console.log(api)
        if (!resumeFile || !jobDescription) return;

        // Make API call to submit the form data
        // multipart/form-data
        const formDataObj = new FormData();
        formDataObj.append('title', title);
        formDataObj.append('resume', resumeFile);
        formDataObj.append('job_description', jobDescription);

        await axios.post(api, formDataObj, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log(response.data);
        }).catch((error) => {
            console.error("There was an error!", error);
        });
        // console.log(formData, title, resumeFile, jobDescription);

        // navigate('/resumes')
    }
    return (
        <div className="min-h-screen w-full bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 py-8">
                <button
                    onClick={() => navigate('/resumes')}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition"
                >
                    <ArrowLeftIcon className="w-5 h-5" />
                    Back to Resumes
                </button>
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="bg-indigo-100 p-3 rounded-lg">
                            <FileTextIcon className="w-6 h-6 text-indigo-600" />
                        </div>
                        <h1 className="text-2xl font-bold text-gray-900">
                            Create New Resume
                        </h1>
                    </div>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Resume Name
                            </label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                placeholder="e.g., Frontend Developer - TechCorp"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Upload Resume
                            </label>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition">
                                <input
                                    type="file"
                                    onChange={handleResumeUpload}
                                    accept=".pdf,.doc,.docx,.txt"
                                    className="hidden"
                                    id="resume-upload"
                                    required
                                />
                                <label
                                    htmlFor="resume-upload"
                                    className="cursor-pointer flex flex-col items-center"
                                >
                                    <UploadIcon className="w-12 h-12 text-gray-400 mb-4" />
                                    {resumeFile ? (
                                        <div className="text-indigo-600 font-medium">
                                            {resumeFile.name}
                                        </div>
                                    ) : (
                                        <>
                                            <p className="text-gray-700 font-medium mb-1">
                                                Click to upload or drag and drop
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                PDF, DOC, or DOCX (max. 10MB)
                                            </p>
                                        </>
                                    )}
                                </label>
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Job Description
                            </label>
                            {/* <textarea
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition resize-none"
                                rows={10}
                                placeholder="Paste the job description here..."
                                required
                            /> */}
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition">
                                <input
                                    type="file"
                                    onChange={handleJDUpload}
                                    accept=".pdf,.doc,.docx,.txt"
                                    className="hidden"
                                    id="job-description-upload"
                                    required
                                />
                                <label
                                    htmlFor="job-description-upload"
                                    className="cursor-pointer flex flex-col items-center"
                                >
                                    <UploadIcon className="w-12 h-12 text-gray-400 mb-4" />
                                    {jobDescription ? (
                                        <div className="text-indigo-600 font-medium">
                                            {jobDescription.name}
                                        </div>
                                    ) : (
                                        <>
                                            <p className="text-gray-700 font-medium mb-1">
                                                Click to upload or drag and drop
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                PDF, DOC, or DOCX (max. 10MB)
                                            </p>
                                        </>
                                    )}
                                </label>
                            </div>

                        </div>
                        <div className="flex gap-4 pt-4">
                            <button
                                type="button"
                                onClick={() => navigate('/resumes')}
                                className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition"
                            >
                                Create Resume
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

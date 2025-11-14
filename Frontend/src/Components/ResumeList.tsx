import { useNavigate } from 'react-router-dom'
import { FileTextIcon, PlusIcon, CalendarIcon } from 'lucide-react'
import { Navbar } from '../Components/Navbar'
import { useEffect, useState } from 'react'
import axios from 'axios'

let res = [
    {
        id: 1,
        name: 'Frontend Developer - TechCorp',
        createdDate: '2024-01-15',
        updatedDate: '2024-01-20',
    },
    {
        id: 2,
        name: 'Product Designer - Design Studio',
        createdDate: '2024-01-10',
        updatedDate: '2024-01-18',
    },
    {
        id: 3,
        name: 'Backend Engineer - StartupXYZ',
        createdDate: '2024-01-08',
        updatedDate: '2024-01-16',
    },
].sort(
    (a, b) =>
        new Date(b.updatedDate).getTime() - new Date(a.updatedDate).getTime(),
)
export function Resumes() {
    const navigate = useNavigate()

    const [resumes, setResumes] = useState([]);
    const api = import.meta.env.VITE_SERVER_URL + '/api/resumeEntries';

    const formatDate = (dateString: string) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        })
    }

    useEffect(() => {
        axios.get(api)
            .then(response => {
                console.log('Resume Entries:', response.data);
                setResumes(response.data.data);
            })
            .catch(error => {
                console.error('Error fetching resume entries:', error);
            });
    }, [setResumes]);

    return (
        <div className="min-h-screen w-full bg-gray-50">
            <Navbar />
            <div className="max-w-6xl mx-auto px-4 py-8">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 mb-2">
                            My Resumes
                        </h1>
                        <p className="text-gray-600">
                            Manage and create tailored resumes for different positions
                        </p>
                    </div>
                    <button
                        onClick={() => navigate('/resumes/create')}
                        className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition flex items-center gap-2"
                    >
                        <PlusIcon className="w-5 h-5" />
                        Create New Resume
                    </button>
                </div>
                <div className="space-y-4">
                    {resumes.map((resume) => (
                        <div
                            key={resume['id']}
                            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition cursor-pointer"
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex items-start gap-4 flex-1">
                                    <div className="bg-indigo-100 p-3 rounded-lg">
                                        <FileTextIcon className="w-6 h-6 text-indigo-600" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-xl font-semibold text-gray-900 mb-3">
                                            {resume['title']}
                                        </h3>
                                        <div className="flex gap-6 text-sm text-gray-600">
                                            <div className="flex items-center gap-2">
                                                <CalendarIcon className="w-4 h-4" />
                                                <span>Created: {formatDate(resume['created_date'])}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <CalendarIcon className="w-4 h-4" />
                                                <span>Updated: {formatDate(resume['updated_date'])}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <button className="px-4 py-2 text-indigo-600 border border-indigo-600 rounded-lg font-medium hover:bg-indigo-50 transition">
                                        Edit
                                    </button>
                                    <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition">
                                        Download
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

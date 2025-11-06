import { useNavigate, useLocation } from 'react-router-dom'
import {
    FileTextIcon,
    BriefcaseIcon,
    FolderIcon,
    LogOutIcon,
} from 'lucide-react'

export function Navbar() {
    const navigate = useNavigate()
    const location = useLocation()
    const isActive = (path: string) => location.pathname === path
    return (
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center gap-8">
                        <div
                            className="flex items-center gap-2 cursor-pointer"
                            onClick={() => navigate('/resumes')}
                        >
                            <div className="bg-indigo-600 p-2 rounded-lg">
                                <FileTextIcon className="w-5 h-5 text-white" />
                            </div>
                            <span className="text-xl font-bold text-gray-900">
                                ResumeForge
                            </span>
                        </div>
                        <div className="flex gap-1">
                            <button
                                onClick={() => navigate('/resumes')}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition ${isActive('/resumes') || isActive('/resumes/create') ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-50'}`}
                            >
                                <FolderIcon className="w-5 h-5" />
                                My Resumes
                            </button>
                            <button
                                onClick={() => navigate('/job-openings')}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition ${isActive('/job-openings') ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-50'}`}
                            >
                                <BriefcaseIcon className="w-5 h-5" />
                                Job Openings
                            </button>
                        </div>
                    </div>
                    <button
                        onClick={() => navigate('/')}
                        className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 transition"
                    >
                        <LogOutIcon className="w-5 h-5" />
                        Sign Out
                    </button>
                </div>
            </div>
        </nav>
    )
}

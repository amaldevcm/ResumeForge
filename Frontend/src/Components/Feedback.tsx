import { Navbar } from "./Navbar"

export function Feedback() {
    return (
        <div className="min-h-screen w-full bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto mt-12 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="p-6 border-b border-gray-200">
                    <h2 className="text-2xl font-bold text-gray-800">
                        Resume Analysis Results
                    </h2>
                    <p className="text-gray-600 mt-1">
                        Here's how your resume matches the job description
                    </p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3">
                    <div className="p-6 flex justify-center border-b lg:border-b-0 lg:border-r border-gray-200"
                        id="resumeScore">
                        <img src="data:image/png;base64, {{ chart }}" alt="Score card" />
                    </div>
                    <div className="col-span-2 p-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4 font-bold">
                            Improvement Suggestions
                        </h3>
                        <ul className="space-y-3" id="suggestion"></ul>
                    </div>
                </div>
                <div className="border-t border-gray-200">
                    <div className="p-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4 font-bold">
                            Keyword Analysis
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="bg-green-50 p-4 rounded-lg">
                                <h4 className="font-medium text-green-800 flex items-center gap-2 mb-3">
                                    <i className="bi bi-check2-circle text-lg"></i>
                                    <span>Matched Keywords</span>
                                </h4>
                                <div className="flex flex-wrap gap-2" id="matchedSkill"></div>
                            </div>
                            <div className="bg-red-50 p-4 rounded-lg">
                                <h4 className="font-medium text-red-800 flex items-center gap-2 mb-3">
                                    <i className="bi bi-x-circle text-lg"></i>
                                    <span>Missing Keywords</span>
                                </h4>
                                <div className="flex flex-wrap gap-2" id="missingSkill"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="border-t border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4 font-bold">
                        Section Feedback
                    </h3>
                    <div className="space-y-4" id="sectionFeedback"></div>
                </div>
                <div className="bg-blue-50 p-6 border-t border-blue-100">
                    <div className="flex items-start gap-4">
                        <div className="px-2 py-1 bg-blue-100 rounded-full">
                            <i className="bi bi-arrow-right h-5 w-6 text-blue-700"></i>
                        </div>
                        <div>
                            <h3 className="text-lg font-medium text-blue-800 font-bold">Next Steps</h3>
                            <p className="text-blue-700 mt-1">
                                Make the suggested improvements to your resume and re-upload for a
                                new analysis. Focus on adding the missing keywords and
                                strengthening the sections that need improvement.
                            </p>
                        </div>
                    </div>
                </div>
            </div>


            <div className="mt-8 flex justify-center gap-4 clickable">
                <button type="submit"
                    className="px-6 py-3 rounded-lg font-medium border border-gray-300 hover:bg-gray-100 transition-colors">
                    Customize
                </button>
            </div>
        </div>
    )
}
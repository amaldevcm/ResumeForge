import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login } from './Components/Login'
import { JobOpenings } from './Components/JobList'
import { Resumes } from './Components/ResumeList'
import { SignUp } from './Components/Signup'
import { CreateResume } from './Components/NewResumeEntry'
import { Feedback } from './Components/Feedback'

export function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/job-openings" element={<JobOpenings />} />
                <Route path="/resumes" element={<Resumes />} />
                <Route path="/resumes/create" element={<CreateResume />} />
                <Route path="/resumes/feedback" element={<Feedback />} />
            </Routes>
        </BrowserRouter>
    )
}

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login } from './Pages/Login'
import { JobOpenings } from './Pages/JobList'
import { Resumes } from './Pages/ResumeList'
import { SignUp } from './Pages/Signup'
import { CreateResume } from './Pages/NewResumeEntry'
import { Feedback } from './Pages/Feedback'
import { Profile } from './Pages/Profile'

export function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/job-openings" element={<JobOpenings />} />
                <Route path="/resumes" element={<Resumes />} />
                <Route path="/resumes/create" element={<CreateResume isEdited={false} id={null} />} />
                <Route path="/resumes/feedback" element={<Feedback />} />
                <Route path="/profile" element={<Profile />} />
            </Routes>
        </BrowserRouter>
    )
}

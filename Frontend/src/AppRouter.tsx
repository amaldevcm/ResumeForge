import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login } from './Components/Login'
import { JobOpenings } from './Components/jobList'
import { Resumes } from './Components/ResumeList'
// import { CreateResume } from './pages/CreateResume'

export function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/job-openings" element={<JobOpenings />} />
                <Route path="/resumes" element={<Resumes />} />
                {/* <Route path="/resumes/create" element={<CreateResume />} /> */}
            </Routes>
        </BrowserRouter>
    )
}

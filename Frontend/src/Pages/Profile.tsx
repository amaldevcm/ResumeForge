import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UserIcon, MailIcon, LockIcon, Trash2Icon } from 'lucide-react'
import { Navbar } from '../Components/Navbar'
import { Spinner } from '../Components/Spinner'
import axios from 'axios'

export function Profile() {
    const navigate = useNavigate()
    const [isLoading, setIsLoading] = useState(true)

    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [email, setEmail] = useState('')

    const [currentPassword, setCurrentPassword] = useState('')
    const [newPassword, setNewPassword] = useState('')
    const [confirmNewPassword, setConfirmNewPassword] = useState('')

    const api = import.meta.env.VITE_SERVER_URL + '/api/';

    useEffect(() => {
        axios.get(api + 'currentUser')
            .then(response => {
                const user = response.data.user
                setFirstName(user.first_name || '')
                setLastName(user.last_name || '')
                setEmail(user.email || '')
                setIsLoading(false)
            })
            .catch(error => {
                console.error('Error fetching current user:', error)
                setIsLoading(false)
            })
    }, []);

    const handleSaveProfile = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await axios.put(api + 'updateProfile', {
                first_name: firstName,
                last_name: lastName,
                email,
            })
            alert('Profile updated successfully')
        } catch (error: any) {
            alert(error.response?.data?.message || 'Failed to update profile')
        }
    }

    const handleChangePassword = async (e: React.FormEvent) => {
        e.preventDefault()
        if (newPassword !== confirmNewPassword) {
            alert('New passwords do not match')
            return
        }
        try {
            await axios.post(api + 'changePassword', {
                current_password: currentPassword,
                new_password: newPassword,
            })
            setCurrentPassword('')
            setNewPassword('')
            setConfirmNewPassword('')
            alert('Password updated successfully')
        } catch (error: any) {
            alert(error.response?.data?.message || 'Failed to update password')
        }
    }

    const handleDeleteAccount = async () => {
        if (!window.confirm('Are you sure you want to delete your account? This cannot be undone.')) {
            return
        }
        try {
            await axios.delete(api + 'deleteAccount')
            navigate('/')
        } catch (error: any) {
            alert(error.response?.data?.message || 'Failed to delete account')
        }
    }

    return (
        <>
            {isLoading ? (
                <Spinner fullPage label="Loading profile..." />
            ) : (
                <div className="min-h-screen w-full bg-gray-50">
                    <Navbar />
                    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 mb-2">
                                Profile
                            </h1>
                            <p className="text-gray-600">
                                Manage your account information and security
                            </p>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-xl font-semibold text-gray-900 mb-6">
                                Profile Information
                            </h2>
                            <form onSubmit={handleSaveProfile} className="space-y-5">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        First Name
                                    </label>
                                    <div className="relative">
                                        <UserIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="text"
                                            value={firstName}
                                            onChange={(e) => setFirstName(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Last Name
                                    </label>
                                    <div className="relative">
                                        <UserIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="text"
                                            value={lastName}
                                            onChange={(e) => setLastName(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Email
                                    </label>
                                    <div className="relative">
                                        <MailIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            required
                                        />
                                    </div>
                                </div>
                                <button
                                    type="submit"
                                    className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
                                >
                                    Save Changes
                                </button>
                            </form>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-xl font-semibold text-gray-900 mb-6">
                                Change Password
                            </h2>
                            <form onSubmit={handleChangePassword} className="space-y-5">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Current Password
                                    </label>
                                    <div className="relative">
                                        <LockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="password"
                                            value={currentPassword}
                                            onChange={(e) => setCurrentPassword(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            placeholder="••••••••"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        New Password
                                    </label>
                                    <div className="relative">
                                        <LockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="password"
                                            value={newPassword}
                                            onChange={(e) => setNewPassword(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            placeholder="••••••••"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Confirm New Password
                                    </label>
                                    <div className="relative">
                                        <LockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="password"
                                            value={confirmNewPassword}
                                            onChange={(e) => setConfirmNewPassword(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                                            placeholder="••••••••"
                                            required
                                        />
                                    </div>
                                </div>
                                <button
                                    type="submit"
                                    className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
                                >
                                    Update Password
                                </button>
                            </form>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
                            <h2 className="text-xl font-semibold text-red-600 mb-2">
                                Danger Zone
                            </h2>
                            <p className="text-gray-600 mb-6">
                                Deleting your account permanently removes your profile and login access. This cannot be undone.
                            </p>
                            <button
                                onClick={handleDeleteAccount}
                                className="flex items-center gap-2 bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 transition"
                            >
                                <Trash2Icon className="w-5 h-5" />
                                Delete Account
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}

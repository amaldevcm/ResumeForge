import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppRouter } from './AppRouter'

function App() {

  return (
    <>
      <Toaster position="top-right" toastOptions={{ duration: 4000 }} />
      <AppRouter />
    </>
  )
}

export default App

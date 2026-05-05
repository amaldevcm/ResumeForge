import { Loader2Icon } from 'lucide-react'
interface SpinnerProps {
    label?: string
    size?: 'sm' | 'md' | 'lg'
    fullPage?: boolean
}
export function Spinner({
    label = 'Loading...',
    size = 'md',
    fullPage = false,
}: SpinnerProps) {
    const sizeClass = {
        sm: 'w-5 h-5',
        md: 'w-8 h-8',
        lg: 'w-12 h-12',
    }[size]
    const content = (
        <div className="flex flex-col items-center justify-center gap-3">
            <Loader2Icon className={`${sizeClass} text-indigo-600 animate-spin`} />
            {label && <p className="text-sm text-gray-600 font-medium">{label}</p>}
        </div>
    )
    if (fullPage) {
        return (
            <div className="flex items-center justify-center py-24">{content}</div>
        )
    }
    return content
}
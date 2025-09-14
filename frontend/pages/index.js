import { useUser } from '@auth0/nextjs-auth0/client';
import Link from 'next/link';

export default function Index() {
  const { user, isLoading } = useUser();

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center p-8 bg-white rounded-lg shadow-xl">
        <h1 className="text-4xl font-bold mb-4">N-Device Auth App</h1>
        {isLoading && <p>Loading login status...</p>}
        {!isLoading && !user && (
          <>
            <p className="mb-6 text-lg">Please log in to manage your account.</p>
            <a href="/api/auth/login" className="bg-blue-600 text-white font-semibold px-6 py-3 rounded-md hover:bg-blue-700 transition-colors">
              Login
            </a>
          </>
        )}
        {user && (
          <>
            <p className="mb-6 text-lg">Welcome back, <strong>{user.name}</strong>!</p>
            <div className="space-x-4">
              <Link href="/profile" className="bg-green-600 text-white font-semibold px-6 py-3 rounded-md hover:bg-green-700 transition-colors">
                  Go to Profile
              </Link>
              <a href="/api/auth/logout" className="bg-red-500 text-white font-semibold px-6 py-3 rounded-md hover:bg-red-600 transition-colors">
                Logout
              </a>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
import { useUser } from '@auth0/nextjs-auth0/client';
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

function Profile() {
  const { user, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="p-8 bg-white rounded-lg shadow-xl w-full max-w-md">
            <h1 className="text-3xl font-bold mb-6 text-center">User Profile</h1>
            <div className="space-y-4">
                <div className="flex items-center space-x-4">
                    <img src={user.picture} alt="Profile" className="w-20 h-20 rounded-full" />
                    <div>
                        <h2 className="text-xl font-semibold">{user.name}</h2>
                        <p className="text-gray-500">{user.email}</p>
                    </div>
                </div>
                <div>
                    <h3 className="font-semibold">Full Name:</h3>
                    <p>{user.name || 'Not Provided'}</p>
                </div>
                 <div>
                    <h3 className="font-semibold">Phone Number:</h3>
                    {/* This custom claim comes from the Auth0 Action we set up earlier */}
                    <p>{user['https://3device-app.com/phone_number'] || 'Not Provided'}</p>
                </div>
            </div>
             <a href="/api/auth/logout" className="block w-full text-center mt-8 bg-gray-200 text-gray-800 font-semibold px-6 py-3 rounded-md hover:bg-gray-300 transition-colors">
                Logout
              </a>
        </div>
    </div>
  );
}

// This wrapper protects the page and handles redirection
export default withPageAuthRequired(Profile);
import React from 'react';
import { UserProvider } from '@auth0/nextjs-auth0/client';
import SessionManager from '../components/SessionManager'; // Import it
import { Toaster } from 'react-hot-toast';
import '../styles/globals.css';

export default function App({ Component, pageProps }) {
  return (
    <UserProvider>
      {/* SessionManager runs in the background on all pages */}
      <SessionManager /> 
      <Toaster position="top-center" />
      <Component {...pageProps} />
    </UserProvider>
  );
}
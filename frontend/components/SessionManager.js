import { useEffect, useState } from 'react';
import { useUser } from '@auth0/nextjs-auth0/client';
import apiClient from '../lib/apiClient';
import toast from 'react-hot-toast';

// Helper to get or create a unique device ID
const getDeviceId = () => {
  let deviceId = localStorage.getItem('deviceId');
  if (!deviceId) {
    deviceId = crypto.randomUUID();
    localStorage.setItem('deviceId', deviceId);
  }
  return deviceId;
};

const SessionManager = () => {
  const { user, isLoading } = useUser();
  // We will build the modals in the next step. For now, we just log.
  const [showDeviceLimitModal, setShowDeviceLimitModal] = useState(false);
  const [showLoggedOutModal, setShowLoggedOutModal] = useState(false);
  const [activeDevices, setActiveDevices] = useState([]);

  useEffect(() => {
    if (user && !isLoading) {
      const deviceId = getDeviceId();

      const handleLogin = async () => {
        try {
          const { data } = await apiClient.post('/api/v1/sessions/login', { device_id: deviceId });
          
          if (data.status === 'limit_exceeded') {
            toast.error('Device limit reached!');
            setActiveDevices(data.devices);
            setShowDeviceLimitModal(true); // This will trigger the modal
          } else {
            console.log('Device session active.');
          }
        } catch (error) {
          console.error('Login session error:', error);
          toast.error('Could not verify device session.');
        }
      };

      handleLogin();

      // Start heartbeat every 30 seconds
      const intervalId = setInterval(async () => {
        try {
          const { data } = await apiClient.post('/api/v1/sessions/heartbeat', { device_id: deviceId });
          if (data.status === 'inactive') {
            setShowLoggedOutModal(true); // Trigger graceful logout modal
            clearInterval(intervalId); // Stop heartbeat
          }
        } catch (error) {
          // If token expired or other auth error, Auth0 will handle logout
          console.error('Heartbeat error:', error);
          clearInterval(intervalId);
        }
      }, 30000);

      // Cleanup on component unmount
      return () => clearInterval(intervalId);
    }
  }, [user, isLoading]);

  
  if (showDeviceLimitModal) {
    // Placeholder for DeviceLimitModal
    console.log("SHOULD SHOW DEVICE LIMIT MODAL with devices:", activeDevices);
  }
  if (showLoggedOutModal) {
    // Placeholder for LoggedOutModal
    console.log("SHOULD SHOW LOGGED OUT MODAL");
  }

  return null;
};

export default SessionManager;
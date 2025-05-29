import React, { useEffect, useState } from 'react';
import { Box, CircularProgress } from '@mui/material';
import MainPage from './MainPage';
import UserSelectModal from './UserSelectModal';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("selectedUser");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleUserSelect = (selectedUser) => {
    localStorage.setItem("selectedUser", JSON.stringify(selectedUser));
    setUser(selectedUser);
  };

  if (!user) {
    return <UserSelectModal onSelect={handleUserSelect} />;
  }

  return (
    <Box>
      <MainPage user={user} />
    </Box>
  );
}

export default App;

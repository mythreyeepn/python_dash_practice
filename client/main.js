import React, { useEffect, useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import axios from 'axios';

function UserSelectModal({ onSelect }) {
  const [open, setOpen] = useState(true);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");

  useEffect(() => {
    axios.get("/users").then((res) => {
      setUsers(res.data || []);
    });
  }, []);

  const handleConfirm = () => {
    if (!selectedUser) return;
    const userObj = users.find((u) => u.user_id === selectedUser);
    onSelect(userObj);
    setOpen(false);
  };

  return (
    <Dialog open={open}>
      <DialogTitle>Select User</DialogTitle>
      <DialogContent>
        <FormControl fullWidth>
          <InputLabel>User</InputLabel>
          <Select
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            label="User"
          >
            {users.map((u) => (
              <MenuItem key={u.user_id} value={u.user_id}>
                {u.first_name} {u.last_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleConfirm} disabled={!selectedUser}>
          Continue
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default UserSelectModal;

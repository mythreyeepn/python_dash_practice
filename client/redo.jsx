
import React from "react";
import { Button } from "@mui/material";
import { handleRedo } from "./handleRedo";

const RedoButton = ({ currentUser }) => {
  const onClick = () => {
    if (!currentUser) {
      alert("User not selected");
      return;
    }
    handleRedo(currentUser);
  };

  return (
    <Button variant="outlined" onClick={onClick}>
      Redo
    </Button>
  );
};

export default RedoButton;



import axios from "axios";

export const handleRedo = async (currentUser) => {
  try {
    const response = await axios.post("/skews_redo", {
      user_id: currentUser.id
    });

    console.log("Redo success for group:", response.data.restored_group);
    return response.data;
  } catch (err) {
    console.error("Redo failed:", err.response?.data?.detail || err.message);
    alert("Nothing to redo or redo failed.");
  }
};
import { Box, Typography } from "@mui/material";
import React from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";

const InfoDisplay: React.FC = () => {
  const poseStatus = useSelector((state: RootState) => state.pose.status);

  return (
    <Box
      sx={{
        flex: 1,
        bgcolor: "background.paper",
        p: 2,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Typography variant="h6">Information</Typography>
      <Typography variant="body1">{poseStatus}</Typography>
    </Box>
  );
};

export default InfoDisplay;

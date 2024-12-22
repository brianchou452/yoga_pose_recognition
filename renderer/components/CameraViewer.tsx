import { Box, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";

const CameraViewer: React.FC = () => {
  const [timeLeft, setTimeLeft] = useState(60);
  const poseStatus = useSelector((state: RootState) => state.pose.status);

  useEffect(() => {
    const timer = setInterval(() => {
      if (poseStatus === "Pose is correct") {
        setTimeLeft((prevTime) => (prevTime > 0 ? prevTime - 1 : 60));
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [poseStatus]);

  return (
    <Box
      sx={{
        flex: 4,
        position: "relative",
      }}
    >
      <Box
        component="img"
        src="http://127.0.0.1:8000/api/video/frame"
        alt="Live Frame"
        sx={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
      <Box
        sx={{
          position: "absolute",
          top: 16,
          right: 16,
          bgcolor: "rgba(0, 0, 0, 0.5)",
          color: "white",
          p: 1,
          borderRadius: 1,
        }}
      >
        <Typography variant="h6">{timeLeft}s</Typography>
      </Box>
    </Box>
  );
};

export default CameraViewer;

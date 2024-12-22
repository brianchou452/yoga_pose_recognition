import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { Box, Typography } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import CameraViewer from "../components/CameraViewer";
import { RootState } from "../store";
import { setPoseStatus } from "../store/slices/poseSlice";

export default function HomePage() {
  const dispatch = useDispatch();
  const poseStatus = useSelector((state: RootState) => state.pose.status);

  React.useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/api/video/is_pose_wrong/ws");
    ws.onmessage = (event) => {
      console.log(event.data);
      dispatch(
        setPoseStatus(
          event.data === "True" ? "Pose is wrong" : "Pose is correct"
        )
      );
    };

    return () => {
      ws.close();
    };
  }, [dispatch]);

  return (
    <Box
      sx={{
        display: "flex",
        height: "100vh",
        overflow: "hidden",
        margin: 0,
      }}
    >
      <CameraViewer />
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
    </Box>
  );
}

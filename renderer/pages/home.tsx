import { Box } from "@mui/material";
import React from "react";
import { useDispatch } from "react-redux";
import CameraViewer from "../components/CameraViewer";
import InfoDisplay from "../components/InfoDisplay";
import { setIsPoseWrong, setPoseStatus } from "../store/slices/poseSlice";

export default function HomePage() {
  const dispatch = useDispatch();

  React.useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/api/video/is_pose_wrong/ws");
    ws.onmessage = (event) => {
      const isWrong = event.data === "True";
      dispatch(setPoseStatus(isWrong ? "Pose is wrong" : "Pose is correct"));
      dispatch(setIsPoseWrong(isWrong));
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
      <InfoDisplay />
    </Box>
  );
}

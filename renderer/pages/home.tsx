import { Box } from "@mui/material";
import CameraViewer from "../components/CameraViewer";
import InfoDisplay from "../components/InfoDisplay";

export default function HomePage() {
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

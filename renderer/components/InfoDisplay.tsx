import {
  Box,
  Button,
  List,
  ListItem,
  MenuItem,
  Select,
  SelectChangeEvent,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";
import { setPoseStatus, setTimeLeft } from "../store/slices/poseSlice";

interface Course {
  id: number;
  name: string;
  description: string;
  poses: { id: string; server_id: string; name: string; duration: number }[];
}

const InfoDisplay: React.FC = () => {
  const dispatch = useDispatch();
  const poseStatus = useSelector((state: RootState) => state.pose.status);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [currentPoseId, setCurrentPoseId] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      const response = await fetch("http://localhost:8000/api/course/");
      const data = await response.json();
      setCourses(data.courses);
    };

    fetchCourses();
  }, []);

  const handleCourseChange = (event: SelectChangeEvent<number>) => {
    const courseId = event.target.value as number;
    const course = courses.find((course) => course.id === courseId) || null;
    setSelectedCourse(course);
  };

  const setServerPoseId = async (poseId: string) => {
    await fetch("http://localhost:8000/api/video/pose", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pose_id: poseId }),
    });
  };

  const handleStart = async () => {
    let isPoseWrong = false;
    if (selectedCourse) {
      const ws = new WebSocket(
        "ws://127.0.0.1:8000/api/video/is_pose_wrong/ws"
      );
      ws.onmessage = (event) => {
        const isWrong = event.data == "True";
        dispatch(setPoseStatus(isWrong ? "Pose is wrong" : "Pose is correct"));
        isPoseWrong = isWrong;
      };

      for (const pose of selectedCourse.poses) {
        setCurrentPoseId(pose.id);
        await setServerPoseId(pose.server_id);
        dispatch(setTimeLeft(pose.duration));

        let localTimeLeft = pose.duration;
        let previousTime: number;
        while (true) {
          previousTime = Date.now();
          await new Promise((resolve) => setTimeout(resolve, 1000));
          const elapsedTime = (Date.now() - previousTime) / 1000;
          if (!isPoseWrong) {
            localTimeLeft = localTimeLeft - elapsedTime;
            const displayTimeLeft = Math.max(0, Math.floor(localTimeLeft));
            dispatch(setTimeLeft(displayTimeLeft));
          }

          if (!isPoseWrong && localTimeLeft <= 0) {
            break;
          }
        }
      }
      dispatch(setPoseStatus("Course completed"));
      setCurrentPoseId(null);
      await setServerPoseId("no_pose");
      ws.close();
    }
  };

  return (
    <Box
      sx={{
        flex: 1,
        bgcolor: "background.paper",
        p: 2,
        display: "flex",
        flexDirection: "column",
        justifyContent: "top",
        alignItems: "center",
      }}
    >
      <Typography variant="body1">{poseStatus}</Typography>
      <Box sx={{ display: "flex", alignItems: "center", mt: 2 }}>
        <Select
          value={selectedCourse?.id || ""}
          onChange={handleCourseChange}
          displayEmpty
          sx={{ minWidth: 200, mr: 2 }}
        >
          <MenuItem value="" disabled>
            Select a course
          </MenuItem>
          {courses.map((course) => (
            <MenuItem key={course.id} value={course.id}>
              {course.name}
            </MenuItem>
          ))}
        </Select>
        <Button variant="contained" onClick={handleStart}>
          Start
        </Button>
      </Box>
      {selectedCourse && (
        <Box sx={{ mt: 2, overflowY: "auto", width: "100%" }}>
          <Typography variant="h6">Poses</Typography>
          <List>
            {selectedCourse.poses.map((pose) => (
              <ListItem
                key={pose.id}
                sx={{
                  bgcolor: pose.id === currentPoseId ? "grey.300" : "inherit",
                }}
              >
                <Typography variant="body1">
                  {pose.name} - {pose.duration}s
                </Typography>
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
};

export default InfoDisplay;

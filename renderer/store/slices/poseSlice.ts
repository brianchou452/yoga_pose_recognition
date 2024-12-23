import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface PoseState {
    status: string;
    timeLeft: number;
}

const initialState: PoseState = {
    status: "選一門課程開始練習",
    timeLeft: 0,
};

const poseSlice = createSlice({
    name: "pose",
    initialState,
    reducers: {
        setPoseStatus(state, action: PayloadAction<string>) {
            state.status = action.payload;
        },
        setTimeLeft(state, action: PayloadAction<number>) {
            state.timeLeft = action.payload;
        },
    },
});

export const { setPoseStatus, setTimeLeft } = poseSlice.actions;
export default poseSlice.reducer;

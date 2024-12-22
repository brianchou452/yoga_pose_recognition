import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface PoseState {
    status: string;
    duration: number;
    isPoseWrong: boolean;
}

const initialState: PoseState = {
    status: "Checking...",
    duration: 0,
    isPoseWrong: false,
};

const poseSlice = createSlice({
    name: "pose",
    initialState,
    reducers: {
        setPoseStatus(state, action: PayloadAction<string>) {
            state.status = action.payload;
        },
        setPoseDuration(state, action: PayloadAction<number>) {
            state.duration = action.payload;
        },
        setIsPoseWrong(state, action: PayloadAction<boolean>) {
            state.isPoseWrong = action.payload;
        },
    },
});

export const { setPoseStatus, setPoseDuration, setIsPoseWrong } = poseSlice.actions;
export default poseSlice.reducer;

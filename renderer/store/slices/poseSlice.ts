import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface PoseState {
    status: string;
}

const initialState: PoseState = {
    status: "Checking...",
};

const poseSlice = createSlice({
    name: "pose",
    initialState,
    reducers: {
        setPoseStatus(state, action: PayloadAction<string>) {
            state.status = action.payload;
        },
    },
});

export const { setPoseStatus } = poseSlice.actions;
export default poseSlice.reducer;

import { configureStore } from "@reduxjs/toolkit";
import poseReducer from "./slices/poseSlice";

const store = configureStore({
    reducer: {
        pose: poseReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Angle(BaseModel):
    connection1: str
    connection2: str
    value: int


class Pose(BaseModel):
    name: str
    angles: List[Angle]


class PoseData(BaseModel):
    poses: List[Pose]

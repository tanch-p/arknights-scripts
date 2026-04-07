from __future__ import annotations

from typing import TypedDict

from .common import ItemCost


class StoryRequiredStage(TypedDict):
    stageId: str
    minState: str  # "PLAYED" | "PASS" | "COMPLETE"
    maxState: str


class StoryUnlockData(TypedDict):
    storyReviewType: str  # "NONE" | ...
    storyId: str
    storyGroup: str
    storySort: int
    storyDependence: str | None
    storyCanShow: int
    storyCode: str
    storyName: str
    storyPic: str | None
    storyInfo: str
    storyCanEnter: int
    storyTxt: str
    avgTag: str
    unLockType: str  # "BY_START_TIME" | "CONDITION" | ...
    costItemType: str  # "NONE" | ...
    costItemId: str | None
    costItemCount: int
    stageCount: int
    requiredStages: list[StoryRequiredStage]


class StoryReviewEntry(TypedDict):
    id: str
    name: str
    entryType: str  # "ACTIVITY" | "MAINLINE" | ...
    actType: str  # "ACTIVITY_STORY" | "MAINLINE_STORY" | ...
    startTime: int
    endTime: int
    startShowTime: int
    endShowTime: int
    remakeStartTime: int
    remakeEndTime: int
    storyEntryPicId: str
    storyPicId: str | None
    storyMainColor: str | None
    customType: int
    storyCompleteMedalId: str | None
    rewards: list[ItemCost]
    infoUnlockDatas: list[StoryUnlockData]


# Top-level type: story set ID → entry
StoryReviewTable = dict[str, StoryReviewEntry]

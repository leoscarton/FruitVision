import cv2
import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

@dataclass
class VideoInfo:
    video_file_path: Path
    fps: float
    total_frames: int
    width: int
    height: int
    duration_seconds: float

@dataclass
class FrameMetadata:
    index: int
    timestamp_seconds: float
    file_path: Path

class VideoFrameExtractor:
    def __init__(self, video_path: str, output_dir: str):
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
        self.cap: Optional[cv2.VideoCapture] = None
        self.info: Optional[VideoInfo] = None
        self.metadata: List[FrameMetadata] = []

    def __enter__(self):
        self._open_video()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _open_video(self) -> None:
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {self.video_path}")

        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise IOError (f"Could not open video: {self.video_path}")

        fps = self.cap.get(cv2.CAP_PROP_FPS) or 0.0
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0.0

        self.info(
            video_path = self.video_path,
            fps = fps,
            total_frames = total_frames,
            width = width,
            height = height,
            duration_seconds = duration
        )

        logger.info(
            "Video open: %s | %.2f fps | %d frames | %dx%d | %.2fs",
            self.video_path.name, fps, total_frames, width, height, duration
        )

    def extract(self, mode: str = "interval", value:float = 30, prefix: str = "frame", format: str = "jpg") -> List[FrameMetadata]:
        if self.cap is None or self.info is None:
            raise RuntimeError(
                "Video was not opened"
            )

        if mode == "time":
            frame_step = max(1, round(self.info.fps*value)) if self.info.fps > 0 else 1
        elif mode == "all":
            frame_step = 1
        elif mode == "interval":
            frame_step = max(1, int(value))
        else:
            raise ValueError(f"Invalid mode: {mode}")

        index = 0
        saved_frames = 0

        while True:
            success, frame = self.cap.read()
            if not success:
                break

            if index % frame_step == 0:
                timestamp = index / self.info.fps if self.info.fps > 0 else 0.0
                file_name = f"{prefix}_{index:06d}.{format}"
                output_path = self.output_dir / file_name

                cv2.imwrite(str(output_path), frame)

                self.metadata.append(
                    FrameMetadata(
                        index=index,
                        timestamp_seconds=timestamp,
                        file_path=output_path
                    )
                )
                saved_frames += 1

            index += 1

        logger.info(f"Extraction finished: {saved_frames} frames saved in {self.output_dir}")

        return self.metadata

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
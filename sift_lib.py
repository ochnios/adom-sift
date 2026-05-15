from enum import Enum

import cv2
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import dataclass
from typing import Optional, Dict, Any


class SiftMatcherType(Enum):
    BFMatcher = 1
    FLANN = 2


@dataclass
class SiftConfig:
    """Configuration parameters for SIFT matcher."""
    matcher_type: SiftMatcherType = SiftMatcherType.BFMatcher
    norm_type: int = cv2.NORM_L2  # cv2.NORM_L2 / cv2.NORM_L1
    ratio_threshold: float = 0.75  # Lowe test threshold
    cross_check: bool = False  # BFMatcher flag ( (wzajemnie najlepsze dopasowania)
    flann_index_params: Optional[Dict[str, Any]] = None
    flann_search_params: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize FLANN params."""
        if self.matcher_type == SiftMatcherType.FLANN:
            FLANN_INDEX_KDTREE = 1
            if self.flann_index_params is None:
                self.flann_index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            if self.flann_search_params is None:
                self.flann_search_params = dict(checks=50)


class SiftMatcher:

    def __init__(self, config: SiftConfig = SiftConfig()):
        self.sift = cv2.SIFT_create()
        self.config = config
        self.matcher = cv2.BFMatcher(cv2.NORM_L2)

        if self.config.matcher_type == SiftMatcherType.BFMatcher:
            self.matcher = cv2.BFMatcher(
                normType=self.config.norm_type,
                crossCheck=self.config.cross_check
            )
        elif self.config.matcher_type == SiftMatcherType.FLANN:
            self.matcher = cv2.FlannBasedMatcher(
                self.config.flann_index_params,
                self.config.flann_search_params
            )
        else:
            raise ValueError('Unknown SIFT matcher.')

    @staticmethod
    def load_image(path: str) -> np.ndarray:
        """
        Loads image from path.
        :param path: Path to image
        :return: Loaded image
        """
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Failed to load image: {path}")
        return img

    def extract_features(self, image: np.ndarray):
        """
        Extracts feature points and their descriptors from the image.
        :param image: Image to extract features from
        :return: Tuple of keypoints and descriptors
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        return keypoints, descriptors

    @staticmethod
    def draw_features(image: np.ndarray, keypoints: list, rich_display: bool = False) -> np.ndarray:
        """
        Draws local features onto the image.
        :param image: Source image with extracted features
        :param keypoints: Key points of the image
        :param rich_display: Indicates whether to display additional details, such as orientation
        :return: Image with drawn local features
        """
        flag = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS if rich_display else cv2.DRAW_MATCHES_FLAGS_DEFAULT

        result_image = cv2.drawKeypoints(
            image,
            keypoints,
            None,
            color=(0, 0, 255),
            flags=flag
        )
        return result_image

    def find_matches(self, descriptors1: np.ndarray, descriptors2: np.ndarray) -> list:
        """
        Discovers best feature matches using configured matcher.
        :param descriptors1: Descriptors of the first image features
        :param descriptors2: Descriptors of the second image features
        :return: Matching feature points
        """
        if self.config.matcher_type == SiftMatcherType.BFMatcher and self.config.cross_check:
            raw_matches = self.matcher.match(descriptors1, descriptors2)
            good_matches = sorted(raw_matches, key=lambda x: x.distance)
        else:
            # KNN + Lowe test
            raw_matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)
            good_matches = []

            for m, n in raw_matches:
                if m.distance < self.config.ratio_threshold * n.distance:
                    good_matches.append(m)

        return good_matches

    @staticmethod
    def draw_matches(img1, kp1, img2, kp2, matches) -> np.ndarray:
        """
        Draws lines between matching feature points between 2 images.
        :param img1: First image
        :param kp1: Feature points of the first image
        :param img2: Second image
        :param kp2: Feature points of the second image
        :param matches: Matching features
        :return: Image stitch with matches
        """

        result_image = cv2.drawMatches(
            img1, kp1, img2, kp2, matches, None,
            matchColor=(0, 255, 0),
            singlePointColor=None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        return result_image

    @staticmethod
    def show_image(title: str, image: np.ndarray):
        """
        Displays image on screen.
        :param title: Title of image
        :param image: Image to display
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(15, 10))
        plt.title(title)
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()

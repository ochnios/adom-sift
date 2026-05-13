import cv2
import matplotlib.pyplot as plt
import numpy as np


class SiftMatcher:

    def __init__(self, ratio_threshold: float = 0.75):
        self.sift = cv2.SIFT_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_L2)
        self.ratio_threshold = ratio_threshold

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
            color=(0, 0, 255),  # Yellow circles for visibility
            flags=flag
        )
        return result_image

    def find_matches(self, descriptors1: np.ndarray, descriptors2: np.ndarray) -> list:
        """
        Znajduje najlepsze dopasowania używając algorytmu k-Nearest Neighbors (k=2)
        oraz filtruje je za pomocą Lowe's Ratio Test.
        """
        # Znajdujemy 2 najbliższe dopasowania dla każdego deskryptora
        raw_matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)

        good_matches = []
        for m, n in raw_matches:
            # Lowe's Ratio Test: upewniamy się, że najlepsze dopasowanie (m)
            # jest znacznie lepsze niż drugie w kolejności (n).
            if m.distance < self.ratio_threshold * n.distance:
                good_matches.append(m)

        return good_matches

    def draw_matches(self, img1, kp1, img2, kp2, matches) -> np.ndarray:
        """Rysuje linie łączące dopasowane punkty na obu obrazach."""
        # Rysujemy tylko poprawne dopasowania (pomijamy pojedyncze punkty bez pary)
        result_image = cv2.drawMatches(
            img1, kp1, img2, kp2, matches, None,
            matchColor=(0, 255, 0),  # Zielone linie dla matchy
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

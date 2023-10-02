import os
import random

import cv2
import numpy as np

from augraphy.base.augmentation import Augmentation


class Gamma(Augmentation):
    """Adjusts the gamma of the whole image by a chosen multiplier.

    :param gamma_range: Pair of ints determining the range from which to sample the
           gamma shift.
    :type gamma_range: tuple, optional
    :param p: The probability that this Augmentation will be applied.
    :type p: float, optional
    """

    def __init__(
        self,
        gamma_range=(0.5, 1.5),
        p=1,
    ):
        """Constructor method"""
        super().__init__(p=p)
        self.gamma_range = gamma_range

    def __repr__(self):
        return f"Gamma(gamma_range={self.gamma_range}, p={self.p})"

    def __call__(self, image, layer=None, mask=None, keypoints=None, bounding_boxes=None, force=False):
        if force or self.should_run():
            image = image.copy()
            image = image.astype(np.uint8)
            value = random.uniform(self.gamma_range[0], self.gamma_range[1])
            invGamma = 1.0 / value
            table = np.array(
                [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)],
            ).astype("uint8")
            frame = cv2.LUT(image, table)

            # check for additional output of mask, keypoints and bounding boxes
            outputs_extra = []
            if mask is not None or keypoints is not None or bounding_boxes is not None:
                outputs_extra = [mask, keypoints, bounding_boxes]

            # returns additional mask, keypoints and bounding boxes if there is additional input
            if outputs_extra:
                # returns in the format of [image, mask, keypoints, bounding_boxes]
                return [frame] + outputs_extra
            else:
                return frame

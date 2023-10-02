import cv2
import numpy as np

from augraphy.base.augmentation import Augmentation


class ColorPaper(Augmentation):
    """Change color of input paper based on user input hue and saturation.

    :param hue_range: Pair of ints determining the range from which
           hue value is sampled.
    :type hue_range: tuple, optional
    :param saturation_range: Pair of ints determining the range from which
           saturation value is sampled.
    :param p: The probability that this Augmentation will be applied.
    :type p: float, optional
    """

    def __init__(
        self,
        hue_range=(28, 45),
        saturation_range=(10, 40),
        p=1,
    ):
        super().__init__(p=p)
        self.hue_range = hue_range
        self.saturation_range = saturation_range

    # Constructs a string representation of this Augmentation.
    def __repr__(self):
        return f"ColorPaper(hue_range={self.hue_range}, saturation_range={self.saturation_range}, p={self.p})"

    def add_color(self, image):
        """Add color background into input image.

        :param image: The image to apply the function.
        :type image: numpy.array (numpy.uint8)
        """

        has_alpha = 0
        if len(image.shape) > 2:
            is_gray = 0
            if image.shape[2] == 4:
                has_alpha = 1
                image, image_alpha = image[:, :, :3], image[:, :, 3]
        else:
            is_gray = 1
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        ysize, xsize = image.shape[:2]

        # convert to hsv colorspace
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # assign hue and saturation
        image_h = np.random.randint(self.hue_range[0], self.hue_range[1], size=(ysize, xsize))
        image_s = np.random.randint(self.saturation_range[0], self.saturation_range[1], size=(ysize, xsize))

        # assign hue and saturation channel back to hsv image
        image_hsv[:, :, 0] = image_h
        image_hsv[:, :, 1] = image_s

        # convert back to bgr
        image_color = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

        # return image follows the input image color channel
        if is_gray:
            image_color = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
        if has_alpha:
            image_color = np.dstack((image_color, image_alpha))

        return image_color

    # Applies the Augmentation to input data.
    def __call__(self, image, layer=None, mask=None, keypoints=None, bounding_boxes=None, force=False):
        if force or self.should_run():
            image = image.copy()

            color_image = self.add_color(image)

            # check for additional output of mask, keypoints and bounding boxes
            outputs_extra = []
            if mask is not None or keypoints is not None or bounding_boxes is not None:
                outputs_extra = [mask, keypoints, bounding_boxes]

            # returns additional mask, keypoints and bounding boxes if there is additional input
            if outputs_extra:
                # returns in the format of [image, mask, keypoints, bounding_boxes]
                return [color_image] + outputs_extra
            else:
                return color_image

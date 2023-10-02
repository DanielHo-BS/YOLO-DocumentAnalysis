import random

import cv2
import numpy as np
from numba import config
from numba import jit
from PIL import Image

from augraphy.base.augmentation import Augmentation


class DotMatrix(Augmentation):
    """Creates dot matrix effect by drawing dots of mean color in the detected contours.

    :param dot_matrix_shape: The shape of single dot in dot matrix effect.
            The existing shapes are "cicle", "rectangle", "triangle" and "diamond".
            Use "random" to select shape randomly.
    :type dot_matrix_shape: string, optional
    :param dot_matrix_dot_width_range: Tuple of ints determining the width of single dot in dot matrix effect.
    :type dot_matrix_dot_width_range: tuple, optional
    :param dot_matrix_dot_height_range: Tuple of ints determining the height of single dot in dot matrix effect.
    :type dot_matrix_dot_height_range: tuple, optional
    :param dot_matrix_min_width_range: Pair of ints/floats determining the minimum width of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the minimum width will be scaled by image width:
            min width (int) = image width  * min width (float and 0.0 - 1.0)
    :type dot_matrix_min_width_range: tuple, optional
    :param dot_matrix_max_width_range: Pair of ints/floats determining the maximum width of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the maximum width will be scaled by image width:
            max width (int) = image width  * max width (float and 0.0 - 1.0)
    :type dot_matrix_max_width_range: tuple, optional
    :param dot_matrix_min_height_range: Pair of ints/floats determining the minimum height of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the minimum height will be scaled by image height:
            min height (int) = image height  * min height (float and 0.0 - 1.0)
    :type dot_matrix_min_height_range: tuple, optional
    :param dot_matrix_max_height_range: Pair of ints/floats determining the maximum height of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the maximum height will be scaled by image height:
            max height (int) = image height  * max height (float and 0.0 - 1.0)
    :type dot_matrix_max_height_range: tuple, optional
    :param dot_matrix_min_area_range: Pair of ints/floats determining the minimum area of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the minimum area will be scaled by image area:
            min area (int) = image area  * min area (float and 0.0 - 1.0)
    :type dot_matrix_min_area_range: tuple, optional
    :param dot_matrix_max_area_range: Pair of ints/floats determining the maximum area of the contour to apply the effect.
            If the value is within the range of 0.0 to 1.0 and the value is float,
            the maximum area will be scaled by image area:
            max area (int) = image area  * max area (float and 0.0 - 1.0)
    :type dot_matrix_max_area_range: tuple, optional
    :param dot_matrix_gaussian_kernel_value_range: Tuple of ints determining the Gaussian kernel value in blurring the dot matrix image.
    :type dot_matrix_gaussian_kernel_value_range: tuple, optional
    :param dot_matrix_rotate_value_range: Tuple of ints determining the angle of rotation of the dot matrix effect.
    :type dot_matrix_rotate_value_range: tuple, optional
    :param numba_jit: The flag to enable numba jit to speed up the processing in the augmentation.
    :type numba_jit: int, optional
    :param p: The probability that this Augmentation will be applied.
    :type p: float, optional
    """

    def __init__(
        self,
        dot_matrix_shape="random",
        dot_matrix_dot_width_range=(3, 19),
        dot_matrix_dot_height_range=(3, 19),
        dot_matrix_min_width_range=(1, 2),
        dot_matrix_max_width_range=(150, 200),
        dot_matrix_min_height_range=(1, 2),
        dot_matrix_max_height_range=(150, 200),
        dot_matrix_min_area_range=(10, 20),
        dot_matrix_max_area_range=(2000, 5000),
        dot_matrix_median_kernel_value_range=(128, 255),
        dot_matrix_gaussian_kernel_value_range=(1, 3),
        dot_matrix_rotate_value_range=(0, 360),
        numba_jit=1,
        p=1,
    ):
        """Constructor method"""
        super().__init__(p=p)
        self.dot_matrix_shape = dot_matrix_shape
        self.dot_matrix_dot_width_range = dot_matrix_dot_width_range
        self.dot_matrix_dot_height_range = dot_matrix_dot_height_range
        self.dot_matrix_min_width_range = dot_matrix_min_width_range
        self.dot_matrix_max_width_range = dot_matrix_max_width_range
        self.dot_matrix_min_height_range = dot_matrix_min_height_range
        self.dot_matrix_max_height_range = dot_matrix_max_width_range
        self.dot_matrix_min_area_range = dot_matrix_min_area_range
        self.dot_matrix_max_area_range = dot_matrix_max_area_range
        self.dot_matrix_median_kernel_value_range = dot_matrix_median_kernel_value_range
        self.dot_matrix_gaussian_kernel_value_range = dot_matrix_gaussian_kernel_value_range
        self.dot_matrix_rotate_value_range = dot_matrix_rotate_value_range
        self.numba_jit = numba_jit
        config.DISABLE_JIT = bool(1 - numba_jit)

    def __repr__(self):
        return f"DotMatrix(dot_matrix_shape={self.dot_matrix_shape}, dot_matrix_dot_width_range={self.dot_matrix_dot_width_range}, dot_matrix_dot_height_range={self.dot_matrix_dot_height_range}, dot_matrix_min_width_range={self.dot_matrix_min_width_range}, dot_matrix_max_width_range={self.dot_matrix_max_width_range}, dot_matrix_min_height_range={self.dot_matrix_min_height_range}, dot_matrix_max_height_range={self.dot_matrix_max_height_range},  dot_matrix_min_area_range={self.dot_matrix_min_area_range}, dot_matrix_max_area_range={self.dot_matrix_max_area_range}, dot_matrix_median_kernel_value_range={self.dot_matrix_median_kernel_value_range}, dot_matrix_gaussian_kernel_value_range={self.dot_matrix_gaussian_kernel_value_range}, dot_matrix_rotate_value_range={self.dot_matrix_rotate_value_range}, numba_jit={self.numba_jit}, p={self.p})"

    @staticmethod
    @jit(nopython=True, cache=True)
    def fill_dot(
        image,
        image_dot_matrix,
        image_dot,
        image_mask,
        dot_matrix_dot_width,
        dot_matrix_dot_height,
        n_dot_x,
        n_dot_y,
        remainder_x,
        remainder_y,
    ):
        """The core function to fill output image with each dot image.

        :param image: The input image.
        :type image: numpy array
        :param image_dot_matrix: The output image.
        :type image_dot_matrix: numpy array
        :param image_dot: The image where it contains single dot of various shape.
        :type image_dot: numpy array
        :param image_mask: The mask to indicate the location to apply image dot into the output image.
        :type image_mask: numpy array
        :param dot_matrix_dot_width: Width of single dot.
        :type dot_matrix_dot_width: int
        :param dot_matrix_dot_height: Height of single dot.
        :type dot_matrix_dot_height: int
        :param n_dot_x: The number of dots in horizontal direction.
        :type n_dot_x: int
        :param n_dot_y: The number of dots in vertical direction.
        :type n_dot_y: int
        :param remainder_x: The remaining horizontal pixels after all dots are applied.
        :type remainder_x: int
        :param remainder_y: The remaining vertical pixels after all dots are applied.
        :type remainder_y: int
        """

        # fill in image_dot
        for y in range(n_dot_y):
            cy = y * dot_matrix_dot_height
            for x in range(n_dot_x):
                cx = x * dot_matrix_dot_width
                # non empty contour area
                if np.sum(image_mask[cy : cy + dot_matrix_dot_height, cx : cx + dot_matrix_dot_width]) > 0:
                    # mean of current dot color
                    image_patch = image[cy : cy + dot_matrix_dot_height, cx : cx + dot_matrix_dot_width]
                    dot_color = np.array(
                        [np.mean(image_patch[:, :, 0]), np.mean(image_patch[:, :, 1]), np.mean(image_patch[:, :, 2])],
                    )

                    # indices of shape mapping
                    indices = np.logical_or(
                        np.logical_or(image_dot[:, :, 0], image_dot[:, :, 1]),
                        image_dot[:, :, 2],
                    )

                    # map dot to image
                    for i in range(3):
                        dot_color_patch = ((image_dot / 255.0) * dot_color[i])[:, :, i]
                        dot_matrix_patch = image_dot_matrix[
                            cy : cy + dot_matrix_dot_height,
                            cx : cx + dot_matrix_dot_width,
                            i,
                        ]
                        for y in range(dot_color_patch.shape[0]):
                            for x in range(dot_color_patch.shape[1]):
                                if indices[y, x]:
                                    dot_matrix_patch[y, x] = np.uint8(dot_color_patch[y, x])

        # remaining last column
        if remainder_y > 0:
            for x in range(n_dot_x):
                cx = x * dot_matrix_dot_width
                start_y = n_dot_y * dot_matrix_dot_height
                # non empty contour area
                if np.sum(image_mask[start_y : start_y + remainder_y, cx : cx + dot_matrix_dot_width]) > 0:
                    # mean of current dot color
                    image_patch = image[start_y : start_y + remainder_y, cx : cx + dot_matrix_dot_width]
                    dot_color = np.array(
                        [np.mean(image_patch[:, :, 0]), np.mean(image_patch[:, :, 1]), np.mean(image_patch[:, :, 2])],
                    )

                    # indices of shape mapping
                    indices = np.logical_or(
                        np.logical_or(image_dot[:remainder_y, :, 0], image_dot[:remainder_y, :, 1]),
                        image_dot[:remainder_y, :, 2],
                    )

                    # map dot to image
                    for i in range(3):
                        dot_color_patch = ((image_dot[:remainder_y, :] / 255.0) * dot_color[i])[:, :, i]
                        dot_matrix_patch = image_dot_matrix[
                            start_y : start_y + remainder_y,
                            cx : cx + dot_matrix_dot_width,
                            i,
                        ]
                        for y in range(dot_color_patch.shape[0]):
                            for x in range(dot_color_patch.shape[1]):
                                if indices[y, x]:
                                    dot_matrix_patch[y, x] = np.uint8(dot_color_patch[y, x])

        # remaining last row
        if remainder_x > 0:
            for y in range(n_dot_y):
                cy = y * dot_matrix_dot_height
                start_x = n_dot_x * dot_matrix_dot_width
                # non empty contour area
                if np.sum(image_mask[cy : cy + dot_matrix_dot_height, start_x : start_x + remainder_x]) > 0:
                    # mean of current dot color
                    image_patch = image[cy : cy + dot_matrix_dot_height, start_x : start_x + remainder_x]
                    dot_color = np.array(
                        [np.mean(image_patch[:, :, 0]), np.mean(image_patch[:, :, 1]), np.mean(image_patch[:, :, 2])],
                    )

                    # indices of shape mapping
                    indices = np.logical_or(
                        np.logical_or(image_dot[:, :remainder_x, 0], image_dot[:, :remainder_x, 1]),
                        image_dot[:, :remainder_x, 2],
                    )

                    # map dot to image
                    for i in range(3):
                        dot_color_patch = ((image_dot[:, :remainder_x] / 255.0) * dot_color[i])[:, :, i]
                        dot_matrix_patch = image_dot_matrix[
                            cy : cy + dot_matrix_dot_height,
                            start_x : start_x + remainder_x,
                            i,
                        ]
                        for y in range(dot_color_patch.shape[0]):
                            for x in range(dot_color_patch.shape[1]):
                                if indices[y, x]:
                                    dot_matrix_patch[y, x] = np.uint8(dot_color_patch[y, x])

        # last dot (bottom right)
        if remainder_x and remainder_y > 0:

            if remainder_x > 0:
                length_x = remainder_x
            else:
                length_x = dot_matrix_dot_width
            if remainder_y > 0:
                length_y = remainder_y
            else:
                length_y = dot_matrix_dot_height

            start_x = n_dot_x * dot_matrix_dot_width
            start_y = n_dot_y * dot_matrix_dot_height
            # non empty contour area
            if np.sum(image_mask[start_y : start_y + length_y, start_x : start_x + length_x]) > 0:
                # mean of current dot color
                image_patch = image[start_y : start_y + length_y, start_x : start_x + length_x]
                dot_color = np.array(
                    [np.mean(image_patch[:, :, 0]), np.mean(image_patch[:, :, 1]), np.mean(image_patch[:, :, 2])],
                )

                # indices of shape mapping
                indices = np.logical_or(
                    np.logical_or(image_dot[:length_y, :length_x, 0], image_dot[:length_y, :length_x, 1]),
                    image_dot[:length_y, :length_x, 2],
                )

                # map dot to image
                for i in range(3):
                    dot_color_patch = ((image_dot[:length_y, :length_x] / 255.0) * dot_color[i])[:, :, i]
                    dot_matrix_patch = image_dot_matrix[
                        start_y : start_y + length_y,
                        start_x : start_x + length_x,
                        i,
                    ]
                    for y in range(dot_color_patch.shape[0]):
                        for x in range(dot_color_patch.shape[1]):
                            if indices[y, x]:
                                dot_matrix_patch[y, x] = np.uint8(dot_color_patch[y, x])

    def __call__(self, image, layer=None, mask=None, keypoints=None, bounding_boxes=None, force=False):
        if force or self.should_run():
            image = image.copy()

            ysize, xsize = image.shape[:2]

            # check and convert image into BGR format
            if len(image.shape) > 2:
                is_gray = 0
            else:
                is_gray = 1
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            # apply median filter
            median_kernel_value = random.randint(
                self.dot_matrix_median_kernel_value_range[0],
                self.dot_matrix_median_kernel_value_range[1],
            )
            # median kernel value must be odd
            if not median_kernel_value % 2:
                median_kernel_value += 1
            # the max kernel value is 255, if value > 255, scale down image
            if median_kernel_value > 255:
                scale = 255 / median_kernel_value
                image_resize = cv2.resize(image, (int(xsize * scale), int(ysize * scale)), 0)
                image_median = cv2.medianBlur(image_resize, 255)
            else:
                image_median = cv2.medianBlur(image, median_kernel_value)
            if median_kernel_value > 255:
                image_median = cv2.resize(image_median, (xsize, ysize), 0)

            # init binary image for edge detection purpose
            image_binary = np.zeros((ysize, xsize), dtype="int32")
            contours = []
            # get better contours by getting contours from all three channels
            for i in range(3):

                # get binary of current channel and sum to binary image
                _, image_binary_single_channel = cv2.threshold(
                    image[:, :, i],
                    0,
                    255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU,
                )

                # sum of binary to get binary images across all channels
                image_binary += image_binary_single_channel.astype("int32")

                # find contours of current channel
                contours_single, _ = cv2.findContours(
                    image_binary_single_channel,
                    cv2.RETR_LIST,
                    cv2.CHAIN_APPROX_SIMPLE,
                )

                # merge contours in each channel
                contours.extend(contours_single)

            # convert back to uint8
            image_binary[image_binary > 255] = 255
            image_binary = image_binary.astype("uint8")

            # find contours of merged binary
            contours_single, _ = cv2.findContours(
                image_binary,
                cv2.RETR_LIST,
                cv2.CHAIN_APPROX_SIMPLE,
            )
            # merge contours of binary image
            contours.extend(contours_single)

            # width
            if self.dot_matrix_min_width_range[0] <= 1.0 and isinstance(self.dot_matrix_min_width_range[0], float):
                min_width = random.randint(
                    int(self.dot_matrix_min_width_range[0] * xsize),
                    int(self.dot_matrix_min_width_range[1] * xsize),
                )
            else:
                min_width = random.randint(
                    self.dot_matrix_min_width_range[0],
                    self.dot_matrix_min_width_range[1],
                )
            if self.dot_matrix_max_width_range[0] <= 1.0 and isinstance(self.dot_matrix_max_width_range[0], float):
                max_width = random.randint(
                    int(self.dot_matrix_max_width_range[0] * xsize),
                    int(self.dot_matrix_max_width_range[1] * xsize),
                )
            else:
                max_width = random.randint(
                    self.dot_matrix_max_width_range[0],
                    self.dot_matrix_max_width_range[1],
                )

            # height
            if self.dot_matrix_min_height_range[0] <= 1.0 and isinstance(self.dot_matrix_min_height_range[0], float):
                min_height = random.randint(
                    int(self.dot_matrix_min_height_range[0] * ysize),
                    int(self.dot_matrix_min_height_range[1] * ysize),
                )
            else:
                min_height = random.randint(
                    self.dot_matrix_min_height_range[0],
                    self.dot_matrix_min_width_range[1],
                )
            if self.dot_matrix_max_height_range[0] <= 1.0 and isinstance(self.dot_matrix_max_height_range[0], float):
                max_height = random.randint(
                    int(self.dot_matrix_max_height_range[0] * ysize),
                    int(self.dot_matrix_max_height_range[1] * ysize),
                )
            else:
                max_height = random.randint(
                    self.dot_matrix_max_height_range[0],
                    self.dot_matrix_max_height_range[1],
                )

            # area
            if self.dot_matrix_min_area_range[0] <= 1.0 and isinstance(self.dot_matrix_min_area_range[0], float):
                min_area = random.randint(
                    int(self.dot_matrix_min_area_range[0]),
                    int(self.dot_matrix_min_area_range[1]),
                )
            else:
                min_area = random.randint(
                    self.dot_matrix_min_area_range[0],
                    self.dot_matrix_min_area_range[1],
                )
            if self.dot_matrix_max_area_range[0] <= 1.0 and isinstance(self.dot_matrix_max_area_range[0], float):
                max_area = random.randint(
                    int(self.dot_matrix_max_area_range[0]),
                    int(self.dot_matrix_max_area_range[1]),
                )
            else:
                max_area = random.randint(
                    self.dot_matrix_max_area_range[0],
                    self.dot_matrix_max_area_range[1],
                )

            # find contours of image
            image_mask = np.zeros_like(image_binary, dtype="uint8")
            # draw mask
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                if (
                    w < max_width
                    and w > min_width
                    and h < max_height
                    and h > min_height
                    and area < max_area
                    and area > min_area
                ):
                    cv2.drawContours(image_mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

            # generate shape
            if self.dot_matrix_shape == "random":
                dot_matrix_shape = random.choice(["circle", "rectangle", "triangle", "diamond"])
            else:
                dot_matrix_shape = self.dot_matrix_shape

            # generate each dot height and width
            dot_matrix_dot_width = random.randint(
                self.dot_matrix_dot_width_range[0],
                self.dot_matrix_dot_width_range[1],
            )
            dot_matrix_dot_height = random.randint(
                self.dot_matrix_dot_height_range[0],
                self.dot_matrix_dot_height_range[1],
            )

            # each dot width or height must be odd
            if not dot_matrix_dot_width % 2:
                dot_matrix_dot_width += 1
            if not dot_matrix_dot_height % 2:
                dot_matrix_dot_height += 1

            if dot_matrix_shape == "circle":
                # min size of dot is 3 pixels for circle
                dot_matrix_dot_width = max(3, dot_matrix_dot_width)
                dot_matrix_dot_height = max(3, dot_matrix_dot_height)
                # initialize dot image
                image_dot = np.zeros((dot_matrix_dot_height, dot_matrix_dot_width, 3), dtype="uint8")
                # draw shape
                center_x = int(np.floor(dot_matrix_dot_width / 2))
                center_y = int(np.floor(dot_matrix_dot_height / 2))
                radius = int(np.floor(min(dot_matrix_dot_width / 2, dot_matrix_dot_height / 2)))
                cv2.circle(image_dot, (center_x, center_y), radius, (255, 255, 255), -1)

            elif dot_matrix_shape == "rectangle":
                # min size of dot is 3 pixels for rectangle
                dot_matrix_dot_width = max(3, dot_matrix_dot_width)
                dot_matrix_dot_height = max(3, dot_matrix_dot_height)
                # initialize dot image
                image_dot = np.zeros((dot_matrix_dot_height, dot_matrix_dot_width, 3), dtype="uint8")
                # draw shape
                image_dot[1:-1, 1:-1] = 255

            elif dot_matrix_shape == "triangle":
                # min size of dot is 5 pixels for triangle
                dot_matrix_dot_width = max(5, dot_matrix_dot_width)
                dot_matrix_dot_height = max(5, dot_matrix_dot_height)
                # initialize dot image
                image_dot = np.zeros((dot_matrix_dot_height, dot_matrix_dot_width, 3), dtype="uint8")
                # draw shape (index starts from 1 to leave 1 space for black pixel)
                y0 = 0
                yn = dot_matrix_dot_height - 1
                x0 = 0
                xmid = int(np.floor(dot_matrix_dot_width / 2))
                xn = dot_matrix_dot_width - 1
                triangle_points = np.array([(x0, yn), (xmid, y0), (xn, yn)])
                cv2.drawContours(image_dot, [triangle_points], 0, (255, 255, 255), -1)
                # mirror left right for consistent shape
                image_dot[:, :xmid] = np.fliplr(image_dot[:, xmid + 1 :])

            elif dot_matrix_shape == "diamond":
                # min size of dot is 5 pixels for triangle
                dot_matrix_dot_width = max(5, dot_matrix_dot_width)
                dot_matrix_dot_height = max(5, dot_matrix_dot_height)
                # initialize dot image
                image_dot = np.zeros((dot_matrix_dot_height, dot_matrix_dot_width, 3), dtype="uint8")
                # draw shape
                y0 = 0
                ymid = int(np.floor(dot_matrix_dot_height / 2))
                yn = dot_matrix_dot_height - 1
                x0 = 0
                xmid = int(np.floor(dot_matrix_dot_width / 2))
                xn = dot_matrix_dot_width - 1
                triangle_points = np.array([(x0, ymid), (xmid, y0), (xn, ymid)])
                cv2.drawContours(image_dot, [triangle_points], 0, (255, 255, 255), -1)
                # mirror left right for consistent shape
                image_dot[:, :xmid] = np.fliplr(image_dot[:, xmid + 1 :])
                # mirror up down to create diamond shape
                image_dot[ymid:, :] = np.flipud(image_dot[: ymid + 1, :])

            # rotate dot image
            dot_matrix_rotate_value = random.randint(
                self.dot_matrix_rotate_value_range[0],
                self.dot_matrix_rotate_value_range[1],
            )
            if dot_matrix_rotate_value != 0:
                image_dot_PIL = Image.fromarray(image_dot)
                rotated_image_dot_PIL = image_dot_PIL.rotate(dot_matrix_rotate_value)
                image_dot = np.array(rotated_image_dot_PIL)

            # divided value from each dot width and height
            div_x = xsize / dot_matrix_dot_width
            div_y = ysize / dot_matrix_dot_height

            # number of divisible width and height
            n_dot_x = int(np.floor(div_x))
            n_dot_y = int(np.floor(div_y))

            # remainder of division by dot width and height
            remainder_x = xsize % dot_matrix_dot_width
            remainder_y = ysize % dot_matrix_dot_height

            # change contours area to median image
            image_dot_matrix = image.copy()

            for i in range(3):
                image_dot_matrix[:, :, i][image_mask > 0] = image_median[:, :, i][image_mask > 0]

            # fill output image with dots
            self.fill_dot(
                image,
                image_dot_matrix,
                image_dot.astype("float"),
                image_mask,
                dot_matrix_dot_width,
                dot_matrix_dot_height,
                n_dot_x,
                n_dot_y,
                remainder_x,
                remainder_y,
            )

            # apply Gaussian Blur on dot image
            dot_matrix_gaussian_kernel_value = random.randint(
                self.dot_matrix_gaussian_kernel_value_range[0],
                self.dot_matrix_gaussian_kernel_value_range[1],
            )
            # Gaussian kernel value must be odd
            if not dot_matrix_gaussian_kernel_value % 2:
                dot_matrix_gaussian_kernel_value += 1
            image_dot_matrix_blur = cv2.GaussianBlur(
                image_dot_matrix,
                (dot_matrix_gaussian_kernel_value, dot_matrix_gaussian_kernel_value),
                0,
            )

            # perform blur on detected contours only
            image_dot_matrix[image_mask > 0] = image_dot_matrix_blur[image_mask > 0]

            # return image follows the input image color channel
            if is_gray:
                image_dot_matrix = cv2.cvtColor(image_dot_matrix, cv2.COLOR_BGR2GRAY)

            # check for additional output of mask, keypoints and bounding boxes
            outputs_extra = []
            if mask is not None or keypoints is not None or bounding_boxes is not None:
                outputs_extra = [mask, keypoints, bounding_boxes]

            # returns additional mask, keypoints and bounding boxes if there is additional input
            if outputs_extra:
                # returns in the format of [image, mask, keypoints, bounding_boxes]
                return [image_dot_matrix] + outputs_extra
            else:
                return image_dot_matrix

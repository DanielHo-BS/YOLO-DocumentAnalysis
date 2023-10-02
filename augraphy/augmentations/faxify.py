import random

import cv2
import numpy as np
from numba import config
from numba import jit

from augraphy.augmentations.lib import binary_threshold
from augraphy.base.augmentation import Augmentation


class Faxify(Augmentation):
    """Emulates faxify effect in the image.

    :param scale_range: Pair of floats determining the range from which to
           divide the resolution by.
    :type scale_range: tuple, optional
    :param monochrome: Flag to enable monochrome effect.
    :type monochrome: int, optional
    :param monochrome_method: Monochrome thresholding method.
    :type monochrome_method: string, optional
    :param monochrome_arguments: A dictionary contains argument to monochrome
            thresholding method.
    :type monochrome_arguments: dict, optional
    :param halftone: Flag to enable halftone effect.
    :type halftone: int, optional
    :param invert: Flag to invert grayscale value in halftone effect.
    :type invert: int, optional
    :param half_kernel_size: Pair of ints to determine half size of gaussian kernel for halftone effect.
    :type half_kernel_size: tuple, optional
    :param angle: Pair of ints to determine angle of halftone effect.
    :type angle: tuple, optional
    :param sigma: Pair of ints to determine sigma value of gaussian kernel in halftone effect.
    :type sigma: tuple, optional
    :param numba_jit: The flag to enable numba jit to speed up the processing in the augmentation.
    :type numba_jit: int, optional
    :param p: The probability that this Augmentation will be applied.
    :type p: float, optional
    """

    def __init__(
        self,
        scale_range=(1.0, 1.25),
        monochrome=-1,
        monochrome_method="random",
        monochrome_arguments={},
        halftone=-1,
        invert=1,
        half_kernel_size=(1, 1),
        angle=(0, 360),
        sigma=(1, 3),
        numba_jit=1,
        p=1,
    ):

        """Constructor method"""
        super().__init__(p=p, numba_jit=numba_jit)
        self.scale_range = scale_range
        self.monochrome = monochrome
        self.monochrome_method = monochrome_method
        self.monochrome_arguments = monochrome_arguments
        self.halftone = halftone
        self.invert = invert
        self.half_kernel_size = half_kernel_size
        self.angle = angle
        self.sigma = sigma
        self.numba_jit = numba_jit
        config.DISABLE_JIT = bool(1 - numba_jit)

    # Constructs a string representation of this Augmentation.
    def __repr__(self):
        return f"Faxify(scale_range={self.scale_range}, monochrome={self.monochrome}, monochrome_method={self.monochrome_method}, monochrome_arguments={self.monochrome_arguments}, halftone={self.halftone}, invert={self.invert}, half_kernel_size={self.half_kernel_size}, angle={self.angle}, sigma={self.sigma}, numba_jit={self.numba_jit}, p={self.p})"

    def cv_rotate(self, image, angle):
        """Rotate image based on the input angle.

        :param image: The image to apply the function.
        :type image: numpy.array (numpy.uint8)
        :param angle: The angle of the rotation.
        :type angle: int
        """
        # image shape
        ysize, xsize = image.shape[:2]
        # center of rotation
        cx, cy = xsize // 2, ysize // 2
        # rotation matrix
        M = cv2.getRotationMatrix2D((cx, cy), angle, 1)

        # rotation calculates the cos and sin, taking absolutes of those
        abs_cos = abs(M[0, 0])
        abs_sin = abs(M[0, 1])

        # find the new x and y bounds
        bound_x = int(ysize * abs_sin + xsize * abs_cos)
        bound_y = int(ysize * abs_cos + xsize * abs_sin)

        # subtract old image center (bringing image back to origin) and adding the new image center coordinates
        M[0, 2] += bound_x / 2 - cx
        M[1, 2] += bound_y / 2 - cy

        # warp and rotate the image
        image_rotated = cv2.warpAffine(image, M, (bound_x, bound_y))

        return image_rotated

    @staticmethod
    @jit(nopython=True, cache=True)
    def apply_halftone(image_halftone, gaussian_kernel, rotated, ysize, xsize, kernel_size):
        """Run loops and apply halftone effect in the input image.

        :param image_halftone: The image with halftone effect.
        :type image_halftone: numpy.array (numpy.uint8)
        :param gaussian_kernel: Gaussian kernel to generate the halftone effect.
        :type gaussian_kernel: numpy.array (numpy.uint8)
        :param rotated: The rotated input image
        :type rotated: numpy.array (numpy.uint8)
        :param ysize: Row numbers of the input image.
        :type ysize: int
        :param xsize: Column numbers of the input image.
        :type xsize: int
        :param kernel_size: Kernel size to generate the halftone effect.
        :type kernel_size: int
        """

        for y in range(0, ysize - kernel_size + 1, kernel_size):
            for x in range(0, xsize - kernel_size + 1, kernel_size):
                image_halftone[y : y + kernel_size, x : x + kernel_size] = (
                    np.mean(rotated[y : y + kernel_size, x : x + kernel_size]) * gaussian_kernel
                )

    # generate halftone effect
    def generate_halftone(self, image, half_kernel_size=2, angle=45, sigma=2):
        """Generate halftone effect in the input image.

        :param image: The image to apply the function.
        :type image: numpy.array (numpy.uint8)
        :param half_kernel_size: Half value of kernel size to generate halftone effect.
        :type half_kernel_size: int
        :param angle: The angle of the halftone effect.
        :type angle: int
        :param sigma: Sigma value of gaussian kernel for halftone effect.
        :type sigma: int
        """
        # get total width of the kernel
        kernel_size = kernel_size_x = kernel_size_y = 2 * half_kernel_size + 1

        # rotate image based on the angle
        rotated = self.cv_rotate(image, angle)

        # get new rotated image size
        ysize, xsize = rotated.shape[:2]

        # generate gaussian kernel
        image_kernel = np.zeros((kernel_size_x, kernel_size_x))
        image_kernel[half_kernel_size, half_kernel_size] = 1
        gaussian_kernel = cv2.GaussianBlur(
            image_kernel,
            (kernel_size_x, kernel_size_y),
            sigmaX=sigma,
            sigmaY=sigma,
        )
        gaussian_kernel *= 1 / np.max(gaussian_kernel)

        # initialize empty image
        image_halftone = np.zeros((ysize, xsize))

        # apply halftone effect to image
        self.apply_halftone(image_halftone, gaussian_kernel, rotated, ysize, xsize, kernel_size)

        # rotate back using negative angle
        image_halftone = self.cv_rotate(image_halftone, -angle)

        # crop the center section of image
        ysize_out, xsize_out = image_halftone.shape[:2]
        ysize_in, xsize_in = image.shape[:2]
        y_start = int((ysize_out - ysize_in) / 2)
        y_end = y_start + ysize_in
        x_start = int((xsize_out - xsize_in) / 2)
        x_end = x_start + xsize_in
        image_halftone = image_halftone[y_start:y_end, x_start:x_end]

        return image_halftone

    def complement_rgb_to_gray(self, img, invert=1, gray_level=255, max_value=255):
        """Convert RGB/BGR image to single channel grayscale image.

        :param img: The image to apply the function.
        :type img: numpy.array (numpy.uint8)
        :param invert: Flag to invert the generated grayscale value.
        :type invert: int
        :param gray_level: The selected gray value.
        :type gray_level: int
        :param max_value: Maximum value of gray value.
        :type max_value: int
        """

        img_complement = max_value - img

        if len(img.shape) > 2:
            img_gray = np.min(img_complement, axis=2) * (gray_level / max_value)
            img_gray[np.where(np.sum(img, axis=2) == 0)] = max_value  # if there is no color, set it to max value
        else:
            img_gray = img_complement * (gray_level / max_value)
            img_gray[np.where(img == 0)] = max_value  # if there is no color, set it to max value

        if invert:
            return (img_gray / 255).astype("float")
        else:
            return (1 - (img_gray / 255)).astype("float")

    def downscale(self, image):
        """Downscale image based on the user input scale value.

        :param image: The image to apply the function.
        :type image: numpy.array (numpy.uint8)
        """

        ysize, xsize = image.shape[:2]
        scale = np.random.uniform(self.scale_range[0], self.scale_range[1])
        new_size = (int(xsize // scale), int(ysize // scale))
        image_downscaled = cv2.resize(image, new_size)

        return image_downscaled

    # Applies the Augmentation to input data.
    def __call__(self, image, layer=None, mask=None, keypoints=None, bounding_boxes=None, force=False):
        if force or self.should_run():
            image = image.copy()

            # check and convert image into BGR format
            has_alpha = 0
            if len(image.shape) > 2:
                is_gray = 0
                if image.shape[2] == 4:
                    has_alpha = 1
                    image, image_alpha = image[:, :, :3], image[:, :, 3]
            else:
                is_gray = 1
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            if self.monochrome == -1:
                monochrome = random.choice([0, 1])
            else:
                monochrome = self.monochrome

            if self.halftone == -1:
                halftone = random.choice([0, 1])
            else:
                halftone = self.halftone

            # downscale image
            image_out = self.downscale(image)

            if monochrome:
                # randomly select threshold method
                if self.monochrome_method == "random":
                    all_monochrome_method = [
                        # "grayscale",
                        "threshold_li",
                        "threshold_mean",
                        "threshold_otsu",
                        "threshold_sauvola",
                        "threshold_triangle",
                        # "threshold_yen",
                        # "cv2.threshold",
                        # "threshold_minimum",
                        # "cv2.adaptiveThreshold",
                        # "threshold_local",
                        # "threshold_niblack",
                    ]
                    monochrome_method = random.choice(all_monochrome_method)
                else:
                    monochrome_method = self.monochrome_method

                monochrome_arguments = self.monochrome_arguments.copy()

                # block size must present in the input argument
                if monochrome_method == "threshold_local" and "block_size" not in monochrome_arguments:
                    # min image size is 30
                    block_size = random.randint(3, 29)
                    # block size must be odd
                    if not block_size % 2:
                        block_size += 1
                    monochrome_arguments["block_size"] = block_size

                # window size of niblack and sauvola must be odd
                if (monochrome_method == "threshold_niblack") or (monochrome_method == "threshold_sauvola"):
                    if monochrome_arguments and "window_size" in monochrome_arguments:
                        if not monochrome_arguments["window_size"] % 2:
                            monochrome_arguments["window_size"] += 1

                # cv2 threshold needs to have input arguments
                if monochrome_method == "cv2.threshold":
                    if monochrome_arguments is None:
                        monochrome_arguments = {}
                    if "thresh" not in monochrome_arguments:
                        monochrome_arguments["thresh"] = random.randint(64, 128)
                    if "maxval" not in monochrome_arguments:
                        monochrome_arguments["maxval"] = 255
                    if "type" not in self.monochrome_arguments:
                        monochrome_arguments["type"] = cv2.THRESH_BINARY

                # cv2 adaptiveThreshold needs to have input arguments
                if monochrome_method == "cv2.adaptiveThreshold":
                    if monochrome_arguments is None:
                        monochrome_arguments = {}
                    if "maxValue" not in monochrome_arguments:
                        monochrome_arguments["maxValue"] = 255
                    if "adaptiveMethod" not in monochrome_arguments:
                        monochrome_arguments["adaptiveMethod"] = random.choice(
                            (
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.ADAPTIVE_THRESH_MEAN_C,
                            ),
                        )
                    if "thresholdType" not in monochrome_arguments:
                        monochrome_arguments["thresholdType"] = cv2.THRESH_BINARY
                    if "blockSize" not in monochrome_arguments:
                        block_size = random.randint(5, 29)
                        if not block_size % 2:
                            block_size += 1
                        monochrome_arguments["blockSize"] = block_size
                    if "C" not in monochrome_arguments:
                        monochrome_arguments["C"] = random.randint(1, 3)

                # run binarization
                image_out = binary_threshold(
                    image_out,
                    monochrome_method,
                    monochrome_arguments,
                )

            # check and apply halftone
            if halftone:

                # convert to gray
                image_out = self.complement_rgb_to_gray(image_out, invert=self.invert)

                half_kernel_size = random.randint(
                    self.half_kernel_size[0],
                    self.half_kernel_size[1],
                )
                angle = random.randint(self.angle[0], self.angle[1])
                sigma = random.randint(self.sigma[0], self.sigma[1])

                image_out = self.generate_halftone(
                    image_out,
                    half_kernel_size,
                    angle,
                    sigma,
                )

                # check and invert image, then return image as uint8
                if self.invert:
                    image_out = ((1 - image_out) * 255).astype("uint8")
                else:
                    image_out = (image_out * 255).astype("uint8")

            # upscale image
            image_faxify = cv2.resize(image_out, (image.shape[1], image.shape[0]))

            if is_gray and len(image_faxify.shape) > 2:
                image_faxify = cv2.cvtColor(image_faxify, cv2.COLOR_BGR2GRAY)
            if has_alpha:
                # convert to BGRA if input has alpha layer
                if len(image_faxify.shape) < 3:
                    image_faxify = cv2.cvtColor(image_faxify, cv2.COLOR_GRAY2BGR)
                image_faxify = np.dstack((image_faxify, image_alpha))

            # check for additional output of mask, keypoints and bounding boxes
            outputs_extra = []
            if mask is not None or keypoints is not None or bounding_boxes is not None:
                outputs_extra = [mask, keypoints, bounding_boxes]

            # returns additional mask, keypoints and bounding boxes if there is additional input
            if outputs_extra:
                # returns in the format of [image, mask, keypoints, bounding_boxes]
                return [image_faxify] + outputs_extra
            else:
                return image_faxify

import os
import random
import time
from copy import copy
from copy import deepcopy
from glob import glob

import cv2
import numpy as np

from augraphy.base.augmentation import Augmentation
from augraphy.base.augmentationresult import AugmentationResult
from augraphy.base.augmentationsequence import AugmentationSequence
from augraphy.utilities.detectdpi import dpi_resize
from augraphy.utilities.detectdpi import DPIMetrics
from augraphy.utilities.overlaybuilder import OverlayBuilder


class AugraphyPipeline:
    """Contains phases of image augmentations and their results.

    :param pre_phase: Collection of Augmentations to apply
    :param ink_phase: Collection of Augmentations to apply.
    :type ink_phase: base.augmentationsequence or list
    :param paper_phase: Collection of Augmentations to apply.
    :type paper_phase: base.augmentationsequence or list
    :param post_phase: Collection of Augmentations to apply.
    :type post_phase: base.augmentationsequence or list
    :param overlay_type: Blending method to print ink into paper.
    :type overlay_type: string, optional.
    :param overlay_alpha: The alpha value for certain overlay methods.
    :type overlay_alpha: float, optional.
    :param ink_color_range: Pair of ints determining the range from which to
           sample the ink color.
    :type ink_color_range: tuple, optional
    :param paper_color_range: Pair of ints determining the range from which to
           sample the paper color.
    :type paper_color_range: tuple, optional
    :param mask: The mask of labels for each pixel. Mask value should be in range of 1 to 255.
            Value of 0 will be assigned to the filled area after the transformation.
    :type mask: numpy array (uint8), optional
    :param keypoints: A dictionary of single or multiple labels where each label is a nested list of points coordinate.
            For example: keypoints = {"label1":[[xpoint1, ypoint1], [xpoint2, ypoint2]], "label2":[[xpoint3, ypoint3]]}.
    :type keypoints: dictionary, optional
    :param bounding_boxes: A nested list where each nested list contains box location (x1, y1, x2, y2).
            For example: bounding_boxes = [[xa1,ya1,xa2,ya2], [xb1,yb2,xb2,yb2]]
    :type bounding_boxes: list, optional
    :param save_outputs: Flag to enable saving each phase output image.
    :type save_outputs: bool, optional
    :param fixed_dpi: Flag to enable a same DPI in both input and augmented image.
    :type fixed_dpi: bool, optional
    :param log: Flag to enable logging.
    :type log: bool, optional
    :param random_seed: The initial value for PRNGs used in Augraphy.
    :type random_seed: int, optional
    """

    def __init__(
        self,
        ink_phase=[],
        paper_phase=[],
        post_phase=[],
        pre_phase=[],
        overlay_type="ink_to_paper",
        overlay_alpha=0.3,
        ink_color_range=(-1, -1),
        paper_color_range=(255, 255),
        mask=None,
        keypoints=None,
        bounding_boxes=None,
        save_outputs=False,
        fixed_dpi=False,
        log=False,
        random_seed=None,
    ):
        """Constructor method"""
        self.pre_phase = self.wrapListMaybe(pre_phase)
        self.ink_phase = self.wrapListMaybe(ink_phase)
        self.paper_phase = self.wrapListMaybe(paper_phase)
        self.post_phase = self.wrapListMaybe(post_phase)
        self.overlay_type = overlay_type
        self.overlay_alpha = overlay_alpha
        self.ink_color_range = ink_color_range
        self.paper_color_range = paper_color_range
        self.mask = mask
        self.keypoints = keypoints
        self.bounding_boxes = bounding_boxes
        self.save_outputs = save_outputs
        self.fixed_dpi = fixed_dpi
        self.log = log
        self.random_seed = random_seed

        # ensure determinism if random_seed set
        if self.random_seed:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)
            cv2.setRNGSeed(self.random_seed)

        # create directory to store log files
        if self.log:
            self.log_prob_path = os.path.join(os.getcwd(), "logs/")
            os.makedirs(self.log_prob_path, exist_ok=True)

        if self.save_outputs:
            # create each phase folder
            self.save_paths = []
            self.save_paths.append(os.path.join(os.getcwd(), "augmentation_images/pre/"))
            self.save_paths.append(os.path.join(os.getcwd(), "augmentation_images/ink/"))
            self.save_paths.append(os.path.join(os.getcwd(), "augmentation_images/paper/"))
            self.save_paths.append(os.path.join(os.getcwd(), "augmentation_images/post/"))
            for i in range(len(self.save_paths)):
                os.makedirs(self.save_paths[i], exist_ok=True)

    def wrapListMaybe(self, augs):
        """Converts a bare list to an AugmentationSequence, or does nothing."""
        if type(augs) is list:
            return AugmentationSequence(augs)
        else:
            return augs

    def augment(self, image, return_dict=1):
        """Applies the Augmentations in each phase of the pipeline.

        :param image: The image to apply Augmentations to. Minimum 30x30 pixels.
        :type image: numpy.array or list
        :return: 1. A dictionary of AugmentationResults representing the changes in each phase of the pipeline if the input is image.
                 2. A list contains output images if the input is list of images.
                 3. A four dimensional numpy array if the input is a four dimensional numpy array (batch size, channels, height, width).
        :rtype: 1. dictionary
                2. list
                3. numpy array (B, C, H, W)
        :param return_dict: Flag to return output in dictionary format.
                Not applicable when input is 4 dimensional array.
                When input is 4 dimensional numpy array, output will be a 4 dimensional array too.
        :type return_dict: int
        """

        # image is a list of images
        if isinstance(image, list):
            output = []
            for i, single_image in enumerate(image):
                # retrieve mask, keypoints, bounding boxes (if there's any)
                mask, keypoints, bounding_boxes = None, None, None
                if self.mask is not None:
                    mask = self.mask[i]
                if self.keypoints is not None:
                    keypoints = self.keypoints[i]
                if self.bounding_boxes is not None:
                    bounding_boxes = self.bounding_boxes[i]

                data = self.augment_single_image(
                    image=single_image,
                    mask=mask,
                    keypoints=keypoints,
                    bounding_boxes=bounding_boxes,
                )
                if return_dict:
                    output.append(data)
                else:
                    if (mask is not None) or (keypoints is not None) or (bounding_boxes is not None):
                        output.append([data["output"], data["mask"], data["keypoints"], data["bounding_boxes"]])
                    else:
                        output.append(data["output"])

        # image is a 4 dimensional numpy array
        elif len(image.shape) == 4:
            batch_size, channels, height, width = image.shape
            output = np.zeros((batch_size, channels, height, width), dtype=image.dtype)
            output_masks = []
            output_keypoints = []
            output_bounding_boxes = []
            for i in range(batch_size):
                # retrieve mask, keypoints, bounding boxes (if there's any)
                mask, keypoints, bounding_boxes = None, None, None
                if self.mask is not None:
                    mask = self.mask[i]
                if self.keypoints is not None:
                    keypoints = self.keypoints[i]
                if self.bounding_boxes is not None:
                    bounding_boxes = self.bounding_boxes[i]

                # perform augmentation
                single_image = image[i].reshape(height, width, channels)
                output_data = self.augment_single_image(
                    single_image,
                    mask=mask,
                    keypoints=keypoints,
                    bounding_boxes=bounding_boxes,
                )

                # retrieve image and each additional output format
                output_image = output_data["output"]
                output_masks.append(output_data["mask"])
                output_keypoints.append(output_data["keypoints"])
                output_bounding_boxes.append(output_data["bounding_boxes"])

                # output is color image but input is in grayscale, convert output to grayscale
                if len(output_image.shape) > channels:
                    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)
                # output is in grayscale but input is color image, convert output to color image
                if len(output_image.shape) != channels:
                    output_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)
                # rescale image size if the image size is changes after the augmentation
                if output_image.shape[0] != height or output_image.shape[1] != width:
                    output_image = cv2.resize(output_image, (width, height), interpolation=cv2.INTER_AREA)
                output[i] = output_image.reshape(channels, height, width)

                if (mask is not None) or (keypoints is not None) or (bounding_boxes is not None):
                    output = [output, output_masks, output_keypoints, output_bounding_boxes]

        # single image
        else:
            data = self.augment_single_image(
                image,
                mask=self.mask,
                keypoints=self.keypoints,
                bounding_boxes=self.bounding_boxes,
            )
            if return_dict:
                output = data
            else:
                # returns output in [image, mask, keypoints and bounding boxes
                if (
                    (data["mask"] is not None)
                    or (data["keypoints"] is not None)
                    or (data["bounding_boxes"] is not None)
                ):
                    output = [data["output"], data["mask"], data["keypoints"], data["bounding_boxes"]]
                else:
                    output = data["output"]

        return output

    def augment_single_image(self, image, mask, keypoints, bounding_boxes):
        """Applies the Augmentations in each phase of the pipeline.

        :param image: The image to apply Augmentations to. Minimum 30x30 pixels.
        :type image: numpy.array
        :param mask: The mask of labels for each pixel. Mask value should be in range of 0 to 255.
        :type mask: numpy array (uint8), optional
        :param keypoints: A dictionary of single or multiple labels where each label is a nested list of points coordinate (x, y).
        :type keypoints: dictionary, optional
        :param bounding_boxes: A nested list where each nested list contains box location (x1, y1, x2, y2).
        :type bounding_boxes: list, optional
        :return: A dictionary of AugmentationResults representing the changes
                 in each phase of the pipeline.
        :rtype: dictionary
        """

        # Check if image has correct channel
        if len(image.shape) > 2 and (image.shape[2] != 3 and image.shape[2] != 4):
            raise Exception(
                "Image should have channel number of 3 (BGR) or 4 (BGRA), but actual dimensions were {}.".format(
                    image.shape,
                ),
            )

        # Check that image is the correct size.
        if (image.shape[0] < 30) or (image.shape[1] < 30):
            raise Exception(
                "Image should have dimensions greater than 30x30, but actual dimensions were {}.".format(
                    image.shape,
                ),
            )

        # get and check valid image type ( uint or float)
        image_type = str(image.dtype)
        image_max_value = 255
        if image_type[:5] == "float":
            if np.max(image) <= 1:
                image_max_value = 1
                image = np.uint8(image * 255)
            else:
                image = np.uint8(image)
        elif image_type[:4] != "uint":
            raise Exception(
                "Image type should be uint or float, but the image type is {}.".format(
                    image_type,
                ),
            )

        # create augraphy cache folder
        cache_folder_path = os.path.join(os.getcwd() + "/augraphy_cache/")
        os.makedirs(cache_folder_path, exist_ok=True)
        cache_image_paths = glob(cache_folder_path + "*.png", recursive=True)

        file_indices = []
        modified_time = []
        for image_path in cache_image_paths:
            file_name = os.path.basename(image_path)
            file_indices.append(int(file_name[file_name.index("_") + 1 : -4]))
            modified_time.append(os.path.getmtime(image_path))

        # store 30 cache image files
        if len(cache_image_paths) >= 30:
            oldest_index = np.argmin(modified_time)
            outfilename = cache_folder_path + "image_" + str(file_indices[oldest_index]) + ".png"
            cv2.imwrite(
                outfilename,
                image,
            )

        else:
            current_image_index = len(cache_image_paths)
            outfilename = cache_folder_path + "image_" + str(current_image_index) + ".png"
            cv2.imwrite(
                outfilename,
                image,
            )

        data = dict()

        # Store performance metadata and other logs here.
        data["log"] = dict()

        # For storing augmentation execution times.
        data["log"]["time"] = list()
        data["log"]["augmentation_name"] = list()
        data["log"]["augmentation_status"] = list()
        data["log"]["augmentation_parameters"] = list()

        # This is useful.
        data["log"]["image_shape"] = image.shape

        data["image"] = image.copy()
        data["mask"] = None
        data["keypoints"] = None
        data["bounding_boxes"] = None

        data["pipeline"] = self
        data["pre"] = list()
        data["ink"] = list()
        data["paper"] = list()
        data["post"] = list()

        # If phases were defined None or [] in a custom pipeline, they wouldn't
        # be callable objects, so make them empty AugmentationSequences
        if len(self.ink_phase) == 0:
            self.ink_phase = AugmentationSequence([])

        if len(self.paper_phase) == 0:
            self.paper_phase = AugmentationSequence([])

        if len(self.post_phase) == 0:
            self.post_phase = AugmentationSequence([])

        # the input image
        image_input = data["image"].copy()

        # pre phase
        if len(self.pre_phase) > 0:
            if self.fixed_dpi:
                # compute and save a copy of image original dpi and doc dimensions
                dpi_object = DPIMetrics(image_input)
                original_dpi, doc_dimensions = dpi_object()
            # pre phase input
            data["pre"].append(
                AugmentationResult(None, image_input, mask=mask, keypoints=keypoints, bounding_boxes=bounding_boxes),
            )
            # apply pre phase augmentations
            self.apply_phase(data, layer="pre", phase=self.pre_phase)
            # the output of pre phase is the input for ink phase
            ink = data["pre"][-1].result
            mask = data["pre"][-1].mask
            keypoints = data["pre"][-1].keypoints
            bounding_boxes = data["pre"][-1].bounding_boxes
        else:
            ink = image_input

        # ink phase
        # ink phase input
        data["ink"].append(AugmentationResult(None, ink, mask=mask, keypoints=keypoints, bounding_boxes=bounding_boxes))
        # apply ink phase augmentations
        self.apply_phase(data, layer="ink", phase=self.ink_phase)

        # paper phase
        if (self.paper_color_range[0] != 0) | (self.paper_color_range[1] != 0):
            paper_color = random.randint(
                self.paper_color_range[0],
                self.paper_color_range[1],
            )
        else:
            paper_color = 255
        data["log"]["paper_color"] = paper_color
        # paper phase input
        data["paper"].append(
            AugmentationResult(
                None,
                np.full(
                    (data["ink"][-1].result.shape[0], data["ink"][-1].result.shape[1], 3),
                    paper_color,
                    dtype=np.uint8,
                ),
                mask=data["ink"][-1].mask,
                keypoints=data["ink"][-1].keypoints,
                bounding_boxes=data["ink"][-1].bounding_boxes,
            ),
        )
        # apply paper phase augmentations
        self.apply_phase(data, layer="paper", phase=self.paper_phase)

        # post phase
        # post phase input: ink and paper phases always have at least one result by now
        data["post"].append(
            AugmentationResult(
                None,
                self.print_ink_to_paper(
                    data,
                    data["ink"][-1].result.copy(),
                    data["paper"][-1].result.copy(),
                ),
                mask=data["ink"][-1].mask,
                keypoints=data["ink"][-1].keypoints,
                bounding_boxes=data["ink"][-1].bounding_boxes,
            ),
        )
        # apply post phase augmentations
        self.apply_phase(data, layer="post", phase=self.post_phase)

        if self.fixed_dpi and len(self.pre_phase) > 0:
            dpi_object = DPIMetrics(image_input)
            current_dpi, current_doc_dimensions = dpi_object()
            # resize to original input dpi if dpi is changed
            if current_dpi != original_dpi:
                image_resize = dpi_resize(
                    image=data["post"][-1].result,
                    doc_dimensions=current_doc_dimensions,
                    target_dpi=original_dpi,
                )
                data["post"].append(
                    AugmentationResult(
                        None,
                        image_resize,
                        data["post"][-1].mask,
                        data["post"][-1].keypoints,
                        data["post"][-1].bounding_boxes,
                    ),
                )

        # revert to input image type
        if image_type[:5] == "float":
            if image_max_value == 1:
                data["output"] = (data["post"][-1].result.astype(image_type)) / 255
            else:
                data["output"] = data["post"][-1].result.astype(image_type)
        else:
            data["output"] = data["post"][-1].result.astype("uint8")

        # additional outputs
        data["mask"] = data["post"][-1].mask
        data["keypoints"] = data["post"][-1].keypoints
        data["bounding_boxes"] = data["post"][-1].bounding_boxes

        # save each phase augmented images
        if self.save_outputs:
            self.save_images(data)

        # log probability
        if self.log:
            self.write_log(data)

        return data

    def save_images(self, data):
        """Save each augmented image in each phases to local disk.

        :param data: A dictionary of AugmentationResults representing the changes in each phase of the pipeline.
        :type data: dictionary
        """

        layer_names = ["pre", "ink", "paper", "post"]
        pre_layers = data["pre"]
        ink_layers = data["ink"]
        paper_layers = data["paper"]
        post_layers = data["post"]

        n = 0
        for j, layers in enumerate([pre_layers, ink_layers, paper_layers, post_layers]):

            # output path for each ink, paper and post phase images
            save_path = self.save_paths[j]

            # name of layer or phase
            layer_name = layer_names[j]

            for i, layer_data in enumerate(layers):
                if layer_data.metadata is None:
                    result = layer_data.result

                    # input layer
                    if layer_data.augmentation is None:
                        augmentation_name = layer_name + "_layer_input"
                        cv2.imwrite(
                            save_path + "p" + str(n) + "_" + layer_name + str(i) + "_" + augmentation_name + ".png",
                            result,
                        )
                        n += 1

                    # one of
                    elif layer_data.augmentation.__class__.__name__ == "OneOf":
                        augmentation_name = "oneof_"
                        n = self.get_oneof_data(
                            layer_data.augmentation,
                            result,
                            save_path,
                            layer_name,
                            augmentation_name,
                            i,
                            n,
                        )

                    # sequence
                    elif layer_data.augmentation.__class__.__name__ == "AugmentationSequence":
                        augmentation_name = "sequence_"
                        n = self.get_sequence_data(
                            layer_data.augmentation,
                            result,
                            save_path,
                            layer_name,
                            augmentation_name,
                            i,
                            n,
                        )

                    # normal augmentations
                    else:
                        augmentation_name = layer_data.augmentation.__class__.__name__
                        cv2.imwrite(
                            save_path + "p" + str(n) + "_" + layer_name + str(i) + "_" + augmentation_name + ".png",
                            result,
                        )
                        n += 1

    def get_oneof_data(self, augmentation, result, save_path, layer_name, augmentation_name, i, n):
        """Get augmentation information from OneOf augmentation recursively or save the augmented image in disk.

        :param augmentation: Augmentation object of OneOf augmentation.
        :type augmentation: class instance
        :param result: Augmentation output, it may be nested in a list.
        :type result: list or numpy array.
        :param save_path: Output path of result.
        :type save_path: list
        :param layer_name: Name of current layer.
        :type layer_name: list
        :param augmentation_name: A combined name of augmentations, seperated by _.
        :type augmentation_name: list
        :param i: Index of current augmentation in total number of augmentations.
        :type i: int
        :param n: Index of current augmented in total number of augmented images.
        :type n: int
        """

        current_augmentation = augmentation.augmentations[np.argmax(augmentation.augmentation_probabilities)]
        # sequence inside oneof
        if current_augmentation.__class__.__name__ == "AugmentationSequence":
            augmentation_name += "sequence_"
            n = self.get_sequence_data(current_augmentation, result, save_path, layer_name, augmentation_name, i, n)
        # oneof inside oneof
        elif current_augmentation.__class__.__name__ == "OneOf":
            augmentation_name += "oneof_"
            n = self.get_oneof_data(current_augmentation, result, save_path, layer_name, augmentation_name, i, n)
        # augmentations inside oneof
        else:
            augmentation_name += current_augmentation.__class__.__name__
            cv2.imwrite(save_path + "p" + str(n) + "_" + layer_name + str(i) + "_" + augmentation_name + ".png", result)
            n += 1
        return n

    def get_sequence_data(self, augmentation, result, save_path, layer_name, input_augmentation_name, i, n):
        """Get augmentation information from AugmentationSequence augmentation recursively or save the augmented image in disk.

        :param augmentation: Augmentation object of OneOf augmentation.
        :type augmentation: class instance
        :param result: Augmentation output, it may be nested in a list.
        :type result: list or numpy array.
        :param save_path: Output path of result.
        :type save_path: list
        :param layer_name: Name of current layer.
        :type layer_name: list
        :param augmentation_name: A combined name of augmentations, seperated by _.
        :type augmentation_name: list
        :param i: Index of current augmentation in total number of augmentations.
        :type i: int
        :param n: Index of current augmented in total number of augmented images.
        :type n: int
        """

        s = 0
        for current_augmentation, result in zip(augmentation.augmentations, augmentation.results):
            augmentation_name = copy(input_augmentation_name) + str(s) + "_"
            # sequence inside sequence
            if current_augmentation.__class__.__name__ == "AugmentationSequence":
                # sequence returns (result, self.augmentations), so get result only here
                result = result[0]
                augmentation_name += "sequence_"
                n = self.get_sequence_data(current_augmentation, result, save_path, layer_name, augmentation_name, i, n)
            # oneof inside sequence
            elif current_augmentation.__class__.__name__ == "OneOf":
                # oneof returns (image, [augmentation]), so get image only here
                result = result[0]
                augmentation_name += "oneof_"
                n = self.get_oneof_data(current_augmentation, result, save_path, layer_name, augmentation_name, i, n)
            # augmentations inside sequence
            else:
                augmentation_name += current_augmentation.__class__.__name__
                if result is not None:
                    cv2.imwrite(
                        save_path + "p" + str(n) + "_" + layer_name + str(i) + "_" + augmentation_name + ".png",
                        result,
                    )
                n += 1
            s += 1
        return n

    def write_log(self, data):
        """Save augmentations log to local disk.

        :param data: A dictionary of AugmentationResults representing the changes in each phase of the pipeline.
        :type data: dictionary
        """

        # path to log file
        log_file_name = "log_" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".txt"
        log_prob_file_path = self.log_prob_path + log_file_name

        augmentation_names = data["log"]["augmentation_name"]
        augmentation_status = data["log"]["augmentation_status"]
        augmentation_parameters = deepcopy(data["log"]["augmentation_parameters"])

        # remove image array and replace it with shape
        for j, augmentation_parameter in enumerate(augmentation_parameters):
            # check and convert from tuple to list
            if isinstance(augmentation_parameter, tuple):
                augmentation_parameter = list(augmentation_parameter)
                augmentation_parameters[j] = augmentation_parameter
            check_values = [augmentation_parameter]
            while check_values:
                value = check_values.pop(0)
                if value:
                    if isinstance(value, list):
                        for i, nested_value in enumerate(value):
                            if hasattr(nested_value, "shape"):
                                value[i] = nested_value.shape
                            elif (
                                isinstance(nested_value, list)
                                or isinstance(nested_value, tuple)
                                or hasattr(nested_value, "shape")
                            ):
                                # convert from tuple to list
                                if isinstance(nested_value, tuple):
                                    nested_value = list(nested_value)
                                    value[i] = nested_value
                                check_values.append(nested_value)
                    elif hasattr(value, "items"):
                        for parameter, nested_value in value.items():
                            if hasattr(nested_value, "shape"):
                                value[parameter] = nested_value.shape
                            elif (
                                isinstance(nested_value, list)
                                or isinstance(nested_value, tuple)
                                or hasattr(nested_value, "shape")
                            ):
                                # convert from tuple to list
                                if isinstance(nested_value, tuple):
                                    nested_value = list(nested_value)
                                    value[parameter] = nested_value
                                check_values.append(nested_value)

        with open(log_prob_file_path, "w+") as file:
            for (name, status, parameters) in zip(
                augmentation_names,
                augmentation_status,
                augmentation_parameters,
            ):
                file.write("%s,%s,%s \n" % (name, status, parameters))
                # put a space
                file.write("\n")
        file.close()

    def apply_phase(self, data, layer, phase):
        """Applies every augmentation in a phase.

        :param data: A dictionary of AugmentationResults representing the changes in each phase of the pipeline.
        :type data: dictionary
        :param layer: The name of current layer or phase.
        :type layer: string
        :param phase: Collection of Augmentations to apply.
        :type phase: base.augmentationsequence or list
        """

        for augmentation in phase.augmentations:
            result = data[layer][-1].result.copy()
            mask, keypoints, bounding_boxes = None, None, None
            if data[layer][-1].mask is not None:
                mask = data[layer][-1].mask.copy()
            if data[layer][-1].keypoints is not None:
                keypoints = deepcopy(data[layer][-1].keypoints)
            if data[layer][-1].bounding_boxes is not None:
                bounding_boxes = deepcopy(data[layer][-1].bounding_boxes)

            if augmentation.should_run():
                start = time.process_time()  # time at start of execution

                result = augmentation(
                    image=result,
                    layer=layer,
                    mask=mask,
                    keypoints=keypoints,
                    bounding_boxes=bounding_boxes,
                    force=True,
                )
                end = time.process_time()  # time at end of execution
                elapsed = end - start  # execution duration
                data["log"]["time"].append((augmentation, elapsed))

                # not "OneOf" or "AugmentationSequence"
                if isinstance(augmentation, Augmentation):
                    # unpacking augmented image, mask, keypoints and bounding boxes from output
                    if (mask is not None) or (keypoints is not None) or (bounding_boxes is not None):
                        result, mask, keypoints, bounding_boxes = result

            else:
                result = None

            data["log"]["augmentation_name"].append(augmentation.__class__.__name__)
            if result is None:
                data["log"]["augmentation_status"].append(False)
                data["log"]["augmentation_parameters"].append("")
                data[layer].append(
                    AugmentationResult(
                        augmentation,
                        data[layer][-1].result.copy(),
                        mask,
                        keypoints,
                        bounding_boxes,
                        'This augmentation did not run, its "result" is unchanged.',
                    ),
                )
            else:
                data["log"]["augmentation_status"].append(True)
                data["log"]["augmentation_parameters"].append(augmentation.__dict__)
                # for "OneOf" or "AugmentationSequence"
                while isinstance(result, tuple) or isinstance(result, list):
                    result, augmentations = result
                    for nested_augmentation in augmentations:
                        data["log"]["augmentation_name"].append(
                            nested_augmentation.__class__.__name__,
                        )
                        data["log"]["augmentation_status"].append(True)
                        data["log"]["augmentation_parameters"].append(
                            nested_augmentation.__dict__,
                        )
                    # unpacking augmented image, mask, keypoints and bounding boxes from output
                    if (mask is not None) or (keypoints is not None) or (bounding_boxes is not None):
                        result, mask, keypoints, bounding_boxes = result

                data[layer].append(AugmentationResult(augmentation, result, mask, keypoints, bounding_boxes))

    def print_ink_to_paper(self, data, overlay, background):
        """Applies the ink layer to the paper layer.

        :param data: A dictionary of AugmentationResults representing the changes in each phase of the pipeline.
        :type data: dictionary
        :param overlay: Foreground of overlay process, output from ink phase.
        :type overlay: numpy array
        :param background: Background of overlay process, output from paper phase.
        :type background: numpy array
        """

        if (self.ink_color_range[0] != -1) or (self.ink_color_range[1] != -1):
            ink_color = random.randint(self.ink_color_range[0], self.ink_color_range[1])
        else:
            ink_color = -1
        data["log"]["ink_color"] = ink_color

        # prevent inconsistency in size between background and overlay
        if overlay.shape[:2] != background.shape[:2]:
            overlay_y, overlay_x = overlay.shape[:2]
            background = cv2.resize(
                background,
                (overlay_x, overlay_y),
                interpolation=cv2.INTER_AREA,
            )

        # preserve alpha layer
        has_alpha = 0
        if len(overlay.shape) > 2 and overlay.shape[2] == 4:
            has_alpha = 1
            image_alpha = overlay[:, :, 3]
            overlay = overlay[:, :, :3]

        ink_to_paper_builder = OverlayBuilder(
            overlay_types=self.overlay_type,
            foreground=overlay,
            background=background,
            ntimes=1,
            nscales=(1, 1),
            edge="center",
            edge_offset=0,
            alpha=self.overlay_alpha,
            ink_color=ink_color,
        )

        image_blended = ink_to_paper_builder.build_overlay()

        if has_alpha:
            image_blended = np.dstack((image_blended, image_alpha))

        return image_blended

    def __repr__(self):
        r = f"pre_phase = {repr(self.pre_phase)}\n\n"
        r += f"ink_phase = {repr(self.ink_phase)}\n\n"
        r += f"paper_phase = {repr(self.paper_phase)}\n\n"
        r += f"post_phase = {repr(self.post_phase)}\n\n"
        r += f"AugraphyPipeline(pre_phase , ink_phase, paper_phase, post_phase, overlay_type={self.overlay_type}, overlay_alpha={self.overlay_alpha}, ink_color_range={self.ink_color_range}, paper_color_range={self.paper_color_range}, save_outputs={self.save_outputs}, log={self.log}, random_seed={self.random_seed})"
        return r

    def visualize(self):
        print(repr(self))

    def __call__(self, image):
        return self.augment(image, return_dict=0)

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "lizlooney@google.com (Liz Looney)"

# Other Modules
import numpy as np

# My Modules
import util


def __convert_bbox_to_text(bbox, scale):
    # Scale the bbox
    p0 = bbox[:2].astype(float)
    p1 = p0 + bbox[2:].astype(float)
    size = p1 - p0
    center = p0 + (size / 2)
    new_size = scale * size
    p0 = center - new_size / 2
    p1 = center + new_size / 2
    scaled_bbox = np.array([p0, p1 - p0]).reshape(-1)
    # Convert the scaled bbox to rect to match format x1, y1, x2, y2
    p0 = scaled_bbox[:2]
    size = scaled_bbox[2:]
    p1 = p0 + size
    return "%d,%d,%d,%d" % (int(p0[0]), int(p0[1]), int(p1[0]), int(p1[1]))


def __convert_bboxes_and_labels_to_text(bboxes, scale, labels):
    assert(len(bboxes) == len(labels))
    bboxes_text = ""
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        label = labels[i]
        if bbox is None or label is None:
            continue
        bboxes_text += "%s,%s\n" % (__convert_bbox_to_text(bbox, scale), label)
    return bboxes_text


def __convert_rects_to_bboxes(rects):
    bboxes = []
    for rect in rects:
        p0 = rect[:2]
        p1 = rect[2:]
        size = p1 - p0
        bbox = np.array([p0, size]).reshape(-1)
        bboxes.append(bbox)
    return bboxes


def __convert_text_to_rects_and_labels(bboxes_text):
    rects = []
    labels = []
    lines = bboxes_text.split("\n")    
    for line in lines:
        try:
            *rect, label = line.strip().split(",")
            assert(len(rect) == 4)
            rect = np.array(rect, dtype=float).astype(int)
            rects.append(rect)
            labels.append(label)
        except Exception as e:
            continue
    return rects, labels


def __convert_text_to_bboxes_and_labels(bboxes_text):
    rects, labels = __convert_text_to_rects_and_labels(bboxes_text)
    bboxes = __convert_rects_to_bboxes(rects)
    return bboxes, labels


def __scale_bboxes(bboxes, scale):
    scaled_bboxes = []
    for bbox in bboxes:
        if bbox is None:
            scaled_bboxes.append(None)
        else:
            p0 = bbox[:2].astype(float)
            p1 = p0 + bbox[2:].astype(float)
            size = p1 - p0
            center = p0 + (size / 2)
            new_size = scale * size
            p0 = center - new_size / 2
            p1 = center + new_size / 2
            scaled_bboxes.append(np.array([p0, p1 - p0]).reshape(-1))
    return scaled_bboxes


def parse_bboxes_text(bboxes_text, scale=1):
    bboxes_, labels = __convert_text_to_bboxes_and_labels(bboxes_text)
    bboxes = __scale_bboxes(bboxes_, scale)
    return bboxes, labels


def parse_bboxes_text_to_labels(bboxes_text):
    _, labels = __convert_text_to_bboxes_and_labels(bboxes_text)
    return labels


def format_bboxes_text(bboxes, labels, scale):
    return __convert_bboxes_and_labels_to_text(bboxes, 1 / scale, labels)
# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dataclasses import dataclass
from typing import Callable, Tuple, Union

import torch

from flash.core.data.io.input_transform import InputTransform
from flash.core.data.transforms import kornia_collate
from flash.core.utilities.imports import _TORCHVISION_AVAILABLE

if _TORCHVISION_AVAILABLE:
    from torchvision import transforms as T


@dataclass
class ImageClassificationInputTransform(InputTransform):

    image_size: Tuple[int, int] = (196, 196)
    mean: Union[float, Tuple[float, float, float]] = (0.485, 0.456, 0.406)
    std: Union[float, Tuple[float, float, float]] = (0.229, 0.224, 0.225)

    def input_per_sample_transform(self):
        return T.Compose([T.ToTensor(), T.Resize(self.image_size), T.Normalize(self.mean, self.std)])

    def train_input_per_sample_transform(self):
        return T.Compose(
            [T.ToTensor(), T.Resize(self.image_size), T.Normalize(self.mean, self.std), T.RandomHorizontalFlip()]
        )

    def target_per_sample_transform(self) -> Callable:
        return torch.as_tensor

    def collate(self) -> Callable:
        # TODO: Remove kornia collate for default_collate
        return kornia_collate

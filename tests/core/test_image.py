import os

import pytest
from PIL import Image

from src.core.image import search_most_common_color


@pytest.mark.parametrize(
    "image, color",
    [
        ("HE002EMKLGV2_11830316_1_v1.jpg", "cdb678"),
        ("TR776EMKFNC4_11819445_1_v1_2x.jpg", "74575e"),
    ],
)
def test_most_common_color_search(image: str, color: str, test_data_dir: str) -> None:
    """
    Arrange: картинка и ожидаемый цвет
    Act: определяем цвет
    Assert: Определененный цвет доджен быть равен ожидаемому
    """
    img = Image.open(os.path.join(test_data_dir, image))

    actual_color = search_most_common_color(img)

    assert actual_color == color

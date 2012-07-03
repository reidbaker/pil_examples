import Image
from image_transforms import tileify
from image_transforms import calculate_random_location

class TestTileify:
    def test_smoke(self):
        """
        Smoke test to make sure tileify runs without errors
        REQUIRES photo named test_photo.jpg to be in current dir
        """
        image_data = Image.open("test_photo.jpg")
        num_tiles = 10
        max_shift = 30
        new_image_data = tileify(image_data, num_tiles, max_shift)
        assert new_image_data

    def test_calculate_random_location(self):
        start_x = 10
        start_y = 10
        max_shift = 10
        # Because it is random call it a few times to catch a mistake
        for i in xrange(10):
            (x, y) = calculate_random_location(start_x, start_y, max_shift)
            assert x >= start_x - max_shift
            assert x <= start_x + max_shift
            assert y >= start_y - max_shift
            assert y <= start_y + max_shift

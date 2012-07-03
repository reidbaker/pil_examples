from ..image_transforms import tileify

def test_equal():       # py.test looks for functions that start with test_
    import ipdb; ipdb.set_trace()
    assert tileify(3) == 5

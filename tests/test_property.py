from app.utils import interpolate_value

from hypothesis import given, strategies, settings
import pytest

class TestInterpolation:
    @given(
        start_value=strategies.integers(min_value=0, max_value=255),
        end_value=strategies.integers(min_value=0, max_value=255),
        start_time=strategies.floats(min_value=0.0, max_value=100.0),
        end_time=strategies.floats(min_value=0.0, max_value=100.0),
        current_time=strategies.floats(min_value=0.0, max_value=100.0),
    )
    @settings(max_examples=100)
    def test_interpolate_value(self, start_value, end_value, start_time, end_time, current_time):
        if start_time > end_time:
            try:
                interpolate_value(start_value, end_value, start_time, end_time, current_time)
            except ValueError:
                assert True
            return

        result = interpolate_value(start_value, end_value, start_time, end_time, current_time)
        assert 0 <= result <= 255
        if current_time < start_time:
            assert result == start_value
        elif current_time > end_time:
            assert result == end_value
        elif start_time == end_time:
            assert result == start_value
        else:
            expected_result = int(start_value + (end_value - start_value) * ((current_time - start_time) / (end_time - start_time)))
            expected_result = max(0, min(255, expected_result))
            assert result == expected_result

    def test_interpolate_value_exact_start(self):
        assert interpolate_value(10, 20, 0.0, 10.0, 0.0) == 10

    def test_interpolate_value_exact_end(self):
        assert interpolate_value(10, 20, 0.0, 10.0, 10.0) == 20

    def test_interpolate_value_before_start(self):
        assert interpolate_value(10, 20, 5.0, 10.0, 2.0) == 10

    def test_interpolate_value_after_end(self):
        assert interpolate_value(10, 20, 5.0, 10.0, 12.0) == 20

    def test_interpolate_value_midpoint(self):
        assert interpolate_value(0, 100, 0.0, 10.0, 5.0) == 50

    def test_interpolate_value_clamping(self):
        assert interpolate_value(-100, 0, 0.0, 10.0, 5.0) == 0
        assert interpolate_value(200, 300, 0.0, 10.0, 10.0) == 255

    def test_interpolate_value_start_equals_end_time(self):
        assert interpolate_value(42, 99, 5.0, 5.0, 5.0) == 42

    def test_interpolate_value_invalid_time(self):
        with pytest.raises(ValueError):
            interpolate_value(10, 20, 10.0, 5.0, 7.0)

# Funzione che interpola il valore di un canale DMX in base ai keyframes

def interpolate_value(
    start_value: int,
    end_value: int,
    start_time: float,
    end_time: float,
    current_time: float,
) -> int:
    """
    Interpolates the value of a DMX channel based on keyframes.
    :param start_value: The starting value of the channel.
    :param end_value: The ending value of the channel.
    :param start_time: The time at which the starting value is set.
    :param end_time: The time at which the ending value is set.
    :param current_time: The current time for which the value is to be interpolated.
    :return: The interpolated value of the channel.
    """
    if current_time < start_time:
        return start_value
    if current_time > end_time:
        return end_value
    if start_time > end_time:
        raise ValueError("Start time must be less than or equal to end time.")

    if start_time == end_time:
        return start_value

    # Calculate the interpolation factor
    factor = (current_time - start_time) / (end_time - start_time)

    # Clamp the factor to the range [0, 1]
    factor = max(0, min(1, factor))

    # Interpolate the value
    interpolated_value = int(start_value + (end_value - start_value) * factor)
    if interpolated_value < 0:
        interpolated_value = 0
    if interpolated_value > 255:
        interpolated_value = 255

    return interpolated_value

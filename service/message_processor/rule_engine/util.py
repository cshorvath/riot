def get_input_topic_pattern(prefix: str):
    return f"{prefix}/device/+/outgoing"


def get_output_topic_pattern(prefix: str, device_id: int):
    return f"{prefix}/device/+/{device_id}"

import logging


def parse_device_id(topic_name: str, device_id_idx: int = 2) -> int:
    """
    Parses device id from topic name. Topic name expected to consist of parts separated with "/"
    :param device_id_idx:
    :param topic_name:
    :return: device id
    """
    topic_splitted = topic_name.split("/")
    if len(topic_splitted) >= device_id_idx + 1:
        device_id_str = topic_splitted[device_id_idx]
        if device_id_str.isdigit():
            return int(device_id_str)
    logging.error(f"Unable to parse device_id from topic name: {topic_name}")
    return -1
from enum import Enum
from typing import Generator

from langflow.schema import Record
from langflow.schema.message import Message


class ArtifactType(str, Enum):
    TEXT = "text"
    RECORD = "record"
    OBJECT = "object"
    ARRAY = "array"
    STREAM = "stream"
    UNKNOWN = "unknown"
    MESSAGE = "message"


def get_artifact_type(value, build_result=None) -> str:
    result = ArtifactType.UNKNOWN
    match value:
        case Record():
            result = ArtifactType.RECORD

        case str():
            result = ArtifactType.TEXT

        case dict():
            result = ArtifactType.OBJECT

        case list():
            result = ArtifactType.ARRAY

        case Message():
            result = ArtifactType.MESSAGE

    if result == ArtifactType.UNKNOWN:
        if build_result and isinstance(build_result, Generator):
            result = ArtifactType.STREAM
        elif isinstance(value, Message) and isinstance(value.text, Generator):
            result = ArtifactType.STREAM

    return result.value


def post_process_raw(raw, artifact_type: str):
    if artifact_type == ArtifactType.STREAM.value:
        raw = ""

    return raw
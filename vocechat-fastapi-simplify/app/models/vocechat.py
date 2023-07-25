from typing import Optional, Union, Set, List
from pydantic import BaseModel


# voce
class VoceProperties(BaseModel):
    content_type: Union[str, None] = None
    height: Union[int, None] = None
    width: Union[int, None] = None
    name: Union[str, None] = None
    size: Union[int, None] = None


class VoceDetail(BaseModel):
    content: Union[str, None] = None
    content_type: Union[str, None] = None
    expires_in: Union[str, None] = None
    properties: Union[VoceProperties, None] = None
    type: Union[str, None] = None


class VoceTarget(BaseModel):
    gid: Union[int, None] = None


class VoceMsg(BaseModel):
    created_at: Union[str, None] = None
    detail: Union[VoceDetail, None] = None
    from_uid: Union[int, None] = None
    mid: Union[int, None] = None
    target: Union[VoceTarget, None] = None


class VerificationCode(BaseModel):
    code: str
    expire_time: Union[int, None] = None

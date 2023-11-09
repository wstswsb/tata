from pydantic import BaseModel


class CheckPingIn(BaseModel):
    target_ip: str

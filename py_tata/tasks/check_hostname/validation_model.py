from pydantic import BaseModel, ConfigDict


class CheckHostnameIn(BaseModel):
    target_hostname: str

    model_config = ConfigDict(extra="forbid")

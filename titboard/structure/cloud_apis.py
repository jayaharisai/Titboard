from pydantic import BaseModel

class AWSCredentials(BaseModel):
    access_key: str
    secret_key: str
    region: str


class InstanceRequest(BaseModel):
    instance_id: str

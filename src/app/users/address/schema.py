import uuid
import pydantic as pyd


class IAddressIn(pyd.BaseModel):
    street: str = pyd.Field(max_length=(100))
    city: str = pyd.Field(max_length=(100))
    state: str = pyd.Field(max_length=(100))
    zipcode: str = pyd.Field(max_length=(10))


class IAddressOut(IAddressIn):
    id: uuid.UUID

    class Config:
        orm_mode = True

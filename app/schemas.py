from pydantic import BaseModel, ConfigDict


class ContactCreate(BaseModel):
    name: str
    mobile: str
    email: str


class ContactResponse(BaseModel):
    id: int
    name: str
    mobile: str
    email: str

    model_config = ConfigDict(from_attributes=True)
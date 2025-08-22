from pydantic import BaseModel, Field


class IntermittentCreate(BaseModel):
    first_name: str
    last_name: str
    is_active: bool = Field(default=True)
    skills: str | None = Field(default=None)


class IntermittentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    skills: str | None = None


class IntermittentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    is_active: bool
    skills: str | None

    class Config:
        from_attributes = True

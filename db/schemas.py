from pydantic import BaseModel


class ProfileBase(BaseModel):
    title: str
    description: str | None = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    Profiles: list[Profile] = []

    class Config:
        from_attributes = True
import uuid

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON

class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=20)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str

    chats: list["Chat"] = Relationship(back_populates="owner", cascade_delete=True)

# UserCreate is used to validate user input for db entry creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# UserRead is used to return user data to the client via API
class UserRead(UserBase):
    id: uuid.UUID

# UserRegister is used to validate user input for registration via API
class UserRegister(SQLModel):
    username: str = Field(max_length=20)
    password: str = Field(min_length=8, max_length=40)

class ChatBase(SQLModel):
    title: str = Field()
    context: list[str] = Field(default_factory=list, sa_type=JSON)

class Chat(ChatBase, table=True):
    __tablename__ = "chats"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(default=None)
    owner_id: uuid.UUID = Field(foreign_key="users.id")

    owner: User = Relationship(back_populates="chats")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.title is None:
            self.title = f"Chat-{self.id.hex[:8]}"

class ChatCreate(ChatBase):
    pass

class ChatRead(ChatBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class ChatsRead(SQLModel):
    chats: list[ChatRead]
    count: int

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
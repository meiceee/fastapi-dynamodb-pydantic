from typing import Any, List

from models.lib.functions import generate_current_timestamp, generate_uuid
from pydantic import BaseModel, Field, RootModel, model_validator


class PostCreateRequest(BaseModel):
    """新しいランチ投稿を作成するためのリクエストモデル"""

    content: str = Field(validation_alias="content")
    image_key: str = Field(validation_alias="imageKey")
    restaurant: str = Field(validation_alias="restaurant")


class PostCreateToDB(BaseModel):
    """新しいランチ投稿のデータベース登録用モデル"""

    id: str
    pk: str = "Posts"
    sk: str
    user_id: str
    timestamp: str = Field(default_factory=generate_current_timestamp)
    content: str
    image_key: str
    restaurant: str
    likes: list = []

    @model_validator(mode="before")
    @classmethod
    def generate_values(cls, values: dict[str, Any]) -> dict[str, Any]:
        """id, skを生成するメソッド"""
        id = generate_uuid()
        values["id"] = id
        values["sk"] = f"Post#{id}"

        return values


class PostCreatedResponse(BaseModel):
    """新しいランチ投稿のレスポンスモデル"""

    id: str = Field(serialization_alias="id")
    pk: str = Field(exclude=True)
    sk: str = Field(exclude=True)
    user_id: str = Field(serialization_alias="userId")
    timestamp: str = Field(serialization_alias="timestamp")
    content: str = Field(serialization_alias="content")
    image_key: str = Field(serialization_alias="imageKey")
    restaurant: str = Field(serialization_alias="restaurant")
    likes: list = Field(serialization_alias="likes")


class PostInfoInDB(BaseModel):
    """DynamoDBに格納されているランチ投稿情報のモデル"""

    pk: str = Field(validation_alias="PK")
    sk: str = Field(validation_alias="SK")
    user_id: str = Field(validation_alias="UserId")
    timestamp: str = Field(validation_alias="Timestamp")
    content: str = Field(validation_alias="Content")
    image_key: str = Field(validation_alias="ImageKey")
    restaurant: str = Field(validation_alias="Restaurant")
    likes: List[str] = Field(validation_alias="Likes")


class PostInfoReponse(PostInfoInDB):
    """ランチ投稿情報のレスポンスモデル"""

    id: str
    pk: str = Field(validation_alias="PK", exclude=True)
    sk: str = Field(validation_alias="SK", exclude=True)
    user_id: str = Field(validation_alias="UserId", serialization_alias="userId")
    timestamp: str = Field(validation_alias="Timestamp", serialization_alias="timestamp")
    content: str = Field(validation_alias="Content", serialization_alias="content")
    image_key: str = Field(validation_alias="ImageKey", serialization_alias="imageKey")
    restaurant: str = Field(validation_alias="Restaurant", serialization_alias="restaurant")
    likes: list = Field(validation_alias="Likes", serialization_alias="likes")

    @model_validator(mode="before")
    @classmethod
    def generate_values(cls, values: dict[str, Any]) -> dict[str, Any]:
        """idを生成するメソッド"""
        id = values["SK"].split("#")[1]
        values["id"] = id

        return values


PostInfoListResponse = RootModel[List[PostInfoReponse]]

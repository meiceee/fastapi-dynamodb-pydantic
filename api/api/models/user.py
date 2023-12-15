from pydantic import BaseModel, Field


class CognitoUser(BaseModel):
    """Cognitoから取得したユーザー情報のモデル"""

    username: str = Field(validation_alias="cognito:username")
    email: str = Field(validation_alias="email")

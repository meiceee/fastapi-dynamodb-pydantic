from models.user import CognitoUser
from starlette.requests import Request


def get_user_info_from_request(request: Request) -> CognitoUser:
    """リクエストからユーザー情報を取得する"""
    auth_info = request.scope["aws.event"]["requestContext"]["authorizer"]["claims"]

    return CognitoUser(**auth_info)

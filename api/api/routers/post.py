from botocore.exceptions import ClientError
from databases.tables.lunch_blog import LunchBlogTable
from fastapi import APIRouter, HTTPException, status
from models.post import (
    PostCreatedResponse,
    PostCreateRequest,
    PostCreateToDB,
    PostInfoInDB,
    PostInfoListResponse,
    PostInfoReponse,
)
from starlette.requests import Request
from utils.cognito import get_user_info_from_request
from utils.error import NotFoundError
from utils.logger import logger

router = APIRouter(
    tags=["Posts"],
)

lunch_blog_table = LunchBlogTable()


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreatedResponse)
def create_posts(request: Request, post: PostCreateRequest):
    """新しいランチ投稿を作成"""

    try:
        user_info = get_user_info_from_request(request)

        new_post_item = PostCreateToDB(
            **post.dict(),
            user_id=user_info.username,
        )
        logger.debug(new_post_item)

        lunch_blog_table.create_post(new_post_item)
    except ClientError as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return new_post_item


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=PostInfoListResponse)
def get_posts():
    """全てのランチ投稿を取得"""

    try:
        posts = lunch_blog_table.get_posts()
    except ClientError as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return posts


@router.post("/posts/{post_id}/likes", status_code=status.HTTP_200_OK, response_model=PostInfoReponse)
def update_likes(request: Request, post_id: str):
    """ランチ投稿にいいねを追加"""

    try:
        user_info = get_user_info_from_request(request)

        post_response = lunch_blog_table.get_post(post_id)
        post = PostInfoInDB(**post_response)
        post.likes.append(user_info.username)

        updated_post = lunch_blog_table.update_post_likes(post)
    except ClientError as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except NotFoundError as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return updated_post

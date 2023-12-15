import os

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from databases.setting import DynamodbTable
from models.post import PostCreateToDB
from utils.error import NotFoundError
from utils.logger import logger


class LunchBlogTable(DynamodbTable):
    """LunchBlogテーブルを操作するためのクラス"""

    def __init__(self):
        # DynamoDBのテーブル名をLambdaの環境変数から取得
        table_name = os.getenv("DYNAMODB_LUNCH_BLOG_TABLE")
        super().__init__(table_name)

    def create_post(self, post: PostCreateToDB):
        """新しいランチ投稿を作成"""
        try:
            self.table.put_item(
                Item={
                    "PK": post.pk,
                    "SK": post.sk,
                    "UserId": post.user_id,
                    "Timestamp": post.timestamp,
                    "Content": post.content,
                    "ImageKey": post.image_key,
                    "Restaurant": post.restaurant,
                    "Likes": post.likes,
                }
            )
        except ClientError as err:
            logger.exception(err)
            raise

    def get_posts(self):
        """全てのランチ投稿を取得"""
        try:
            response = self.table.query(
                KeyConditionExpression=Key("PK").eq("Posts") & Key("SK").begins_with("Post#"),
            )
        except ClientError as err:
            logger.exception(err)
            raise
        else:
            return response["Items"]

    def get_post(self, post_id: str):
        """特定のランチ投稿を取得"""
        try:
            response = self.table.get_item(
                Key={
                    "PK": "Posts",
                    "SK": f"Post#{post_id}",
                },
            )
            if "Item" not in response:
                raise NotFoundError(f"Post#{post_id} is not found.")
        except ClientError as err:
            logger.exception(err)
            raise
        else:
            return response["Item"]

    def update_post_likes(self, post: PostCreateToDB):
        """ランチ投稿のいいねを更新"""
        try:
            response = self.table.update_item(
                Key={
                    "PK": post.pk,
                    "SK": post.sk,
                },
                UpdateExpression="SET Likes = :likes",
                ExpressionAttributeValues={
                    ":likes": post.likes,
                },
                ReturnValues="ALL_NEW",
            )
        except ClientError as err:
            logger.exception(err)
            raise
        else:
            return response["Attributes"]

from boto3 import resource

dynamodb = resource("dynamodb", region_name="ap-northeast-1")


class DynamodbTable:
    """DynamoDBのテーブルを操作するための基底クラス"""

    def __init__(self, table_name):
        self.table = dynamodb.Table(table_name)
        self.dynamodb = dynamodb

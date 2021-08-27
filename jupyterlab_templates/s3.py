import os
from collections import defaultdict

class S3TemplateLoader:
    def __init__(self, bucket, aws_access_key, aws_secret_key, prefix="", **kwargs):
        self.bucket = bucket
        self.prefix = prefix
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self._client = None

    @property
    def client(self):
        if not self._client:
            import boto3
            # So we can test by redirecting to docker
            # endpoint_url = os.getenv("AWS_ENDPOINT_URL")
            # self._client = boto3.client("s3", endpoint_url=endpoint_url)
            self._client = boto3.client("s3", aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key, region_name="ap-south-1")
        return self._client

    def get_paths(self):
        return ["s3://{}/{}".format(self.bucket, self.prefix)]

    def _get_files(self):
        paginator = self.client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix=self.prefix)
        for page in page_iterator:
            for key in page.get("Contents", []):
                yield key["Key"]

    def get_templates(self):
        templates = defaultdict(list)
        templates_by_path = {}

        for path in self._get_files():
            obj = self.client.get_object(Bucket=self.bucket, Key=path)
            filename = os.path.basename(path)
            dirname = os.path.dirname(path)

            data = {
                "name": "{}/{}".format(dirname, filename),
                "path": path,
                "dirname": dirname,
                "content": obj["Body"].read().decode("utf-8"),
            }
            templates[dirname].append({"name": filename})
            templates_by_path[filename] = data

        return templates, templates_by_path
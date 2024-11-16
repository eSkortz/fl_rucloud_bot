from s3fs import S3FileSystem
from config import S3_URL, S3_PUBLIC_KEY, S3_PRIVATE_KEY


class S3Namespace:
    def __init__(self):
        self.s3 = S3FileSystem(
            key=S3_PUBLIC_KEY.get_secret_value(),
            secret=S3_PRIVATE_KEY.get_secret_value(),
            client_kwargs={"endpoint_url": S3_URL.get_secret_value()},
        )

    def create_file(self, path: str, content: str) -> None:
        with self.s3.open(path, "w") as f:
            f.write(content)

    def delete_file(self, path: str) -> None:
        self.s3.rm(path)

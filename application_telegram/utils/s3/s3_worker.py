from s3fs import S3FileSystem
from config import S3_URL, S3_PUBLIC_KEY, S3_PRIVATE_KEY


class S3Worker:
    def __init__(self):
        self.s3 = S3FileSystem(
            key=S3_PUBLIC_KEY,
            secret=S3_PRIVATE_KEY,
            client_kwargs={"endpoint_url": S3_URL},
        )

    async def create_file(self, path: str, content: bytes) -> None:
        if not isinstance(content, bytes):
            raise TypeError("Content must be of type bytes")
        async with self.s3.open_async(path, "wb") as file:
            await file.write(content)

    def delete_file(self, path: str) -> None:
        self.s3.rm(path)

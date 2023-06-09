import asyncio
from streaming_form_data.targets import BaseTarget
from boto3_my.Uploader import Uploader

MAX_VIDEO_SIZE = 1024 * 1024 * 512  # = 512MB
MAX_PREVIEW_SIZE = 1024 * 1024 * 5  # = 5MB

MAX_VIDEO_SIZE_PREMIUM = MAX_VIDEO_SIZE * 2 # = 1GB
MAX_PREVIEW_SIZE_PREMIUM = MAX_PREVIEW_SIZE * 2 # = 10MB


class VideoTypeException(Exception):
    pass


class MaxBodySizeException(Exception):
    pass


class VideoTarget(BaseTarget):

    def __init__(self, *args, bucket, pre_key):
        super().__init__(*args)
        self.uploader = Uploader(bucket=bucket)
        self.raised_exception = False
        self.chunks = []
        self.extension = None
        self.key = pre_key

    def data_received(self, chunk: bytes):
        self._validate(chunk)
        # Здесь нужна кастомная дополнительная проверка файла(форматы и всё такое)
        self.set_video_file()
        if self.extension is not None:
            self.uploader.key = self.key

        asyncio.run(self.uploader.upload_chunk(chunk))

    def set_video_file(self):
        if not self.raised_exception and self.multipart_content_type is not None and self.extension is None:
            video_type, video_extension = self.multipart_content_type.split('/')
            if video_type != 'video' or video_extension not in ['mp4', 'ogg', 'webm']:
                self.raised_exception = True
                raise VideoTypeException()
            else:
                self.extension = video_extension
                self.key = f'{self.key}.{self.extension}'

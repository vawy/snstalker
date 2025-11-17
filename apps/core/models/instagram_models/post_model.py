from django.db import models

from apps.core.common.mixins import TimestampMixin
from apps.core.common.constants import (
    INSTAGRAM_LOCAL_PATH_MAX_LEN,
    MEDIA_TYPES,
    MEDIA_TYPE_MAX_LEN,
    SHOTCODE_MAX_LEN,
    INSTAGRAM_URL_MAX_LEN
)
from profile_model import InstagramProfile


class InstagramPost(TimestampMixin):
    """
    Represents a single Instagram post (photo/video/carousel).

    Fields:
    - profile: Foreign key to InstagramProfile. Links the post to its owner.
    - shortcode: Unique identifier from Instagram URL (e.g., 'B1a2b3c4d5e'). Part of 'instagram.com/p/SHORTCODE/'.
    - caption: Post caption/text. May be empty.
    - media_url: Original media URL from Instagram (e.g., image or video).
    - media_local_path: Local file path or S3 key where media is stored after download.
    - media_type: Type of media ('image', 'video', 'carousel').
    - likes_count: Number of likes (maybe 0 if not scraped).
    - comments_count: Number of comments (maybe 0 if not scraped).
    - taken_at: When the post was originally created/uploaded by the user on Instagram.
    """
    profile = models.ForeignKey(InstagramProfile, on_delete=models.CASCADE, related_name="posts")
    shortcode = models.CharField(
        max_length=SHOTCODE_MAX_LEN, unique=True, help_text="Part of URL: instagram.com/p/SHORTCODE/"
    )
    caption = models.TextField(blank=True)
    media_url = models.URLField(max_length=INSTAGRAM_URL_MAX_LEN)
    media_local_path = models.CharField(max_length=INSTAGRAM_LOCAL_PATH_MAX_LEN, blank=True)
    media_type = models.CharField(max_length=MEDIA_TYPE_MAX_LEN, choices=MEDIA_TYPES, default="image")
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    taken_at = models.DateTimeField()

    def __str__(self):
        return f"Post {self.shortcode} (Profile ID: {self.profile_id})"

    class Meta:
        db_table = "instagram_post"
        ordering = ["-taken_at"]
        indexes = [models.Index(fields=["profile", "-taken_at"]),]

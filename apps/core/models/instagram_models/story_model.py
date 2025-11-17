from django.db import models

from apps.core.common.mixins import TimestampMixin
from apps.core.common.constants import (
    MEDIA_TYPES,
    MEDIA_TYPE_MAX_LEN,
    INSTAGRAM_URL_MAX_LEN,
    INSTAGRAM_LOCAL_PATH_MAX_LEN,
    STORY_ID_MAX_LEN
)
from profile_model import InstagramProfile


class InstagramStory(TimestampMixin):
    """
    Represents a temporary Instagram story (visible for 24 hours).

    Fields:
    - profile: Foreign key to InstagramProfile.
    - story_id: Unique ID of the story from Instagram.
    - media_url: Original media URL from Instagram.
    - media_local_path: Local path or S3 key for stored media.
    - media_type: Type of media ('image', 'video').
    - taken_at: When the story was originally created/uploaded by the user on Instagram.
    """
    profile = models.ForeignKey(InstagramProfile, on_delete=models.CASCADE, related_name="stories")
    story_id = models.CharField(max_length=STORY_ID_MAX_LEN, unique=True)
    media_url = models.URLField(max_length=INSTAGRAM_URL_MAX_LEN)
    media_local_path = models.CharField(max_length=INSTAGRAM_LOCAL_PATH_MAX_LEN, blank=True)
    media_type = models.CharField(max_length=MEDIA_TYPE_MAX_LEN, choices=MEDIA_TYPES, default="image")
    expires_at = models.DateTimeField(db_index=True)
    taken_at = models.DateTimeField()

    def __str__(self):
        return f"Story {self.story_id} (Profile ID: {self.profile_id})"

    class Meta:
        db_table = "instagram_story"
        ordering = ["-taken_at"]
        indexes = [models.Index(fields=["profile", "-taken_at"]), models.Index(fields=["expires_at"]),]

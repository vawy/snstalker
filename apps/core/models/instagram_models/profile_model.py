from django.db import models

from apps.core.common.mixins import TimestampMixin
from apps.core.common.constants import (
    INSTAGRAM_USERNAME_MAX_LEN,
    INSTAGRAM_URL_MAX_LEN,
    INSTAGRAM_LOCAL_PATH_MAX_LEN,
    INSTAGRAM_FULL_NAME_MAX_LEN,
    INSTAGRAM_BIOGRAPHY_MAX_LEN,
)


class InstagramProfile(TimestampMixin):
    """
    Represents an Instagram profile with basic metadata and scraping info.

    Fields:
    - username: Unique Instagram handle (e.g., 'elonmusk'). Used as identifier.
    - current_username: Actual username, in case it was changed after scraping.
    - full_name: Display name of the user.
    - biography: User's bio/description.
    - avatar_url: Original avatar URL from Instagram.
    - avatar_local_path: Local path or S3 key for stored avatar.
    - is_private: Whether the account is private.
    - is_verified: Whether the account is verified.
    - followers_count: Number of followers.
    - following_count: Number of accounts followed.
    - posts_count: Number of posts.
    - last_scraped_at: When the profile was last scraped.
    """
    username = models.CharField(max_length=INSTAGRAM_USERNAME_MAX_LEN, unique=True, db_index=True)
    current_username = models.CharField(max_length=INSTAGRAM_USERNAME_MAX_LEN, blank=True, db_index=True)
    full_name = models.CharField(max_length=INSTAGRAM_FULL_NAME_MAX_LEN, blank=True)
    biography = models.TextField(max_length=INSTAGRAM_BIOGRAPHY_MAX_LEN, blank=True)
    avatar_url = models.URLField(max_length=INSTAGRAM_URL_MAX_LEN, blank=True)
    avatar_local_path = models.CharField(max_length=INSTAGRAM_LOCAL_PATH_MAX_LEN, blank=True)
    is_private = models.BooleanField(default=False, db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    last_scraped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"@{self.username}"

    class Meta:
        db_table = "instagram_profile"
        verbose_name = "Instagram Profile"
        verbose_name_plural = "Instagram Profiles"

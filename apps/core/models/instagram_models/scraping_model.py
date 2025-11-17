from django.db import models

from apps.core.common.mixins import TimestampMixin
from apps.core.common.constants import TASK_STATUS_CHOICES, INSTAGRAM_USERNAME_MAX_LEN, SCRAPING_TASK_STATUS_MAX_LEN
from profile_model import InstagramProfile


class InstagramScrapingTask(TimestampMixin):
    """
    Represents a background task for scraping an Instagram profile.

    Used for:
    - Tracking async scraping initiated via Celery,
    - Monitoring task status (success/error/private account),
    - Logging errors and auditing requests,
    - Allowing retries on failure.

    Status examples:
    - pending: Task is queued,
    - started: Task is running,
    - success: Task completed successfully,
    - failed: An error occurred,
    - private: Account is private.
    """
    username = models.CharField(max_length=INSTAGRAM_USERNAME_MAX_LEN)
    status = models.CharField(max_length=SCRAPING_TASK_STATUS_MAX_LEN, choices=TASK_STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)
    result_profile_id = models.ForeignKey(InstagramProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Task for @{self.username} ({self.status})"

    class Meta:
        db_table = "instagram_scraping_task"

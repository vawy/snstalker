from django.db import models


class TimestampMixin(models.Model):
    """
    Abstract model for adding created_at and updated_at to all models.

    Fields:
    - created_at: When the post was first added to our system.
    - updated_at: When the post record was last updated in our system.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

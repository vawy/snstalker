MEDIA_TYPES = [
    ("image", "Image"),
    ("video", "Video"),
    ("carousel", "Carousel"),
]
MEDIA_TYPE_MAX_LEN = 10

TASK_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("started", "Started"),
    ("success", "Success"),
    ("failed", "Failed"),
    ("private", "Private Account"),
]

SCRAPING_SOURCE_CHOICES = [
    ("mobile_api", "Mobile API"),
    ("playwright", "Playwright"),
    ("mock", "Mock Data"),
]

INSTAGRAM_USERNAME_MAX_LEN = 30
INSTAGRAM_URL_MAX_LEN = 500
INSTAGRAM_LOCAL_PATH_MAX_LEN = 255
INSTAGRAM_FULL_NAME_MAX_LEN = 100
INSTAGRAM_BIOGRAPHY_MAX_LEN = 100
SHOTCODE_MAX_LEN = 20
STORY_ID_MAX_LEN = 50
SCRAPING_TASK_STATUS_MAX_LEN = 20

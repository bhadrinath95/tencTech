from django.contrib import admin
from .models import Post

class Post_Admin(admin.ModelAdmin):
    list_display = [
        "user", "title", "slug", "media_url", "media_type",
        "content", "get_intended_users", "is_html", "draft",
        "publish", "read_time", "updated", "timestamp"
    ]

    # Show the intended_users field in the admin form
    filter_horizontal = ("intended_users",)   # OR filter_vertical = ("intended_users",)

    def get_intended_users(self, obj):
        return ", ".join([user.username for user in obj.intended_users.all()])
    get_intended_users.short_description = "Intended Users"  # sets column header

    class Meta:
        model = Post

admin.site.register(Post, Post_Admin)
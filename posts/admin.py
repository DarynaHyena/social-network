from django.contrib import admin
from posts.models import Posts, Comment, Like, Share

admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
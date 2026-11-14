from django.contrib import admin
from communities.models import Community, CommunityMembership

admin.site.register(Community)
admin.site.register(CommunityMembership)
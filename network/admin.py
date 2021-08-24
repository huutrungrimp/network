from django.contrib import admin
from .models import User, Post, Comment, Friendship, Liking


admin.site.register(Comment)
#admin.site.register(Friendship)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'title', 'content', 'date_created')

admin.site.register(Post, PostAdmin)

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'leaders', 'followers')

admin.site.register(Friendship, FriendshipAdmin)


class LikingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'preference', 'bywhom')

admin.site.register(Liking, LikingAdmin)
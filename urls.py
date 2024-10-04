from django.urls import path
from mysite import settings
from personalblog import views

from django.conf.urls.static import static

urlpatterns = [
    # path("",views.index,name="posts"),
    path("login/",views.logins,name="login"),
    path("logout/",views.logouts,name="logouts"),
    path("signUp/",views.signUp,name="signUp"),
    path("profile/<str:username>/",views.showProfile,name="profile"),
    path("posts/",views.showPosts,name="posts"),
    path("editProfile/",views.editProfile,name="editProfile"),
    path("editPost/<int:blogId>/",views.editPosts,name="editPost"),
    path("users/",views.displayUsers,name="users"),
    path("users/<int:userId>/",views.banUser,name="perms")


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
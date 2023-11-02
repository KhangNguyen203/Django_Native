from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from .admin import admin_site


router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lessons', views.LessonViewSet)
router.register('users', views.UserViewSet)
# /courses/ - GET
# /courses/ - POST
# /courses/{course_id} - GET
# /courses/{course_id} - PUT
# /courses/{course_id} - DELETE

urlpatterns = [
    path('', include(router.urls)),
    # path('welcome/<int:year>/', views.welcome, name="welcome"),
    # path('test/', views.TestView.as_view()),
    # path('admin/', admin_site.urls)
]

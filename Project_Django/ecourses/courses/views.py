from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Course, Lesson, User
from .serializers import CourseSerializer, LessonSerializer, UserSerializer
from django.http import HttpResponse
from django.views import View


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,  #Hiện list users
                  generics.CreateAPIView,  #Hiện thực api create
                  generics.RetrieveAPIView):  #Hiện thực api lấy user
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return [permissions.IsAuthenticated()]
    #
    #     return [permissions.AllowAny()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    # Khi khai báo 2 dòng trên đã tạo được 5 APIs
    # list (GET) --> Xem danh sách Course
    # ... (POST) --> Thêm Course
    # detail --> Xem chi tiết 1 Course
    # ... (PUT) --> Cập nhật Course
    # ... (DELETE) --> Xóa 1 Course
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]  # permissions.AllowAny --> luôn được truy vấn
    #
    #     return [permissions.IsAuthenticated()]  # permissions.IsAuthenticated --> phải ở trạng thái user đang đăng nhập mới được truy vấn


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer

    @action(methods=['post'], detail=True,
            url_path="hide-lesson", url_name="hide-lessons")
    # /lesson/{pk}/hide-lesson
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l, context={'request': request}).data,
                        status=status.HTTP_200_OK)


def index(request):
    # return HttpResponse("hello world!!")

    return render(request, template_name='index.html', context={
        'name': 'Khang nguyễn'
    })


# def welcome(request, year):
#     return HttpResponse("Hello my friend " + str(year))


# class TestView(View):
#
#     def get(self, request):
#         return HttpResponse("Test get")
#
#     def post(self, request):
#         pass

from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from .models import Category, Course, Lesson, User
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.contrib.auth.models import Permission


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through


class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }

    form = LessonForm
    list_display = ["id", "subject", "created_date", "active", "course"]
    search_fields = ["subject", "created_date", "course__subject"]
    list_filter = ["subject", "course__subject"]
    readonly_fields = ["avatar"]
    inlines = (LessonTagInline, )

    def avatar(self, Lesson):
        img_url = Lesson.image.name
        alt = Lesson.subject
        return mark_safe(f"<img src='/static/{img_url}' alt='{alt}' width = '120px' />")


class LessionInline(admin.StackedInline):
    model = Lesson
    pk_name = 'course'


class CoureAdmin(admin.ModelAdmin):
    inlines = (LessionInline, )


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'He thong quan ly khoa hoc'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count=Count('lessons')).values("id", "subject", "lesson_count")

        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })


# admin_site = CourseAppAdminSite('mycourse')


# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Course, CoureAdmin)
admin.site.register(Lesson, LessonAdmin)

# admin_site.register(Category)
# admin_site.register(Course, CoureAdmin)
# admin_site.register(Lesson, LessonAdmin)

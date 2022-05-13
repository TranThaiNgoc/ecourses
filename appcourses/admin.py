from django.contrib import admin
from .models import Category, Lesson, Course, Tag
from django.utils.safestring import mark_safe
# Register your models here.

class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ['/static/css/main.css']
        }
    # quản lý các data bằng cách truyền các tham số quan option (list_display, list_filter, search_fields)
    list_display = ['subject', 'created_date', 'active', 'courses']
    search_fields  = ['subject', 'created_date', 'courses__subject']
    list_filter = ['subject', 'courses__subject']
    readonly_fields = ['avatar']
    inlines = [LessonTagInline]

    def avatar(self, lesson):
        return mark_safe("<img src='{img_url}' alt='{alt}' width='400px'/>".format(img_url=lesson.image, alt=lesson.subject))

class LessonInline(admin.StackedInline):
    model = Lesson
    pk_name = 'courses'

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

admin.site.register(Category)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)


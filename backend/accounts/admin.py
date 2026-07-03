from django.contrib import admin
from .models import InstagramAccount, CleaningTask, DeletedContent, ScheduledCleanup

@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'follower_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'instagram_id')
    readonly_fields = ('instagram_id', 'created_at', 'updated_at', 'last_synced')

@admin.register(CleaningTask)
class CleaningTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'task_type', 'status', 'progress_percentage', 'created_at')
    list_filter = ('status', 'task_type', 'created_at')
    search_fields = ('account__username',)
    readonly_fields = ('created_at', 'updated_at', 'start_time', 'end_time')

@admin.register(DeletedContent)
class DeletedContentAdmin(admin.ModelAdmin):
    list_display = ('account', 'content_type', 'instagram_id', 'deleted_at')
    list_filter = ('content_type', 'deleted_at')
    search_fields = ('account__username', 'instagram_id')
    readonly_fields = ('deleted_at',)

@admin.register(ScheduledCleanup)
class ScheduledCleanupAdmin(admin.ModelAdmin):
    list_display = ('account', 'cleanup_type', 'frequency', 'is_active', 'next_run')
    list_filter = ('is_active', 'frequency', 'created_at')
    search_fields = ('account__username',)
    readonly_fields = ('last_run', 'created_at', 'updated_at')

from django.contrib import admin

from .models import Entry, Topic


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0
    fields = ('text', 'date_added')
    readonly_fields = ('date_added',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'date_added')
    list_filter = ('owner', 'date_added')
    search_fields = ('text', 'owner__username')
    date_hierarchy = 'date_added'
    inlines = [EntryInline]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'topic', 'date_added')
    list_filter = ('topic', 'date_added')
    search_fields = ('text', 'topic__text')
    list_select_related = ('topic',)

    @admin.display(description='Text')
    def short_text(self, obj):
        return obj.text[:50]

from django.contrib import admin
from .models import ClaimRequest, Item


admin.site.site_header = 'Admin Dashboard'
admin.site.site_title = 'Admin Dashboard'
admin.site.index_title = 'Admin Dashboard'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = (
		'title',
		'category',
		'location_found',
		'date_found',
		'status',
		'created_at',
	)
	list_filter = ('status', 'category', 'date_found')
	search_fields = ('title', 'description', 'location_found', 'submitted_by_name')
	readonly_fields = ('created_at', 'updated_at')
	actions = ('approve_items', 'reject_items', 'mark_claimed')

	@admin.action(description='Approve selected items')
	def approve_items(self, request, queryset):
		queryset.update(status='approved')

	@admin.action(description='Reject selected items')
	def reject_items(self, request, queryset):
		queryset.update(status='rejected')

	@admin.action(description='Mark selected items as claimed')
	def mark_claimed(self, request, queryset):
		queryset.update(status='claimed')


@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
	list_display = ('item', 'claimant_name', 'claimant_email', 'status', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('item__title', 'claimant_name', 'claimant_email')
	readonly_fields = ('created_at', 'updated_at')
	actions = ('approve_claims', 'reject_claims', 'mark_reviewed')

	@admin.action(description='Approve selected claims')
	def approve_claims(self, request, queryset):
		queryset.update(status='approved')

	@admin.action(description='Reject selected claims')
	def reject_claims(self, request, queryset):
		queryset.update(status='rejected')

	@admin.action(description='Mark selected claims as reviewed')
	def mark_reviewed(self, request, queryset):
		queryset.update(status='reviewed')

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ClaimRequestForm, ItemSubmissionForm
from .models import ClaimRequest, Item


def home(request):
	recent_items = Item.objects.filter(status='approved')[:6]
	context = {
		'recent_items': recent_items,
		'approved_count': Item.objects.filter(status='approved').count(),
		'claimed_count': Item.objects.filter(status='claimed').count(),
		'pending_count': Item.objects.filter(status='pending').count(),
	}
	return render(request, 'lostfound/home.html', context)


def report_item(request):
	if request.method == 'POST':
		form = ItemSubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(
				request,
				'Thanks for reporting the item. It has been submitted for review.',
			)
			return redirect('report_item')
	else:
		form = ItemSubmissionForm()

	return render(request, 'lostfound/report_item.html', {'form': form})


def found_items(request):
	query = request.GET.get('q', '').strip()
	category = request.GET.get('category', '').strip()
	date_from = request.GET.get('date_from', '').strip()
	date_to = request.GET.get('date_to', '').strip()
	items = Item.objects.filter(status__in=['approved', 'claimed']).order_by('-date_found', '-created_at')

	if query:
		items = items.filter(
			Q(title__icontains=query)
			| Q(description__icontains=query)
			| Q(location_found__icontains=query)
		)

	if category:
		items = items.filter(category=category)

	if date_from:
		items = items.filter(date_found__gte=date_from)

	if date_to:
		items = items.filter(date_found__lte=date_to)

	context = {
		'items': items,
		'query': query,
		'category': category,
		'date_from': date_from,
		'date_to': date_to,
		'category_choices': Item.CATEGORY_CHOICES,
	}
	return render(request, 'lostfound/found_items.html', context)


def item_detail(request, item_id):
	item = get_object_or_404(Item, id=item_id)
	if not request.user.is_staff and item.status not in {'approved', 'claimed'}:
		return HttpResponseForbidden('This item is not available for public viewing.')
	return render(request, 'lostfound/item_detail.html', {'item': item})


def claim_item(request, item_id):
	item = get_object_or_404(Item, id=item_id, status='approved')

	if request.method == 'POST':
		form = ClaimRequestForm(request.POST)
		if form.is_valid():
			claim = form.save(commit=False)
			claim.item = item
			claim.save()
			messages.success(
				request,
				'Your claim request was submitted. A staff member will review it soon.',
			)
			return redirect('item_detail', item_id=item.id)
	else:
		form = ClaimRequestForm()

	return render(
		request,
		'lostfound/claim_item.html',
		{
			'item': item,
			'form': form,
		},
	)


@staff_member_required
def moderation_dashboard(request):
	pending_items = Item.objects.filter(status='pending')
	pending_claims = ClaimRequest.objects.filter(status='pending')
	return render(
		request,
		'lostfound/moderation_dashboard.html',
		{
			'pending_items': pending_items,
			'pending_claims': pending_claims,
		},
	)


@require_POST
@staff_member_required
def moderate_item(request, item_id):
	action = request.POST.get('action')
	item = get_object_or_404(Item, id=item_id)

	if action not in {'approve', 'reject', 'claim'}:
		return HttpResponseForbidden('Invalid action')

	if action == 'approve':
		item.status = 'approved'
	elif action == 'reject':
		item.status = 'rejected'
	else:
		item.status = 'claimed'

	item.admin_notes = request.POST.get('admin_notes', '').strip()
	item.save()
	messages.success(request, f'Item "{item.title}" updated to {item.get_status_display()}.')
	return redirect('moderation_dashboard')


@require_POST
@staff_member_required
def moderate_claim(request, claim_id):
	action = request.POST.get('action')
	claim = get_object_or_404(ClaimRequest, id=claim_id)

	if action not in {'approve', 'reject', 'review'}:
		return HttpResponseForbidden('Invalid action')

	if action == 'approve':
		claim.status = 'approved'
		claim.item.status = 'claimed'
		claim.item.save()
	elif action == 'reject':
		claim.status = 'rejected'
	else:
		claim.status = 'reviewed'

	claim.save()
	messages.success(request, f'Claim by {claim.claimant_name} updated successfully.')
	return redirect('moderation_dashboard')

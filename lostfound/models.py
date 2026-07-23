from django.db import models


class Item(models.Model):
	CATEGORY_CHOICES = [
		('electronics', 'Electronics'),
		('school', 'School Supplies'),
		('clothing', 'Clothing'),
		('sports', 'Sports Gear'),
		('accessories', 'Accessories'),
		('other', 'Other'),
	]

	STATUS_CHOICES = [
		('pending', 'Pending Review'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
		('claimed', 'Claimed'),
	]

	title = models.CharField(max_length=120)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
	description = models.TextField()
	location_found = models.CharField(max_length=120)
	date_found = models.DateField()
	image = models.ImageField(upload_to='item_photos/', blank=True, null=True)
	submitted_by_name = models.CharField(max_length=100)
	submitted_by_email = models.EmailField()
	submitted_by_phone = models.CharField(max_length=25, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	admin_notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.title} ({self.get_status_display()})'


class ClaimRequest(models.Model):
	CLAIM_STATUS_CHOICES = [
		('pending', 'Pending Review'),
		('reviewed', 'Reviewed'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
	]

	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
	claimant_name = models.CharField(max_length=100)
	claimant_email = models.EmailField()
	claimant_phone = models.CharField(max_length=25, blank=True)
	proof_of_ownership = models.TextField()
	additional_message = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'Claim by {self.claimant_name} for {self.item.title}'

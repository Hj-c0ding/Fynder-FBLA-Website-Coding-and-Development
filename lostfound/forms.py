from django import forms

from .models import ClaimRequest, Item


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs.setdefault('class', css_class)
            if name == 'image':
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = [
            'title',
            'category',
            'description',
            'location_found',
            'date_found',
            'image',
            'submitted_by_name',
            'submitted_by_email',
            'submitted_by_phone',
        ]
        widgets = {
            'date_found': DateInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ClaimRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    class Meta:
        model = ClaimRequest
        fields = [
            'claimant_name',
            'claimant_email',
            'claimant_phone',
            'proof_of_ownership',
            'additional_message',
        ]
        widgets = {
            'proof_of_ownership': forms.Textarea(attrs={'rows': 4}),
            'additional_message': forms.Textarea(attrs={'rows': 3}),
        }

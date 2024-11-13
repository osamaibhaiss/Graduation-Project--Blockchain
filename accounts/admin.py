from django.contrib import admin
from .models import Profile
from .forms import ProfileForm
from voting.models import Voter  # Import the Voter model

# Prevent Profile from being registered more than once
try:
    admin.site.unregister(Profile)
except admin.sites.NotRegistered:
    pass

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm  # Use the ProfileForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Pre-populate the form when adding a new profile for a Voter
        if obj is None:  # Only pre-populate when creating a new profile
            voter_id = request.GET.get('voter_id')  # Pass the voter_id in the URL
            if voter_id:
                try:
                    voter_instance = Voter.objects.get(id=voter_id)
                    form.base_fields['phone_number'].initial = voter_instance.phone_number
                    form.base_fields['address'].initial = voter_instance.address
                    form.base_fields['second_name'].initial = voter_instance.second_name
                    form.base_fields['third_name'].initial = voter_instance.third_name
                    form.base_fields['identity_card_number'].initial = voter_instance.identity_card_number
                    form.base_fields['date_of_birth'].initial = voter_instance.date_of_birth
                except Voter.DoesNotExist:
                    pass  # Handle case where Voter does not exist
        return form

# Register Profile model with ProfileAdmin class
admin.site.register(Profile, ProfileAdmin)

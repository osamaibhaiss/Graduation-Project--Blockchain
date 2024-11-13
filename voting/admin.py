from django.contrib import admin
from .models import Voter, Login, Group, Result, Election, Vote  # Import all your models

# Register the Login model
admin.site.register(Login)

# Register the Group model
admin.site.register(Group)

# Register the Result model
admin.site.register(Result)

# Register the Election model
admin.site.register(Election)

# Register the Vote model
admin.site.register(Vote)

# Custom admin class for the Voter model
from django.contrib import admin
from .models import Voter
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Voter
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import admin
from .models import Voter
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import admin
from .models import Voter
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import admin
from .models import Voter, Login, Group, Result, Election
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Voter, Login, Group, Result, Election
from django.contrib.auth.models import User

class VoterAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view of the admin
    list_display = [
        'id', 
        'identity_card_number', 
        'get_username', 
        'get_email', 
        'phone_number', 
        'first_name', 
        'second_name', 
        'third_name', 
        'last_name', 
        'password_display'
    ]
    
    # Add a search field for identity card number
    search_fields = ['identity_card_number']
    
    # You can also add a custom filter or other features
    list_filter = ['identity_card_number']
    
    
    def get_username(self, obj):
        return obj.user.username  # Get the username from the related user model
    get_username.short_description = 'Username'  # Optionally, you can set a custom label


    def get_email(self, obj):
        """Get the email from the User model."""
        return obj.user.email if obj.user else 'No Email'
    get_email.short_description = 'Email'

    def password_display(self, obj):
        """Display a masked password for the admin interface."""
        return "********"  # Masked password for security
    password_display.short_description = "Password"

    def save_model(self, request, obj, form, change):
        """This method is called when saving the model in the admin."""
        if not obj.pk:  # New Voter being added
            # Create a User for the new Voter
            username = f"voter_{Voter.generate_random_string()}"
            password = Voter.generate_random_string()  # Random password
            
            # Create User and set the password
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",  # Placeholder email
                password=password
            )
            
            # Set the User object on the Voter model
            obj.user = user  # This assumes that you have a `user` field in the Voter model.
        
        # Ensure that the password is set securely when saving
        if obj.user and obj.user.password != password:  # Only hash the password if it's new
            obj.user.set_password(obj.user.password)
        
        super().save_model(request, obj, form, change)

admin.site.register(Voter, VoterAdmin)

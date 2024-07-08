from dj_rest_auth.serializers import PasswordResetSerializer, serializers

from apps.user.models import UserAccount

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        # Add custom validation logic for the email field if needed
        return value
    
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        if not UserAccount().objects.filter(email=value).exists():
            raise serializers. ValidationError(('Invalid e-mail address'))
        return value

    def save(self):
        # Implement custom save logic if needed
        super().save()

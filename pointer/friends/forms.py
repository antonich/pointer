from django import forms

from .models import Friendship

class FriendshipForm(forms.ModelForm):

    class Meta:
        model = Friendship
        fields = ('from_user', 'to_user',)

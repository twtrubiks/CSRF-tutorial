from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        max_length=20
    )

    text = forms.CharField(
        required=True,
        max_length=200
    )

    class Meta:
        model = Comment
        fields = ('name', 'text')

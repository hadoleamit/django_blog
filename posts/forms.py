from django import forms
from .models import Post, Comment, Author

class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model= Post
        fields=[
            "title",
            'image',
            "content",
            "draft",
            "publish",
            
        ]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('content',)

class AuthorForms(forms.ModelForm):
    class Meta:
        model = Author
        
        fields =[
            "user",
            "mobile_no",
            "address", 
            "date_of_birth",  
        ] 
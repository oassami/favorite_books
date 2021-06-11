from django.db import models

from login_app.models import User

class BookManager(models.Manager):
    def addValidation(self, post_data):
        errors={}
        if not post_data['title']:
            errors['title'] = 'Title is required.'
        if len(post_data['description']) < 5:
            errors['description'] = 'Description must be at least 5 characters'
        try:
            self.get(title=post_data['title'])
            errors['title'] = "This title already exists!"
        except:
            pass
        return errors

    def updateValidation(self, post_data):
        errors={}
        if not post_data['title']:
            errors['title'] = 'Title is required.'
        if len(post_data['description']) < 5:
            errors['description'] = 'Description must be at least 5 characters'
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name='like_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


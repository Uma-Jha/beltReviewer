from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re, datetime

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = []
        try:
            user = self.get(email=postData['email'])
        except:
            user = None
        if user:
            errors.append("This email is already registered. Please use other")
        if len(postData['name']) < 2:
            errors.append("Name should be more than 1 character")
        elif not postData['name'].isalpha():
            errors.append("Name should only contain characters")
        if len(postData['alias']) < 2:
            errors.append("Alias should be more than 1 character")
        elif not postData['alias'].isalpha():
            errors.append("Alias should only contain characters")
        if len(postData['email']) < 1:
            errors.append("Email should not be blank")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Email is not valid!")
        if len(postData['pwd']) < 8:
            errors.append("Password should be at least 8 characters")
        if len(postData['confirmPwd']) < 8 or postData['pwd']!=postData['confirmPwd']:
            errors.append("Password and Confirm Password should match")
        if errors:
            return (False, errors)  
        else:
            hashPwd = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            user = self.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashPwd)
            return (True, user)

    def validate_login(self, postData):
        errors = []
        if len(postData['email'])==0 or len(postData['pwd'])==0:
            errors.append("Username or password cannot be blank")
            return(False, errors)
        try:
            user = self.get(email=postData['email'])
        except:
            user = None
        if user and bcrypt.hashpw(postData['pwd'].encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            return (True, user)
        errors.append("Invalid login. Email or password is incorrect")
        return(False, errors)

class BookManager(models.Manager):
    def createBook(self, userid, postData):
        if len(postData['addAuthor']) > 0:
            author = postData['addAuthor']
        else:
            author = postData['author']
        book = self.create(title=postData['title'], author=author, rating=int(postData['rating']))
        if(postData['review']):
            review = Review.objects.create(content=postData['review'], user=User.objects.get(id=userid), book=book)
        return book
        

class ReviewManager(models.Manager):
    def getReview(self):
        review_cnt = self.count()
        if(review_cnt>3):
            new_reviews = self.order_by('-created_at')[:3]
            no = Review.objects.count() - 3
            old_reviews = self.order_by('created_at')[:no]
            return(new_reviews, old_reviews)
        else:
            new_reviews = self.order_by('-created_at')
            return(new_reviews, [])
    def bookReview(self, userid, no, data):
        review = self.create(content=data['review'], user=User.objects.get(id=userid), book=Book.objects.get(id=no))
        return review

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=70)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="reviewed_by", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviewed_for", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()






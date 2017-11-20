from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from datetime import datetime, date
import bcrypt
from django.contrib import messages

def index(request):
	if 'userid' not in request.session:
		request.session['logged'] = False
	return render(request, 'exam/index.html')

def register(request):
		result = User.objects.validate_register(request.POST)
		if not result[0]:
			for m in result[1]:
				messages.warning(request, m)
			return render(request, 'exam/index.html')
		else:
			request.session['userid'] = result[1].id
			request.session['logged'] = True
        	return redirect('/books')

def login(request):
	result = User.objects.validate_login(request.POST)
	if not result[0]:
		for m in result[1]:
			messages.warning(request, m)
		return render(request, 'exam/index.html')
	else:
		request.session['userid'] = result[1].id
		request.session['logged'] = True
        return redirect('/books')

def books(request):
	res = Review.objects.getReview()
	context = {}
   	context['reviews'] = res[1]
   	request.session['name'] = User.objects.get(id=request.session['userid']).name
   	context['new_reviews'] = res[0]
   	return render(request, 'exam/dashboard.html', context)

def logout(request):
	request.session['userid'] = 0
	request.session['name'] = ''
	return redirect('/')

def addBooks(request):
	return render(request, 'exam/addBook.html')

def create(request):
	book = Book.objects.createBook(request.session['userid'], request.POST)
	return redirect('/books/'+str(book.id))

def showBook(request, no):
	reviews = Review.objects.filter(book=Book.objects.get(id=no)).all()
	context = {
	'book' : Book.objects.get(id=no),
	'reviews': reviews
	}
	return render(request, 'exam/showBook.html', context)

def showUser(request, id):
	review_cnt = Review.objects.filter(user=User.objects.get(id=id)).count()
	books_reviewed = Review.objects.filter(user=User.objects.get(id=7)).all()
	context = {
	'user': User.objects.get(id=id),
	'review_cnt': review_cnt,
	'books_reviewed': books_reviewed
	}
	return render(request, 'exam/showUser.html', context)

def addReview(request):
	no = int(request.POST['book_id'])
	Review.objects.bookReview(request.session['userid'], no, request.POST)
	result = Review.objects.filter(book=Book.objects.get(id=no)).all()
	context = {
	'book' : Book.objects.get(id=no),
	'reviews':result
	}
	return render(request, 'exam/showBook.html', context)
	
	
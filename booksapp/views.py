from django.shortcuts import render, redirect
from .models import Book, Author, BorrowRequest
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import CreateBookForm
from datetime import datetime, timedelta
from .serializers import RequestSerializer, BookSerializer, AuthorSerializer
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions
from .filterusers import IsUserOrAdminFilter



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(book_title=serializer.validated_data['book_title'] + '!')

    def get_queryset(self):
        queryset = Book.objects.all()
        author_age = self.request.query_params.get('author_age')

        if author_age is not None:
            queryset = queryset.filter(book_authors__author_age__gte=author_age)
        return queryset




class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        books = Book.objects.filter(book_authors=instance)
        book_serializer = BookSerializer(books, many=True)

        data = serializer.data
        data['books'] = book_serializer.data

        return Response(data)


    def get_queryset(self):
        queryset = Author.objects.all()
        book_name = self.request.query_params.get('book_name')
        
        if book_name is not None:
            queryset = queryset.filter(book__book_title__icontains=book_name).distinct()
        
        return queryset


    @action(detail=True, methods=['GET'])
    def author_books(self, request, pk=None):
        author = self.get_object()
        books = Book.objects.filter(book_authors=author)
        books_data = [{'book_id': book.id,'book_title': book.book_title,} for book in books]
        return Response({'id': author.id, 'name': author.name_author, 'books': books_data})
   

class RequestViewSet(viewsets.ModelViewSet):
    queryset = BorrowRequest.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [filters.OrderingFilter, IsUserOrAdminFilter] 

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)

# class BookListView(ListView):
#     model = Book
#     template_name = 'book_list.html'
#     context_object_name = 'books'



# @method_decorator(login_required, name='dispatch')
# class BorrowListView(ListView):
#     model = BorrowRequest
#     template_name = 'borrow_list.html'
#     context_object_name = 'borrow_list'

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff or user.is_superuser:
#             return BorrowRequest.objects.all()
#         else:
#             return BorrowRequest.objects.filter(borrower=user)



# class BorrowRequestView(DetailView):
#     model = Book
#     template_name = 'borrow_request.html'
#     http_method_names = ['get', 'post']
#     context_object_name = 'book'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         try:
#             borrow_request = BorrowRequest.objects.filter(book=context['book'], borrower=context['user']).last()
#             context['borrow_request'] = borrow_request
#         except BorrowRequest.DoesNotExist:
#             context['borrow_request'] = None
#         return context

#     def post(self, request, *args, **kwargs):
#         try:
#             book = Book.objects.get(id=self.kwargs['pk'])
#             borrower = request.user
#             action = request.POST.get('action')

#             if action == 'request':
#                 book.is_available = False
#                 book.book_borrower = borrower
#                 book.save()
#                 BorrowRequest.objects.create(book=book, borrower=borrower, status=1)

#             elif action == 'collect':
#                 borrow_request = book.borrow_requests.filter(book=book, borrower=borrower).last()
#                 borrow_request.status = 3
#                 borrow_request.due_date = datetime.now().date() + timedelta(days=7)
#                 borrow_request.save()

#             elif action == 'return':
#                 book.book_borrower = None
#                 book.save()
#                 borrow_request = book.borrow_requests.filter(book=book, borrower=borrower).last()
#                 borrow_request.status = 4
#                 borrow_request.complete_date = datetime.now().date()
#                 borrow_request.save()

#             url = reverse('booksapp:home_page')
#             return HttpResponseRedirect(url)
#         except Book.DoesNotExist:
#             raise Http404('This book is not found')




# class CreateBookView(CreateView):
#     model = Book
#     form_class = CreateBookForm
#     template_name = 'book_create.html'  

#     def get_success_url(self):
#         return reverse('booksapp:home_page')


# class SearchResultsView(View):
#     template_name = 'search_results.html'

#     def get(self, request):
#         query = request.GET.get('query')
#         if query:
#             search_results = Book.objects.filter(book_title__icontains=query)
#         else:
#             search_results = []

#         print("Query:", query)
#         print("Search Results:", search_results)

#         context = {
#             'query': query,
#             'search_results': search_results,
#         }
#         return render(request, self.template_name, context)


# class DetailBookView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'
#     context_object_name = 'book'  
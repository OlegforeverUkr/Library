from rest_framework import serializers
from .models import Author, Book, UserModel, BorrowRequest



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class RequestSerializer(serializers.ModelSerializer):
    borrower = UserSerializer(read_only=True)

    class Meta:
        model = BorrowRequest
        fields = "__all__"



class BookSerializer(serializers.ModelSerializer):
    orders = RequestSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def validate_book_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Название книги должно содержать не менее 5 символов.")
        return value

    def validate_book_summary(self, value):
        if not value:
            raise serializers.ValidationError("Краткое описание книги не может быть пустым.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"


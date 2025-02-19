from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Professor, Module, Rating
from .serializer import StudentSerializer, ModuleSerializer, RatingSerializer
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from ratings.models import Student
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    RESTful login API that returns a JWT token.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = Student.objects.filter(username=username).first()

    if user is None or not check_password(password, user.password):
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "username": user.username
    }, status=status.HTTP_200_OK)

#, logging out does not actually delete a resource
#POST is used when modifying state on the server.
@api_view(['DELETE'])
@permission_classes([AllowAny])
def logout(request):
    """
    RESTful logout API that invalidates the refresh token.
    """
    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the refresh token (if using Django Rest Framework Simple JWT Blacklist)
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Secure registration API that accepts both JSON and form-encoded data.
    """

    # Accept data from both JSON and form submissions
    username = request.data.get("username") or request.POST.get("username")
    email = request.data.get("email") or request.POST.get("email")
    password = request.data.get("password") or request.POST.get("password")

    if not username or not email or not password:
        return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if Student.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
    if Student.objects.filter(email=email).exists():
        return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)

    # Create user
    student_data = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    serializer = StudentSerializer(data=student_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def modules(request):
    """
    Retrieve all modules with professor names included.
    """
    try:
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to retrieve modules: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([AllowAny])
def professor_ratings(request):
    professors = Professor.objects.all()
    ratings_summary = []

    for professor in professors:
        # Get all ratings for the current professor
        ratings = Rating.objects.filter(professor_id=professor.id)
        
        # Calculate the average rating (returns None if no ratings)
        avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        avg_rating_rounded = round(avg_rating) if avg_rating is not None else "No ratings yet"
        # Add the professor's rating summary to the list
        ratings_summary.append({
            "professor_id": professor.id,
            "professor_name": professor.name,
            "average_rating": avg_rating_rounded
        })

    return Response(ratings_summary, status=status.HTTP_200_OK)



 
@api_view(['GET'])
@permission_classes([AllowAny])
def professor_avg(request, professor_id, module_code):
    """
    Calculate and return the average rating of a professor for a given module.
    """
    try:
        
        professor = Professor.objects.filter(professor_id=professor_id).first()
        if not professor:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)

       
        modules = Module.objects.filter(module_code=module_code)
        if not modules.exists():
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

       
        avg_rating = Rating.objects.filter(professor=professor, module__in=modules).aggregate(Avg('rating'))['rating__avg']

        
        stars = "*" * int(round(avg_rating)) if avg_rating else "No ratings yet"

        
        response_data = {
            "name": professor.name,
            "professor_id": professor.professor_id,
            "module_name": modules.first().name,
            "average_rating_stars": stars
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def rating(request):
    """
    API to create a new rating for a professor in a specific module.
    """
    try:
        
        professor_id = request.data.get("professor_id")
        module_code = request.data.get("module_code")
        year = request.data.get("year")
        semester = request.data.get("semester")
        rating_value = request.data.get("rating")

        # Validate required fields
        if not all([professor_id, module_code, year, semester, rating_value]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        
        if not (1 <= int(rating_value) <= 5):
            return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        professor = Professor.objects.filter(professor_id=professor_id).first()
        if not professor:
            return Response({"error": "Professor not found."}, status=status.HTTP_404_NOT_FOUND)

        module = Module.objects.filter(module_code=module_code, year=year, semester=semester).first()
        if not module:
            return Response({"error": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

        rating_obj = Rating.objects.create(
            rating=rating_value,
            professor=professor,
            module=module
        )

        return Response({
            "message": "Rating submitted successfully!",
            "rating_id": rating_obj.rating_id,
            "professor": professor.name,
            "module": module.name,
            "rating": rating_obj.rating
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



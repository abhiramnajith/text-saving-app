from django.shortcuts import render
from django.contrib.auth import authenticate
from .decorators import tryexcept
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Snippet, Tag
from rest_framework import generics
from .serializers import SnippetSerializer, TagSerializer

# API for registering Users


@api_view(['POST'])
@tryexcept
def register(request):
    username = request.data['username']

    if User.objects.filter(username=username).exists():
        return Response({"app_data": "User with this Username already exist"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email']
    )
    return Response({'app_data': 'User Created'}, status=status.HTTP_200_OK)

# API for login


@api_view(['POST'])
@tryexcept
def login(request):
    user = authenticate(username=request.data['username'],
                        password=request.data['password'])
    if user is None:
        return Response({'app_data:Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)

    return Response(
        {'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK
    )

# API for getting access token with refresh token


@api_view(['POST'])
@tryexcept
def refresh_token(request):
    refresh_token = request.data['refresh_token']
    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
    except Exception as E:
        return Response({'app_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)

# API for listing Snippets with their count


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@tryexcept
def snippet_list(request):
    snippets = Snippet.objects.filter(active_status=True)
    serializer = SnippetSerializer(
        snippets, many=True, context={"request": request})
    return Response({"data": serializer.data,
                     "count": int(snippets.count())})

# API for getting Snippets details


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@tryexcept
def snippet_detail(request, pk):
    snippet = Snippet.objects.get(id=pk)
    serializer = SnippetSerializer(snippet, context={"request": request})
    return Response(serializer.data)

# API for Creating Snippets


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@tryexcept
def snippet_create(request):
    tag = request.data['tag']
    if Tag.objects.filter(title=tag).exists():
        tag = Tag.objects.get(title=tag)
    else:
        tag = Tag.objects.create(title=tag)

    request.data['tag'] = tag.id
    request.data['created_user'] = request.user.id

    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'app_data': 'Snippet Created'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API for updaing Snippet


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@tryexcept
def snippet_update(request, pk):
    try:
        snippet = Snippet.objects.get(id=pk)
    except Exception as E:
        return Response({'app_data': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)

    tag = request.data['tag']
    if snippet.tag != tag:
        if Tag.objects.filter(title=tag).exists():
            tag = Tag.objects.get(title=tag)
        else:
            tag = Tag.objects.create(title=tag)
    request.data['tag'] = tag.id
    request.data['created_user'] = request.user.id
    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'app_data': 'Snippet updated'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to delete Snippets


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@tryexcept
def delete_snippets(request):
    snippets_to_delete = request.data.get('delete_snippets', [])

    for id in snippets_to_delete:
        snippet = Snippet.objects.get(id=id)
        snippet.active_status = False
        snippet.save()

    snippets = Snippet.objects.filter(active_status=True)
    serializer = SnippetSerializer(snippets, many=True,context={"request":request})

    return Response(serializer.data, status=status.HTTP_200_OK)

# API to list Tag


class UserList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

# Tag Detail API


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@tryexcept
def tag_details(request, pk):
    snippets = Snippet.objects.filter(active_status=True, tag__id=pk)
    serializer = SnippetSerializer(snippets, many=True,context={"request":request})
    return Response(serializer.data)

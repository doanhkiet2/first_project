from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import Profile
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import get_user_model

User = get_user_model()


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


# @api_view(['GET'])
# @permission_classes([IsAuthenticated, ])
# def user_profile_detail_view(request, username, *args, **kwargs):
#     current_user = request.user
#     to_follow_user = ??
#     return Response({}, status=200)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, ])
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username) # find user i want follow

    # i don't want follow myself
    if me.username == username:
        my_follower = me.profile.followers.all()
        return Response({"count": my_follower.count()}, status=200)

    # query not found -> 404 or get profile from request user
    if not other_user_qs.exists():
        return Response({}, status=404)
    other = other_user_qs.first()
    profile = other.profile

    #  add or remove me to otheruser(i want follow)/// with context from react
    data = request.data or {}
    action = data.get("action")
    if action == "follow":
        profile.followers.add(me)
    elif action == "unfollow":
        profile.followers.remove(me)
    else:
        pass
    
    # done, get my follow and response
    current_follower_qs = profile.followers.all()
    return Response({"count": current_follower_qs.count()}, status=200)

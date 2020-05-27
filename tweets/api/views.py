from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from ..models import Tweet
from ..forms import TweetForm
from django.conf import settings

from ..serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # print(request.user)
        serializer.save(user=request.user)
        # print("--------------------------------------------------",
        #       serializer.data, "----------------------------------------")
        return Response(serializer.data, status=201)
        # return JsonResponse(serializer.data, status=201) #201 is created items

    return Response({}, status=400)
    # return JsonResponse({}, status=201) #201 is created items


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, ])
@permission_classes([IsAuthenticated, ])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    # print("\n__________\n",obj,"____________\n",qs,"\n___________\n")
    serializer = TweetSerializer(obj)
    # print("\n__________\n",serializer,"\n____________\n",serializer.data,"\n___________\n")
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated, ])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)

    if not qs.exists():
        return Response({"message": "you can't delete this tweet"}, status=401)

    obj = qs.first()
    obj.delete()
    return Response({"message": "tweet removed"}, status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is require
    Action options are: like, unlike, retweet

    '''

    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=obj,
                content=content,
            )
            serializer = TweetSerializer(new_tweet)
            # print(serializer.data)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 3
    paginated_qs = paginator.paginate_queryset(qs, request)
    print(paginated_qs)
    serializer = TweetSerializer(paginated_qs, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')  # ?username=Ak
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def tweet_feed_view(request, *args, **kwargs):
#     user = request.user
#     # 'following' is relation MaToMa profile.follow->User
#     profile = user.following.all()

#     # list-append all user i followed and append me
#     followed_users_id = []
#     if profile.exists():
#         followed_users_id = [x.user.id for x in profile]
#     followed_users_id.append(user.id)

#     #qs filter all tweet with list user i followed
#     qs = Tweet.objects.filter(
#         user__id__in=followed_users_id).order_by("-timestamp")

#     serializer = TweetSerializer(qs, many=True)
#     return Response(serializer.data, status=200)


# more efficient than above
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    # assumed i send this GET
    user = request.user
    qs = Tweet.objects.feed(user)  # def in model TweetQuerySet
    return get_paginated_queryset_response(qs, request)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    # print(user)
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        # print(obj)
        # do other form related logic
        obj.save()

        if request.is_ajax():
            # print(obj.tweet_serialize())
            # 201 is created items
            return JsonResponse(obj.tweet_serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()  # clear

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/form.html", context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or swift/java/ios/android
    return json data
    """
    qs = Tweet.objects.all()
    username = request.GET.get('username')  # ?username=Ak
    if username != None:
        qs.filter(user__username__iexact=username)
    tweet_list = [x.tweet_serialize() for x in qs]
    data = {
        "isUsed": False,
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    consume by javascript or swift/java/ios/android
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['massage'] = "Not found"
        # "image_path": obj.image.url
        status = 404
    # json dumps content_type = 'applicatons/json'
    return JsonResponse(data, status=status)

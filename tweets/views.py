from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Tweet
from .forms import TweetForm
from django.conf import settings


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def home_view2(request, *args, **kwargs):
    return render(request, "pages/home2.html", context={}, status=200)


def local_tweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")


def local_tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})




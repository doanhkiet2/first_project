from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet
from rest_framework.test import APIClient
# Create your tests here.
User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='abc', password='somepassword')
        self.userb = User.objects.create_user(
            username='abcb', password='somepassword')
        # User.objects.create_user(username='fgh', password= 'somepassword')
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my first twee2t", user=self.user)
        Tweet.objects.create(content="my first tweet3", user=self.user)
        Tweet.objects.create(content="my first tweet4", user=self.user)
        Tweet.objects.create(content="my first tweet5", user=self.user)
        Tweet.objects.create(content="my first tweet6", user=self.userb)
        self.currentCount = Tweet.objects.all().count()

    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    

    def test_user_created(self):
        self.assertEqual(self.user.username, "abc")
        # self.assertEqual(tweet.obj.user, self.user)

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(
            content="my second tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 7)
        self.assertEqual(tweet_obj.user, self.user)


    def test_tweets_related_name(self):
        user = self.user
        self.assertEqual(user.tweets.count(), 5)



    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)
        # print(response.json())

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        # self.assertEqual(len(response.json()), 4)
        # print(response.json())
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances_count = user.tweetlike_set.count()
        my_related_likes = user.tweet_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1, "like")
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_related_likes, my_like_instances_count)



    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)

        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.json()), 4)
        # print(response.json())
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0, "unlike")

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        print(data)

        self.assertNotEqual(new_tweet_id, 2)
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_create_api_viewt(self):
        request_data = {"contennt": "this is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail_api_viewt(self):
        client = self.get_client()
        response = client.get("/api/tweets/2/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        _id = response_data.get("id")
        self.assertEqual(_id, 2)

    def test_tweet_delete_api_viewt(self):
        client = self.get_client()
        response = client.post("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.post("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        client = self.get_client()
        response_incorrect_owner = client.post("/api/tweets/6/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)

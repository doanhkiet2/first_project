from django.http import Http404
from django.shortcuts import redirect, render
# Create your views here.

from .forms import ProfileForm
from .models import Profile


def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profiles/update")
   
    user = request.user
    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email' : user.email
    }
    my_profile = user.profile
    form = ProfileForm(request.POST or None, instance=my_profile, initial=user_data)
    if form.is_valid():
        profile_object = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_object.save()
    context = {
        "form": form,
        "btn_label": "Save",
        "title": "Update Profile"
    }
    return render(request, "profiles/form.html", context)

def profile_detail_view(request, username, *args, **kwargs):
    # get the profile for the passed username
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404
    profile_object = qs.first()
    context = {
        "profile": profile_object,
        "username": username
    }
    return render(request, "profiles/detail.html", context)

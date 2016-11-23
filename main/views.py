from django.shortcuts import render, redirect
from .forms import formSignUp,formLogin
from django.db.models import F
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import user_details, Recording, user_work, profession, company, followers
import hashlib
from django.core.files.base import ContentFile
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    form_sign_up = formSignUp()
    form_login = formLogin()
    return render(request, 'main/home_page.html', {'form_sign_up':form_sign_up,'form_login':form_login})

def random_file_name():
    a = 'sjwhdu32'
    return a
def upload(request):
    print ("OUT")
    if request.method == 'POST':
        print("IN")
        view = '4' #1: Private 2: Public 3: Custom 4: not defined
        newrec = Recording(audiolink=request.FILES['blob'],view=view,user_id=request.user.id)
        newrec.save()
        print("File saved: " +request.FILES['blob'].name)
        return HttpResponse("Sorry man!")
    else:
        print("yes")
        return HttpResponse("Sorry!")

def add_audio_details(request):
    user_id_in_action = request.user.id
    title = request.POST['audio_post_title']
    description = request.POST['audio_post_desc']
    view = request.POST['audio_post_view']
    if view == 'Circle':
        view = '1'
    elif view == 'Public':
        view = '2'
    else:
        view = '4'
    audio_id = Recording.objects.filter(user_id=user_id_in_action).order_by('-id')[0].id
    audio_instance = Recording.objects.get(id=audio_id)
    audio_instance.title = title
    audio_instance.description = description
    audio_instance.view = view
    audio_instance.save()
    return HttpResponse("Sorry man!")
    
def add_new_user(request):
    if request.method == 'POST':
        form = formSignUp(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username_email = form.cleaned_data['username_email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username_email,username_email,password)
            user_details_save = user_details.objects.create(user=user,full_name=full_name)
            full_name = full_name.split()
            if len(full_name)== 1:
                user.first_name = full_name[0]
            else:
                user.last_name = full_name[-1]
                user.first_name = " ".join(full_name[:-1])
            user.save()
    else:
        return HttpResponse("Sorry!")
    user = authenticate(username=username_email, password=password)
    login(request, user)
    return render(request, 'main/welcome_user.html')
    # return HttpResponse("thank you, you're added!")

def verify_login(request):
    if request.method == 'POST':
        form = formLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("User is valid, active and authenticated")
                    user_id = request.user.id
                    user_links = user_details.objects.filter(user_id=user_id).values_list('photo_link','profile_link')
                    return render(request, 'main/welcome_user.html',{'photo_link':user_links[0][0], 'profile_link':user_links[0][1]})
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")
                return HttpResponse("Sorry, check initials")
def requested_owner_profile(request,requested_profile_user_id):
    print("in func: " + str(requested_profile_user_id))
    fetched_values = user_details.objects.filter(user_id=requested_profile_user_id).values_list('intro','full_name','photo_link','followers_total','circle_total')
    work = company.objects.filter(user_work__user_id=requested_profile_user_id,user_work__rank='1').values_list('name',flat = True)
    if not work:
        print("yeahsss")
    profession_name = profession.objects.filter(user_work__user_id=requested_profile_user_id,user_work__rank='1').values_list('name', flat = True)
    return render(request,'main/owner_user_profile.html',{'full_name':fetched_values[0][1],'photo_link':fetched_values[0][2],'followers_total':fetched_values[0][3],'circle_total':fetched_values[0][4],'desc':fetched_values[0][0],'profession_name':profession_name,'work':work})

def send_followers(request):
    requested_profile_user_id = request.user.id
    followers_id_list = followers.objects.filter(user_id=requested_profile_user_id).values_list('follower_id')
    followers_final_detail = {}
    for item in followers_id_list:
        one = user_details.objects.filter(user_id=item).values_list('full_name','profile_link','photo_link')
        temp_dict = {}
        temp_dict['full_name'] = one[0][0]
        temp_dict['profile_link'] = one[0][1]
        temp_dict['photo_link'] = one[0][2]
        followers_final_detail['follower' + str(item)] = temp_dict
    return JsonResponse(followers_final_detail)
@csrf_exempt
def add_follower_to_user(request):
    url_user = request.POST['url_user']
    #do the following with regular expressions
    for index in range(-2,-len(url_user),-1):
        if url_user[index] == '/':
            profile_link = url_user[index+1:-1]
            break
    user_id_in_action = request.user.id
    user_id_to_follow = user_details.objects.filter(profile_link=profile_link).values_list('user_id',flat='True')
    print(user_id_to_follow)
    followers.objects.create(follower_id=user_id_in_action,user_id=user_id_to_follow[0])
    user_details.objects.filter(user_id=user_id_to_follow).update(followers_total=F('followers_total') + 1)
    user_details.objects.filter(user_id=user_id_in_action).update(following_total=F('following_total') + 1)
    user_id_to_follow_followers = user_details.objects.filter(user_id=user_id_to_follow).values_list('followers_total', flat=True)
    return JsonResponse({'total':user_id_to_follow_followers[0]})

def show_user_profile(request,requested_profile_link):
    print('show_user_profile')
    print(requested_profile_link)
    requested_profile_user_id = user_details.objects.filter(profile_link=requested_profile_link).values_list('user_id')
    if not requested_profile_user_id:
        return HttpResponse("Profile not found")
    else:
        requested_by_user_id = request.user.id
        if requested_by_user_id == requested_profile_user_id[0][0]:
            print("same")
            return requested_owner_profile(request,requested_profile_user_id)
        fetched_values_user = user_details.objects.filter(user_id=requested_by_user_id).values_list('photo_link',flat=True)
        fetched_values = user_details.objects.filter(user_id=requested_profile_user_id).values_list('intro','full_name','photo_link','followers_total','circle_total')
        work = company.objects.filter(user_work__user_id=requested_profile_user_id,user_work__rank='1').values_list('name',flat = True)
        if not work:
            print("yeahsss")
        profession_name = profession.objects.filter(user_work__user_id=requested_profile_user_id,user_work__rank='1').values_list('name', flat = True)
    # profession_name = ['sas']
        return render(request,'main/user_profile.html',{'self_photo_link':fetched_values_user[0],'full_name':fetched_values[0][1],'photo_link':fetched_values[0][2],'followers_total':fetched_values[0][3],'circle_total':fetched_values[0][4],'desc':fetched_values[0][0],'profession_name':profession_name,'work':work})

@csrf_exempt
def create_feed(request):
    user_id_in_action = request.user.id
    feed_posts = {}
    following_id_list = followers.objects.filter(follower_id=user_id_in_action).values_list('user_id')
    for user_id in following_id_list:
        user_recording_list = Recording.objects.filter(user_id=user_id)
        if user_recording_list:
            for recording in user_recording_list:
                temp_dict = {}
                if recording.view != '3' and recording.view != '1':
                    temp_dict['audio_link'] = str(recording.audiolink)
                    print (recording.audiolink)
                    temp_dict['likes_total'] = recording.likes_total
                    temp_dict['comments_total'] = recording.comments_total
                    temp_dict['shares_total'] = recording.shares_total
                    temp_dict['title'] = recording.title
                    temp_dict['description'] = recording.description
                    one = user_details.objects.filter(user_id=user_id).values_list('full_name','profile_link','photo_link')
                    temp_dict['full_name'] = one[0][0]
                    temp_dict['profile_link'] = one[0][1]
                    temp_dict['photo_link'] = one[0][2]
                feed_posts['post: ' + str(recording.id)] = temp_dict
    print ("sending now ")
    return JsonResponse(feed_posts)

def logout_user(request):
    logout(request)
    # get user details from session_key
    # from django.contrib.sessions.models import Session
    # from django.contrib.auth.models import User
    # session_key = '9fwzxy8fea9oie2yat2xffnbonxm4kjd'
    # session = Session.objects.get(session_key=session_key)
    # uid = session.get_decoded().get('_auth_user_id')
    # user = User.objects.get(pk=uid)
    # print (user.username, user.get_full_name(), user.email)
    form_sign_up = formSignUp()
    form_login = formLogin()
    return render(request, 'main/home_page.html', {'form_sign_up':form_sign_up,'form_login':form_login})

def social_login(request):
    return render(request, 'main/welcome_user.html')
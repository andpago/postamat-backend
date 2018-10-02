from django.db import IntegrityError
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from postamat.settings import MEDIA_ROOT
from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('username', 'avatar')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], url_path='self', url_name='self', detail=False)
    def get_self_info(self, request):
        tk = request.data.get('token', None)

        try:
            user = Token.objects.get(key=tk).user
        except Token.DoesNotExist:
            return JsonResponse({
                "error": "no user with this token"
            })

        try:
            avatarUrl = user.avatar.url
        except ValueError:
            avatarUrl = None

        return JsonResponse({"user": {
            "username": user.username,
            "avatar": avatarUrl,
        }})

    @action(methods=['POST'], url_path='registration', url_name='registration', detail=False)
    def registration(self, request):
        print(dir(request))
        print(request.FILES)
        fields = ['username', 'email', 'password1', 'password2']
        files = ['avatar']

        lost_fields = list(set(fields) - set(request.POST.keys()))
        lost_files = list(set(files) - set(request.FILES.keys()))

        if lost_fields + lost_files:
            print("lost fields:", *lost_fields)
            return HttpResponseBadRequest(f'fields {lost_fields + lost_files} are required')

        if request.POST['password1'] != request.POST['password2']:
            return HttpResponseBadRequest(f'passwords do not match')

        u = User(username=request.POST['username'],
                 email=request.POST['email'])

        u.set_password(request.POST['password1'])


        file = request.FILES['avatar']
        fname = f'avatar_{hash(file)}_{file.name}'

        with open(f'{MEDIA_ROOT}/{fname}', 'wb+') as avatar:
            for chunk in file.chunks():
                avatar.write(chunk)

        print(f'wrote {MEDIA_ROOT}/{fname}')
        u.avatar = fname


        try:
            u.save()
        except IntegrityError:
            return HttpResponseBadRequest(f'a user with this username or email already exists')

        return HttpResponseRedirect(redirect_to='/login')

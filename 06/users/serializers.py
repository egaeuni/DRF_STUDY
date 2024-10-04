from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password # Django의 기본 패스워드 검증 도구
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator #이메일 중복 방지를 위한 검증 도구
from django.contrib.auth import authenticate # 유저 인증
from .models import Profile

# 회원 가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        help_text="이메일(Unique)",
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all())] # 이메일 중복 검증
    )
    password = serializers.CharField(
        help_text = "비밀번호",
        write_only = True,
        required = True,
        validators = [validate_password] # 비밀번호 검증
    )

    password2 = serializers.CharField(write_only=True, required=True, help_text="비밀번호 재입력") #비밀번호 확인
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data):
        # 추가적으로 비밀번호 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
    
        return data

    def create(self, validated_data):
        # create 요청에 대해 create 매소드를 오버라이딩, 유저를 생성하고 토큰 생성
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {
                "error":"Unable to log in with provided credentials"
            }
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", 'subjects', 'image')
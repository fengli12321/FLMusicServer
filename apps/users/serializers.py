from datetime import datetime, timedelta


from rest_framework import serializers

from .models import VerifyCode, UserProfile

class VerifyCodeSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        one_minute_ago = datetime.now() - timedelta(days=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute_ago):
            raise serializers.ValidationError("请稍后再发送")
        if len(mobile) != 11:
            raise serializers.ValidationError("手机号不正确")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):

    code = serializers.CharField(max_length=6, write_only=True)
    mobile = serializers.CharField(max_length=11)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        label="密码",
        write_only=True,
        required=True
    )

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError("密码强度不足")
        return password

    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data["mobile"])
        if verify_code:
            last_record = verify_code.last()
            five_minute_ago = datetime.now() - timedelta(days=0, minutes=5, seconds=0)
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            elif code != last_record.code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("未发送验证码")

    def validate(self, attrs):
        del attrs["code"]
        attrs["username"] = attrs["mobile"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ("code", "mobile", "username", "password")
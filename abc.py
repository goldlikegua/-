# 关注，粉丝
a = User()
b = User()
Follow(follow = a, fan = b).save()
b == a.follow_user.all()[0].fan

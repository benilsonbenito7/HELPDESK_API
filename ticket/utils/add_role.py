from django.contrib.auth.models import User, Group

User.objects.all()

user = User.objects.get(username="bbenito1")
admin_group = Group.objects.get(name="admin")
user.groups.add(admin_group)

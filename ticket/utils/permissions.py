def get_user_role(user):
    if user.groups.exists():
        return user.groups.first().name

    return "user"
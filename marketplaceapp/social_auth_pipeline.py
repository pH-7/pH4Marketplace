from marketplaceapp import Profile

FB_GRAPH_AVATAR_URL = 'https://graph.facebook.com/%s/picture?type=large'

def save_avatar(backend, user, respomse, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        profile.avatar = FB_GRAPH_AVATAR_URL % response['id']

    profile.save()

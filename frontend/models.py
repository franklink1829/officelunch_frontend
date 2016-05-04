from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

import hashlib

class SavedEmbeds(models.Model):
    type = models.CharField(max_length=15)
    provider_url = models.URLField()
    provider_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    html = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    thumbnail_url = models.URLField()
    thumbnail_width = models.IntegerField()
    thumbnail_height = models.IntegerField()
    author_url = models.URLField()
    author_name = models.CharField(max_length=100)
    version = models.DecimalField(max_digits=4, decimal_places=2)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def profile_image_url(self):
        g_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='google')
        email_bytes = self.user.email.encode('utf-8')

        if len(g_uid):
            return g_uid[0].get_avatar_url()

        return "http://www.gravatar.com/avatar/{}".format(hashlib.md5(email_bytes).hexdigest())

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

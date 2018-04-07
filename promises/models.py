from django.db import models

class Promise(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sinceWhen = models.DateTimeField()
    tilWhen = models.DateTimeField()
    user1 = models.ForeignKey("auth.User", related_name="promises_as_inviter", on_delete=models.CASCADE)
    user2 = models.ForeignKey("auth.User", related_name="promises_as_invitee", on_delete=models.CASCADE)

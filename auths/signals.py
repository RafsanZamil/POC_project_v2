from django.db.models.signals import post_save
from django.dispatch import receiver
from auths.models import CustomUser
from transactions.models import Balance


@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)


# Register the signal
post_save.connect(create_user_balance, sender=CustomUser)





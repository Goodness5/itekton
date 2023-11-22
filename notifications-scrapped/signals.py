# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Notification
# from accounts.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def create_notification(sender, instance, created, **kwargs):
#     if created:
#         # Customize the verb and other details based on your application logic
#         Notification.objects.create(
#             actor=instance.user,  # Assuming there is a user field on YourModel
#             verb='created',
#             action_object=instance,
#             target=instance.some_related_model,
#         )

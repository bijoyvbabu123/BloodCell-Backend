from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    AvailableDonors,
    BloodRequirement,
)
from users.models import (
    User, 
    Profile,
)
from telegrambot.models import (
    TelegramData,
)
from telegrambot.telegrambothandlerfunctions import (
    BloodRequestMessage,
)



# populating available donors and initiate telegram messaging
@receiver(post_save, sender=BloodRequirement)
def populate_available_donors(sender, instance, created, **kwargs):
    print("inside signal") ###########################################################################
    if instance.is_case_verified and instance.is_case_live():  # only if the case if verified by the admin and is live
        # get all the users with the same blood group
        blood_matched_profiles = Profile.objects.filter(blood_group=instance.blood_group)
        print(blood_matched_profiles, type(blood_matched_profiles))  ##################################
        
        telegram_ids = []
        for profile in blood_matched_profiles:
            if profile.is_date_three_months_past_last_donation(comp_date=instance.date_of_donation) or not(profile.last_donated_on):
                print(profile, type(profile))  ########################################################
                # create an available donor object
                AvailableDonors.objects.create(
                    user=profile.user,
                    blood_requirement=instance,
                )
                # get the telegram id of the user
                telegram_id = TelegramData.objects.get(user=profile.user).chat_id
                if telegram_id:
                    telegram_ids.append(telegram_id)
        
        print(telegram_ids, type(telegram_ids), "telegram idss")  ########################################################
        # send message to all the telegram ids
        BloodRequestMessage.send_blood_request_messages(chat_ids=telegram_ids, blood_req=instance)

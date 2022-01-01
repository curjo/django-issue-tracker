from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_init


class StatusChoice(models.IntegerChoices):
    OPEN = 0
    IN_PROGRESS = 1
    WONT_FIX = 2
    RESOLVED = 3


# CURTIS: New selection choices
class PlatformChoice(models.IntegerChoices):
    ANDROID = 0
    IOS = 1
    CHROME = 2
    SAFARI = 3
    FIREFOX = 4


class TypeChoice(models.IntegerChoices):
    BUG = 0
    FEATURE = 1


class Issue(models.Model):
    """
    Represents each issues reported by someone.

    Setting foreign relations to protect, since we should allow for deletion
    of any users without activities, but if they already have activity, they shouldn't be
    able to be deleted easily
    """

    name = models.CharField(max_length=255)
    description = models.TextField()

    # CURTIS: New field
    type = models.IntegerField(
        default=TypeChoice.BUG, choices=TypeChoice.choices
    )

    status = models.IntegerField(
        default=StatusChoice.OPEN, choices=StatusChoice.choices
    )
    linked_issues = models.ManyToManyField(to="Issue", blank=True)
    project = models.ForeignKey(to="project.Project", on_delete=models.PROTECT)
    reported_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_reported",
    )
    assigned_to = models.ForeignKey(
        null=True,
        blank=True,
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(class)s_assigned",
    )

    # CURTIS: New fields
    version = models.CharField(null=True, blank=True, max_length=255)
    platform = models.IntegerField(
        default=PlatformChoice.IOS, choices=PlatformChoice.choices
    )

    screenshot = models.ImageField(null=True, blank=True, upload_to='uploads/')


    # CURTIS: Section below tracks "state" change in order to trigger code
    state = models.IntegerField(null=True, default=0)
    previous_state = None

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        if instance.previous_state != instance.state or created:
            print("EVENT HAS BEEN SAVED!")

    @staticmethod
    def remember_state(sender, instance, **kwargs):
        instance.previous_state = instance.state
        instance.state += 1
    # End of state-related section

    def __str__(self) -> str:
        return self.name


# CURTIS: Additional state-change related stuff
post_save.connect(Issue.post_save, sender=Issue)
post_init.connect(Issue.remember_state, sender=Issue)

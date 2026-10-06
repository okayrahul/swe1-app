from django.db import migrations
from django.utils import timezone


def seed_polls(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Choice = apps.get_model("polls", "Choice")

    if Question.objects.exists():
        return

    q1 = Question.objects.create(
        question_text="What's new?",
        pub_date=timezone.now(),
    )
    Choice.objects.create(question=q1, choice_text="Not much")
    Choice.objects.create(question=q1, choice_text="The sky")
    Choice.objects.create(question=q1, choice_text="Just hacking again")

    q2 = Question.objects.create(
        question_text="What's your favorite Django topic?",
        pub_date=timezone.now(),
    )
    Choice.objects.create(question=q2, choice_text="Models")
    Choice.objects.create(question=q2, choice_text="Views")
    Choice.objects.create(question=q2, choice_text="Templates")
    Choice.objects.create(question=q2, choice_text="Deployment")


def unseed_polls(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.filter(
        question_text__in=[
            "What's new?",
            "What's your favorite Django topic?",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_polls, unseed_polls),
    ]

"""Initial integration tests for the polls application."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class PollsWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Keep tests independent of the deployment's sample-data migration.
        Question.objects.all().delete()
        cls.question = Question.objects.create(
            question_text="Which Django feature do you like?",
            pub_date=timezone.now(),
        )
        cls.choice = Choice.objects.create(
            question=cls.question, choice_text="Models", votes=0
        )

    def test_home_redirects_to_polls(self):
        self.assertRedirects(self.client.get("/"), reverse("polls:index"))

    def test_index_displays_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, self.question.question_text)

    def test_detail_displays_choices(self):
        response = self.client.get(reverse("polls:detail", args=[self.question.pk]))
        self.assertContains(response, self.choice.choice_text)

    def test_vote_increments_count_and_redirects_to_results(self):
        response = self.client.post(
            reverse("polls:vote", args=[self.question.pk]),
            {"choice": self.choice.pk},
        )
        self.assertRedirects(
            response, reverse("polls:results", args=[self.question.pk])
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_missing_choice_shows_error_without_recording_vote(self):
        response = self.client.post(reverse("polls:vote", args=[self.question.pk]))
        self.assertContains(response, "You didn&#x27;t select a choice.")
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_choice_from_another_question_is_rejected(self):
        other_question = Question.objects.create(
            question_text="Another poll", pub_date=timezone.now()
        )
        other_choice = Choice.objects.create(
            question=other_question, choice_text="Other choice"
        )
        response = self.client.post(
            reverse("polls:vote", args=[self.question.pk]),
            {"choice": other_choice.pk},
        )
        self.assertContains(response, "You didn&#x27;t select a choice.")
        other_choice.refresh_from_db()
        self.assertEqual(other_choice.votes, 0)

    def test_unknown_question_returns_404(self):
        response = self.client.get(reverse("polls:detail", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_results_without_votes_show_zero_percent(self):
        response = self.client.get(reverse("polls:results", args=[self.question.pk]))
        self.assertEqual(response.context["total_votes"], 0)
        self.assertContains(response, "0%")
        self.assertContains(response, "0 votes")

    def test_results_display_vote_totals_and_rounded_percentages(self):
        self.choice.votes = 2
        self.choice.save()
        Choice.objects.create(question=self.question, choice_text="Views", votes=1)
        response = self.client.get(reverse("polls:results", args=[self.question.pk]))
        self.assertEqual(response.context["total_votes"], 3)
        self.assertContains(response, "67%")
        self.assertContains(response, "33%")
        self.assertContains(response, "3 votes")

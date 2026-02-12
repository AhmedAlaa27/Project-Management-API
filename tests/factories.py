import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from Workspaces.models import Workspace
from Projects.models import Project
from Tasks.models import Task

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password and save user."""
        if create:
            password = extracted or "testpass123"
            self.set_password(password)
            self.save()


class WorkspaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workspace
        skip_postgeneration_save = True

    name = factory.Faker("company")
    description = factory.Faker("text", max_nb_chars=200)
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)
        else:
            # By default, add the owner as a member
            self.members.add(self.owner)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("catch_phrase")
    description = factory.Faker("text", max_nb_chars=300)
    workspace = factory.SubFactory(WorkspaceFactory)
    deadline = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
        skip_postgeneration_save = True

    name = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    project = factory.SubFactory(ProjectFactory)
    author = factory.SubFactory(UserFactory)
    status = Task.Status.TODO
    priority = Task.Priority.MEDIUM
    due_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))

    @factory.post_generation
    def assignees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for assignee in extracted:
                self.assignees.add(assignee)
        # If no assignees specified, optionally add the author
        elif self.author:
            self.assignees.add(self.author)

from django.db import models
from agent_app.models import Agent


class Chat(models.Model):
    """
    Model representing a chat.

    Attributes:
        user_id (ForeignKey): The user associated with the chat.
        name (TextField): The name of the chat.
        created_at (DateTimeField): The date and time of chat creation.
        updated_at (DateTimeField): The date and time of chat update.
    """

    owner_id = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='owner_id',
    )
    addressee_id = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='addressee_id',
    )
    name = models.TextField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.owner_id}'
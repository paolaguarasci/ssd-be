from datetime import date, timedelta

from django.core.exceptions import ValidationError


def descriptionValidator(value: str) -> None:
  if len(value) > 100:
    raise ValidationError("Destription must be at most 100 characters")

def startDateValidator(value: date) -> None:
  if value < date.today():
    raise ValidationError("Start date must not be in the past")

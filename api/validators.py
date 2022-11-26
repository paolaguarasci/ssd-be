from datetime import date, timedelta

from django.core.exceptions import ValidationError


def descriptionValidator(value: str) -> None:
  if len(value) == 0:
    raise ValidationError("Destription must not be empty")

def startDateValidator(value: date) -> None:
  if value < date.today():
    raise ValidationError("Start date must not be in the past")

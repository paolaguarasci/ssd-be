from datetime import date, timedelta

from django.core.exceptions import ValidationError

"""
Error message list
"""
ERROR_DESCRIPTION_MAX_100_CHARACTERS = "Destription must be at most 100 characters"
ERROR_DATE_IS_BEFORE_TODAY = "Start date must not be in the past"


def descriptionSizeValidator(value: str) -> None:
  if len(value) > 100:
    raise ValidationError(f"{ERROR_DESCRIPTION_MAX_100_CHARACTERS}")

def startDateValidator(value: date) -> None:
  if value < date.today():
    raise ValidationError(f"{ERROR_DATE_IS_BEFORE_TODAY}")


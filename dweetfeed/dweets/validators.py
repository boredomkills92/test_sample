from django.core.exceptions import ValidationError

def validateDweet(value):
	value = value.strip(" ")
	if len(value) == 0:
		raise ValidationError("Please provide message !!!")

def validateTweet(value):
	value = value.strip(" ")
	if len(value) == 0:
		raise ValidationError("Please provide message !!!")



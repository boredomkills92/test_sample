from rest_framework import permissions
from .models import Dweet

class PostOwnDweet(permissions.BasePermission):
	"""
	provide only permission to edit/update only their own profiles
	"""

	def has_object_permission(self, request, view, obj):
		"""
		check user for authorization
		"""
		
		if request.method in permissions.SAFE_METHODS:
			return True
		
		if isinstance(obj,Dweet):					
			dweet = obj.dweeted_user.filter(pk=request.user.id).distinct()
			if dweet.exists():
				id_ = dweet[0].id
			else:
				return True
		else:
			id_ = obj.id

		return id_ == request.user.id

class ReactOnDweet(permissions.BasePermission):
	"""
	provide only permission to POST reaction
	"""

	def has_object_permission(self, request, view, obj):
		"""
		check user for authorization
		"""

		if request.method.upper() == "POST".upper() :
			return True
		else:
			return False
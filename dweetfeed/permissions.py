from rest_framework import permissions

class OnlySafeMethods(permissions.BasePermission):
	"""
	provide only permission to safe methods
	"""

	def has_object_permission(self, request, view, obj):
		"""
		restricts only for get, options and head
		"""
		
		if view.action in ['retrieve', 'update', 'partial_update','create']:
			return False
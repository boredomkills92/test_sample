"""
Custom middleware to provide logging for all requests
"""

from django.conf import settings
import logging

class LoggingMiddleware:
    """
    Logging middleware to log details about requests, response and exception

    :param name: get_response callable for the last middleware passed by Django 
    """

    def __init__(self, get_response):
        self.get_response = get_response
        
        #setting logger
        self.debug_helper = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)        

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.        
        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.

        status_code = response.status_code
        log_kwargs =  {
            'method': request.method.lower(),
            'status_code': status_code,
            'request_path': request.path,
        }               

        self.logger.info(log_kwargs)
        self.logger.info(self.debug_helper)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        This methond is called just before the view by django
        """

        self.debug_helper['view_name'] = view_func.__name__
        self.debug_helper['module'] = view_func.__module__        

    def process_exception(self, request, exception):
        """
        This methond is called when a view raises an exception.
        """

        if settings.DEBUG:
            import traceback
            self.logger.exception("printme" + traceback.format_exc())        
        else:
            self.logger.error(exception)
        return None
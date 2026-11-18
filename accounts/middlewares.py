from django.shortcuts import render,redirect
class SimpleMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        #One time configuration and initialization. Runs once when runserver is executed 
        print("Custom middleware initialized.")

    def __call__(self, request):

        #code to be executed for each request before the view (and later middleware are called)
        
        print("Before view call.")

        public_urls=[
            '/admin/',
            '/accounts/register/',
            '/accounts/login/',
            '/',
        ]

        if not request.user.is_authenticated:
            if request.path not in public_urls:
                return redirect("login")

        response = self.get_response(request)
        print("After view call.")

        #code to be executed for each request/response after the view is called 

        if request.user.is_authenticated:
            response['Cache-Control']=('no-cache,no-store,must-revalidate')

            response['Pragama']='no-cache'
            response['Expires']='0'


        return response
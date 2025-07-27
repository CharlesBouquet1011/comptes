from django.http import JsonResponse

class DisableMediaCacheMiddleware:
    """
    Sert à désactiver le cache du navigateur sur les images qui sont modifiées de façons dynamique aux mêmes URLs
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            if request.method in["GET","POST"]:
                compte=request.GET.get("compte") if request.method=="GET" else request.POST.get("compte")
                if compte=="tousComptes" or compte=="":
                    return JsonResponse({"error":"Veuillez chosir un autre nom de compte"},status=403)




        response = self.get_response(request)
        if request.path.startswith('/exports/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
from django.http import JsonResponse



class Success:
    @staticmethod
    def SimpleSuccess(user_payload=None):
        return JsonResponse({'result':'success', 'user_payload':user_payload},safe=False, status=200)
    
    @staticmethod
    def DataSuccess(data, user_payload=None):
        return JsonResponse({'result':'success', 'user_payload':user_payload, 'data':data}, safe=False, status=200)
    


class Error:
    # TOKEN ERRORS
    @staticmethod
    def TokenVerificationError(user_payload=None):
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed', 'user_payload':user_payload}, safe=False, status=401)
    

    # NOT EXIST ERRORS
    @staticmethod
    def UserNotExist(user_payload=None):
        return JsonResponse({'result':'failed','error':'UserNotExist', 'user_payload':user_payload}, safe=False, status=404)
    
    @staticmethod
    def ProfileNotExist(user_payload=None):
        return JsonResponse({'result':'failed', 'error':'ProfileDoesNotExist', 'user_payload':user_payload}, safe=False, status=404)

    @staticmethod
    def PlaylistNotExist(user_payload=None):
        return JsonResponse({'result':'failed','error':'PlaylistNotExist', 'user_payload':user_payload}, safe=False, status=404)
    
    @staticmethod
    def TrackNotExist(user_payload=None):
        return JsonResponse({'result':'failed','error':'TrackNotExist', 'user_payload':user_payload}, safe=False, status=404)

    @staticmethod
    def GenreNotExist(user_payload=None):
        return JsonResponse({'result':'failed','error':'GenreNotExist', 'user_payload':user_payload}, safe=False, status=404)

    @staticmethod
    def RelationNotExist(user_payload=None):
        return JsonResponse({'result':'failed','error':'RelationNotExist', 'user_payload':user_payload}, safe=False, status=404)
    

    # SOMETHING WRONG ERRORS
    @staticmethod
    def WrongBodyRepresentation(user_payload=None):
        return JsonResponse({'result':'failed','error':'WrongBodyRepresentation', 'user_payload':user_payload}, safe=False, status=400)
    
    @staticmethod
    def WrongMethod(user_payload=None):
        return JsonResponse({'result':'failed', 'error':'WrongMethod', 'user_payload':user_payload}, safe=False, status=405)
    
    @staticmethod
    def WrongPassword(user_payload=None):
        return JsonResponse({'result':'failed','error':'WrongPassword', 'user_payload':user_payload}, safe=False, status=400)

    @staticmethod
    def WrongUsername(user_payload=None):
        return JsonResponse({'result':'failed','error':'WrongUsername', 'user_payload':user_payload}, safe=False, status=400)
    
    @staticmethod
    def WrongFileRepresentation(user_payload=None):
        return JsonResponse({'result':'failed','error':'WrongFileRepresentation', 'user_payload':user_payload}, safe=False, status=400)
    
    @staticmethod
    def WrongFileFormat(user_payload=None):
        return JsonResponse({'result':'failed','error':'WrongFileFormat', 'user_payload':user_payload}, safe=False, status=400)
    

    # REGISTRATION ERRORS    
    @staticmethod
    def EmailUsed(user_payload=None):
        return JsonResponse({'result':'failed', 'error':'EmailUsed', 'user_payload':user_payload}, safe=False, status=409)
    
    @staticmethod
    def UsernameUsed(user_payload=None):
        return JsonResponse({'result':'failed', 'error':'UsernameUsed', 'user_payload':user_payload}, safe=False, status=409)
    
    
    # OTHER ERRORS
    @staticmethod
    def UserIsntAuthor(user_payload=None):
        return JsonResponse({'result':'failed','error':'UserIsntAuthor', 'user_payload':user_payload}, safe=False, status=409)
    
    @staticmethod
    def AlreadyInList(user_payload=None):
        return JsonResponse({'result':'failed','error':'AlreadyInList', 'user_payload':user_payload}, safe=False, status=409)

    
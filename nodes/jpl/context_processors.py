from django.conf import settings # import the settings file

def admin_media(context):
    # return values which can be accessed in the templates
    return {'PORTAL_URLPATH': settings.PORTAL_URLPATH,
            'BASE_URL':settings.BASE_URL,
            'TAP_URLPATH':settings.TAP_URLPATH,
            }

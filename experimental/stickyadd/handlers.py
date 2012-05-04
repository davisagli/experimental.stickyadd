import time
import uuid
from email.Utils import formatdate
from zope.component import adapter
from zope.globalrequest import getRequest
from ZPublisher.interfaces import IPubSuccess
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.interfaces import IContentish


@adapter(IContentish, IObjectAddedEvent)
def set_cookie(object, event):
    request = getRequest()
    if 'portal_factory' in object.getPhysicalPath():
        return
    if request is not None:
        request.response.setCookie('__stick', str(uuid.uuid4()), path='/')


@adapter(IPubSuccess)
def expire_cookie(event):
    request = event.request
    if '__stick' not in request.response.cookies:
        request.response.expireCookie('__stick', path='/')

from pybald.core.controllers import action, BaseController
import requests
from jobskill.app.models import User
CLIENT_ID = "9a947adb8134494e866ae93787559187"
CLIENT_SECRET = "dba7262cb357f29d0c508e1192b06226"


class AuthenticatationController(BaseController):
    '''Random experimental pages.'''

    @action
    def smarterer_callback(self, req):
        auth_code = req.GET.get('code', 'NO CODE')

        params = {'client_id': CLIENT_ID,
                  'client_secret': CLIENT_SECRET,
                  'code': auth_code,
                  'grant_type': 'authorization_code'
                  }
        resp = requests.get('https://smarterer.com/oauth/access_token',
                            params=params,
                            verify=False)

        token = resp.json().get('access_token')
        if token:
            params = {'access_token': token}
            resp = requests.get('https://smarterer.com/api/users/me',
                                params=params, verify=False)
            prof_data = resp.json()
            try:
                user = User.get(username=prof_data['username'])
            except User.NotFound:
                user = User(access_token=token, username=prof_data['username']).save()
            self.session.user = user

            return self._redirect_to('home')
            # user_data = resp.json()
            # import pprint
            # return '<pre>'+str(pprint.pformat(user_data))+'</pre>'
        else:
            return self._redirect_to('home')

    @action
    def logout(self, req):
        self.session.user = None
        return self._redirect_to('home')

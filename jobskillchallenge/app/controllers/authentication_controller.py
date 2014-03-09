from pybald.core.controllers import action, BaseController
import requests
from jobskillchallenge.app.models import User
import project
CLIENT_ID = project.SMARTERER_CLIENT_ID
CLIENT_SECRET = project.SMARTERER_SECRET


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

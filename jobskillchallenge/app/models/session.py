from datetime import timedelta
import uuid
from pybald.db import models


def gen_id():
    '''Generate a session_id key for the session'''
    return uuid.uuid1().hex


class Session(models.Model):
    session_id = models.Column(models.String(32), unique=True, nullable=False)
    user_id = models.Column(models.Integer, models.ForeignKey('users.id'))
    user = models.relationship("User")

    def __init__(self, days=14, new=False, *pargs, **kargs):
        self.days = days
        self.new = new
        self.session_id = gen_id()
        super(Session, self).__init__(*pargs, **kargs)

    @models.reconstructor
    def __orm_init__(self):
        self.new = False

    @classmethod
    def _before(cls, req):
        # check if the browser has a cookie with a session_id
        # load the session from the session_id
        try:
            session_id = req.cookies['session_id']
            sess = cls.get(session_id=session_id)
        # no session_id cookie set, either no session
        # or create anon session
        except (KeyError, IOError, cls.NotFound):
            sess = cls(new=True)
            sess.save()
        return sess

    def _after(self, req=None, resp=None):
        # set the cookie on the response
        if self.new:
            expires = None
            if self.days:
                expires = timedelta(days=self.days)
            resp.set_cookie('session_id',
                            req.environ['pybald.session'].session_id,
                            max_age=expires,
                            path='/')

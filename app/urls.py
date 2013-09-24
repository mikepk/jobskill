

def map(urls):
    '''
    Defines the url to controller mapping for the application. A
    routes mapper or submapper object must be passed in.
    '''
    urls.connect('home', r'/', controller="home")

    urls.connect('authentication', r'/reg_complete', controller='authenticatation',
                 action='smarterer_callback')
    urls.connect('logout', r'/logout',
                 controller='authenticatation',
                 action='logout')

    # generic pattern
    urls.connect('base', r'/{controller}/{action}/{id}')
    urls.connect(r'/{controller}/{action}')
    urls.connect(r'/{controller}')

    # REDIRECT ALL URLS TERMINATING IN a slash, '/', to no slash
    # the opposite is also valid, all urls can be forced to have a slash
    # depends on your preference
    urls.redirect('{url:.*}/', '{url}',
                  _redirect_code='301 Moved Permanently')

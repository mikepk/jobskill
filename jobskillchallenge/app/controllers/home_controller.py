from pybald.core.controllers import action, BaseController
class HomeController(BaseController):
    '''The Home page.'''

    @action
    def index(self, req):
        self.post_count = 5
        self.character_level = "novice" if self.user else "hapless noob"
        # novice (authenticated w/Smarterer)
        # apprentice (score proficient in at least 1 skill test)
        # journeyman (score proficient in at least 2 skill tests)
        # seeker (unlock at least one job post)
        # experts
        # master
        # challenger
        # champion
        # legend
        # http://www.mba.com/the-gmat.aspx
        # http://wikipedia.org/

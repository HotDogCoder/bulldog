from django.contrib import admin
from django.utils.translation import ugettext_lazy


# Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('My site admin')

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('My administration')

# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('Site administration')
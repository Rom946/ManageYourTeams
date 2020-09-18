

class InjectFormMediaMixin(object):
    def get_form_class(self):
        form_class = super(InjectFormMediaMixin, self).get_form_class()
        if hasattr(self, 'Media') and not hasattr(form_class, 'Media'):
            form_class.Media = self.Media
        return form_class
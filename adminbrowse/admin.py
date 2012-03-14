from django.contrib.admin import ModelAdmin
from django.db.models import FieldDoesNotExist, ForeignKey, URLField
from django.conf import settings

from adminbrowse.related import link_to_change
from adminbrowse.columns import link_to_url


class AutoBrowseModelAdmin(ModelAdmin):
    """
    Subclass this to automatically enable a subset of adminbrowse features:

    - Linking to the change form for `ForeignKey` fields.
    - Linking to the URL for `URLField` fields.

    This will also include the adminbrowse media definition.

    """
    def __init__(self, model, admin_site):
        super(AutoBrowseModelAdmin, self).__init__(model, admin_site)

        self.list_display = tuple(self._process_list_display_entry(i) for i in self.list_display)

    def _process_list_display_entry(self, entry):
            if not isinstance(entry, basestring):
                return entry  # Do nothing

            try:
                field, model_, direct, m2m = self.opts.get_field_by_name(entry)
            except FieldDoesNotExist:
                return entry

            column = self._get_changelist_column(field)
            if column is not None:
                return column

            return column

    def _get_changelist_column(self, field):
        if isinstance(field, ForeignKey):
            return link_to_change(self.model, field.name)
        elif isinstance(field, URLField):
            return link_to_url(self.model, field.name)

    class Media:
        css = {'all': ("%s/css/adminbrowse.css" % settings.STATIC_URL)}


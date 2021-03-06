from django.contrib import admin
from django.db import models

def getter_for_related_field(name, admin_order_field=None, short_description=None):
    related_names = name.split('__')
    def getter(self, obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
        return obj
    getter.admin_order_field = admin_order_field or name
    getter.short_description = short_description or related_names[-1].title().replace('_',' ')
    return getter

class RelatedFieldAdminMetaclass(type(admin.ModelAdmin)):
    def __new__(cls, name, bases, attrs):
        new_class = super(RelatedFieldAdminMetaclass, cls).__new__(cls, name, bases, attrs)

        for field in new_class.list_display:
            if '__' in field:
                setattr(new_class, field, getter_for_related_field(field))

        return new_class

class RelatedFieldAdmin(admin.ModelAdmin):
    """
        Version of ModelAdmin that can use related fields in list_display, e.g.:
        list_display = ('address__city', 'address__country__country_code')
    """
    __metaclass__ = RelatedFieldAdminMetaclass
    def queryset(self, request):
        qs = super(RelatedFieldAdmin, self).queryset(request)

        # include all related fields in queryset
        select_related = [field.rsplit('__',1)[0] for field in self.list_display if '__' in field]

        # Include all foreign key fields in queryset.
        # This is based on ChangeList.get_query_set().
        # We have to duplicate it here because select_related() only works once.
        # Can't just use list_select_related because we might have multiple__depth__fields it won't follow.
        model = qs.model
        for field_name in self.list_display:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                continue
            if isinstance(field.rel, models.ManyToOneRel):
                select_related.append(field_name)

        return qs.select_related(*select_related)

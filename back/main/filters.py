from rangefilter.filter import DateRangeFilter


class FixedDateRangeFilter(DateRangeFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = '{}__gte'.format(field_path)
        self.lookup_kwarg_lte = '{}__lte'.format(field_path)

        params[self.lookup_kwarg_lte] = request.GET.get(self.lookup_kwarg_lte, '')
        params[self.lookup_kwarg_gte] = request.GET.get(self.lookup_kwarg_gte, '')

        super().__init__(field, request, params, model, model_admin, field_path)

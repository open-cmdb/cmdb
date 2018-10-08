
def get_all_field_name(model):
    fields = [i.name for i in model._meta.fields]
    # fields.reverse()
    return fields

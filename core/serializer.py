import datetime


class Serializer(object):

    def __init__(self, obj, with_relate=False):
        self.obj = obj
        self.meta = obj._meta
        self.with_relate = with_relate
        self.fields = self.meta.db_fields
        self.fk_fields = self.meta.fk_fields
        self.m2m_fields = self.meta.m2m_fields
        self.o2o_fields = self.meta.o2o_fields

    async def to_dict(self):
        res = dict()
        for field_name in self.fields:
            field_value = getattr(self.obj, field_name)
            if isinstance(field_value, datetime.datetime):
                res[field_name] = field_value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                res[field_name] = field_value
        if self.with_relate:
            for fk_field_name in self.fk_fields:
                fk_obj = await getattr(self.obj, fk_field_name)
                res[fk_field_name] = await Serializer(fk_obj, self.with_relate).to_dict()
        return res

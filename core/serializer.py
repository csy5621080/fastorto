import datetime


class Serializer(object):

    def __init__(self, obj, exclude: list = [], with_relate=False):
        self.exclude = exclude
        self.obj = obj
        self.meta = obj._meta
        self.with_relate = with_relate
        self.fields = list(set(self.meta.db_fields).difference(set(exclude)))
        self.fk_fields = list(set(self.meta.fk_fields).difference(set(exclude)))
        self.m2m_fields = list(set(self.meta.m2m_fields).difference(set(exclude)))
        self.o2o_fields = list(set(self.meta.o2o_fields).difference(set(exclude)))

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
                res[fk_field_name] = await Serializer(fk_obj, with_relate=self.with_relate).to_dict()
            for m2m_field_name in self.m2m_fields:
                m2m_objs = await getattr(self.obj, m2m_field_name)
                related_name = self.meta.fields_map[m2m_field_name].related_name
                res[m2m_field_name] = [await Serializer(m2m_obj,
                                                        exclude=[related_name],
                                                        with_relate=self.with_relate
                                                        ).to_dict()
                                       for m2m_obj in m2m_objs]
        return res

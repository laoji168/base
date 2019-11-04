from db import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_CONNECT_STRING = 'sqlite:///tt.db' #'sqlite:///:memory:'

class Base_SQL:
    def __init__(self):
        self.engine = create_engine(DB_CONNECT_STRING, echo=False)
        self.session = sessionmaker(bind=self.engine)()

    def init_db(self):
        model.BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        model.BaseModel.metadata.drop_all(self.engine)

    def insert(self, model):
        a=self.session.add(model)
        b=self.session.commit()
        print(a, b)

    def delete(self, model_cls, conditions=None):
        if conditions:
            conditon_list = []
            for key in conditions.keys():
                if getattr(model_cls, key):
                    conditon_list.append(getattr(model_cls, key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(model_cls)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)

    def update(self, model_cls ,conditions=None, value=None):
        '''
        conditions的格式是个字典。类似self.params
        :param conditions:
        :param value:也是个字典：{'ip':192.168.0.1}
        :return:
        '''
        if conditions and value:
            conditon_list = []
            for key in conditions.keys():
                if getattr(model_cls, key):
                    conditon_list.append(getattr(model_cls, key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(model_cls)
            for condition in conditions:
                query = query.filter(condition)
            updatevalue = {}
            for key in value.keys():
                if getattr(model_cls, key):
                    updatevalue[getattr(model_cls, key)] = value.get(key)
            updateNum = query.update(updatevalue)
            self.session.commit()
        else:
            updateNum = 0
        return {'updateNum': updateNum}


    def select(self, model_cls, property=None ,count=None, conditions=None):
        '''
        conditions的格式是个字典。类似self.params
        :param property: 查询的属性性选择，列表或元组，默认相当于select *
        :param count:
        :param conditions:
        :return:
        '''
        if conditions:
            conditon_list = []
            for key in conditions.keys():
                if getattr(model_cls, key):
                    conditon_list.append(getattr(model_cls, key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        if not property:
            query = self.session.query(model_cls)
        else:
            property = [getattr(model_cls, key) for key in property]
            query = self.session.query(*property)
        if len(conditions) > 0 and count:
            for condition in conditions:
                query = query.filter(condition)

            return query.limit(count).all()
        elif count:
            return query.limit(count).all()
        elif len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)
            return query.all()
        else:
            return query.all()


    def close(self):
        self.session.close()


if __name__ == '__main__':
    b = Base_SQL()
    b.init_db()
    class it:
        def __init__(self):
            self.name = "haha"
            self.fullname = "wahaha"
    user = model.Users().from_item(it())
    print(user.__dict__)
    print(user.name)
    b.insert(user)
    b.update(model.Users, {"name":"haha"}, {"name":"LAOJI"})
    #b.delete(model.Users, {"name":"laoji"})
    print(b.select(model.Users))
    print(b.select(model.Users, ["name"], conditions={'name':'laoji1'}))
    print(b.select(model.Users, ["name"],count=1, conditions={'name':'laoji1'}))
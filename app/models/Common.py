import datetime
from redis_om import (Field,
    Migrator,
    JsonModel)


class CommonModel(JsonModel):

    @classmethod
    def create(cls, fields):
        fields['createdAt'] = datetime.datetime.utcnow().timestamp();
        newCommonModel = cls(**fields)
        keys = fields.keys()
        
        for key in keys:
            if key != "pk":
                setattr(newCommonModel, key, fields[key])
        
        print("added createdAt")
        # setattr(newCommonModel, "createdAt", int(datetime.datetime.utcnow().timestamp()))
        
        newCommonModel.save()
        CommonModel.find()
        return newCommonModel
    
    @classmethod
    def updateField(cls, fields):
        keys = fields.keys()
        updateRecord = cls.get(fields["pk"]) 
        
        for key in keys:
            print(key)
            if key != "pk":
                setattr(updateRecord, key, fields[key])
                
        updateRecord.save()
        print(updateRecord)
        return updateRecord

    @classmethod
    def deleteByID(cls, pk):
        cls.delete(pk)

    @classmethod
    def findByID(cls, pk):
        try:
            print(cls)
            record = cls.get(pk)
            print(record)
            return record
        except Exception as e:
            return None
        


    @classmethod
    def getFilteredModel(cls , searchParams):
        conditions = []
        for param in searchParams:
            findCondition = ""
            key = param["key"]
            value = param["value"]
            operator = param["op"]
            if (value == ""):
                continue
            if operator == "equal":
                findCondition += ("cls." + key + "==" + "\"" + value + "\"")
            elif operator == "=":
                findCondition += ("cls." + key + "==" + value)
            elif operator == ">":
                findCondition += ("cls." + key + ">" + value)
            elif operator == "<":
                findCondition += ("cls." + key + "<" + value)
            elif operator == "contains":
                findCondition += ("cls." + key + "%" + "(\"*" + value + "*\")")

            conditions.append(findCondition)
        
        print("cls.find(" + ",".join(conditions) + ")")
        return eval("cls.find(" + ",".join(conditions) + ")")

    @classmethod
    def getTotalCount(cls, searchParams):
        model = cls.getFilteredModel(searchParams)
        
        return model.count()

    # pageSize, pageIndex, searchParams, projections
    @classmethod
    def findAll(cls, pageSize, pageIndex, searchParams):
        model = cls.getFilteredModel(searchParams)
        print("query :", model.query)
        if(pageSize > 0) :
            model.offset = pageSize * pageIndex
            model.limit = pageSize
        result = model.sort_by("createdAt").all()
        print("result : ", result)
        return result
    

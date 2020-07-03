from db import session

class ApiService():

    def get_all(self, model, schema):
        data = session.query(model).all()
        return [schema.dump(d) for d in data]
    

    def get_by_id(self, model, schema, id):
        data = session.query(model).filter(model.id == id).first()
        return schema.dump(data)


    def set_data(self, model, schema, fields, payload):
        
        error_list = list()
        for f in fields:
            if payload.get(f):
                setattr(model, f, payload[f])
            
            if not payload.get(f):
                error_list.append(f'Field {f} must be setted')
        
        if not error_list:
            session.add(model)
            session.commit()
            
            return True, schema.dump(model)
        
        return False, error_list
    
    def update_data(self, model, schema, payload, id):
        session.query(model).filter(model.id == id).update(payload)
        session.commit()
        
        data = session.query(model).filter(model.id == id).first()
        return schema.dump(data)
    
    def delete_data(self, model, schema, id):
        session.query(model).filter(model.id == id).delete()
        session.commit()

        return f'Removed id {id}'



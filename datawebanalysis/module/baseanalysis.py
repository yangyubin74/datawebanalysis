import datawebanalysis.module.sqlgen as sql


#########################플랫폼 가입도매 와 미 가입도매 분포#########################

#가입자, 비가입자 분포
def get_orm_member():
    return sql.select_org_member()    

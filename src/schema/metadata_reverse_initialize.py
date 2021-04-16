# ######metadata_reverse_initialize.py
from schema import schema_mysql as mysql, schema_oracle as ora, schema_pg as pg
from mdata import metadata_initialize as mdi
from config.config import cfg as config
from privilege import user_mngt as ur
from model import erwin_model_graph as emg

logger = config.logger

if __name__ == '__main__':
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    # oracle/pg为schema，mysql为数据库名
    schema = "demo"
    database_name = "mysql"
    # 数据库类类型mysql/oracle/pb
    db_type = 'mysql'
    # 步骤：1，
    # step={"1":"从erWin初始化表结构和字段元数据信息。",
    #       "2":"从mysql/oracle/pg数据库反向工程，初始化表和字段元数据",
    #       "3":"从数据表和字段元数据，初始化生成实体和属性元数据",
    #       "4":"mySql/oracle/pg的外键关系转成元数据实体关系",
    #       "5":"erwin的外键关系转成元数据实体关系",
    #       "6":"元数据对象生成Neo4J图数据库信息"}
    step = {
        # "2": "从mysql/oracle/pg数据库反向工程，初始化表和字段元数据",
        # "3": "从数据表和字段元数据，初始化生成实体和属性元数据",
          "4":"mySql/oracle/pg的外键关系转成元数据实体关系",
    }

    # ##### 1.初始化表结构从erWin文件(注意文件路径写法d:/downloads/eSpace_File/xxx.erwin)。
    file_name = "d:/downloads/eSpace_File/123-new.erwin"
    if step.get("1") is not None:
        re = emg.reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name)
        logger.info("all tables in[{}],re={}".format(schema, re))

    # ####1.2.从mysql/oracle/pg数据库反向工程，初始化表和字段元数据
    tables_list = ['rules','rules_entity_rel']
    if step.get("2") is not None:
        re=None
        if db_type == 'mysql':
            re = mysql.reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
        elif db_type == 'oracle':
            re = ora.reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
        elif db_type == 'pg':
            re = pg.reverse_tables_columns(user_id, tenant_id, database_name, schema, tables_list)
            pass

        logger.info("all tables in[{}],re={}".format(schema, re))

    # ####2.从数据表和字段元数据，初始化生成实体和属性元数据
    if step.get("3") is not None:
        # entity_list = [{"entity_code": "Contract", "table_name": "data_t"}, {"entity_code": "BoQ", "table_name": "data_t"}]
        entity_list = [{"entity_code": "rules", "table_name": "rules"},
                       {"entity_code": "rules_entity_rel", "table_name": "rules_entity_rel"}]
        re = mdi.initialize_md_entities_from_tables(user_id, tenant_id, entity_list)
        logger.info("all entity import[{}],re={}".format(schema, re))

    # ####3.mySql/oracle/pg的外键关系转成元数据实体关系。
    if step.get("4") is not None:
        re=None
        if db_type == 'mysql':
            re = mysql.reverse_constraint(user_id, tenant_id, schema, tables_list)
        elif db_type == 'oracle':
            # re = ora.reverse_constraint(user_id, tenant_id, schema, tables_list)
            pass
        elif db_type == 'pg':
            # re = pg.reverse_constraint(user_id, tenant_id, schema, tables_list)
            pass

        logger.info("all tables in[{}],re={}".format(schema, re))

    # ####3.1.erwin的外键关系转成元数据实体关系。
    if step.get("5") is not None:
        re = emg.reverse_constraint(user_id, tenant_id, schema, file_name)
        logger.info("all rels in[{}],re={}".format(schema, re))

    # ####4.元数据对象生成Neo4J图数据库信息。
    if step.get("6") is not None:
        entity_code_list = ["xx_Lifecycle", "xx_Rel"]
        entity_catagory = 'XXX'  # 分类，增加一大类标签。
        # entity_code_list = None 为None，则初始化全部实体。
        re = mdi.ini_entity_model_graph(tenant_id, entity_code_list, entity_catagory, schema)

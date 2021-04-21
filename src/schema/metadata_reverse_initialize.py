# ######metadata_reverse_initialize.py
from schema import schema_mysql as mysql, schema_oracle as ora, schema_pg as pg
from mdata import metadata_initialize as mdi, metadata as md
from config.config import cfg as config
from model import erwin_model_graph as emg
from privilege import data_privilege as dp, role_privilege as rp, user_mngt as ur

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
    #       "6":"元数据对象生成Neo4J图数据库信息",
    #       "7":"权限码单独补充初始化"}
    step = {
        # "2": "从mysql/oracle/pg数据库反向工程，初始化表和字段元数据",
        # "3": "从数据表和字段元数据，初始化生成实体和属性元数据",
        "4": "mySql/oracle/pg的外键关系转成元数据实体关系",
          # "7":"权限码单独补充初始化"
    }

    # ##### 1.初始化表结构从erWin文件(注意文件路径写法d:/downloads/eSpace_File/xxx.erwin)。
    file_name = "d:/downloads/eSpace_File/123-new.erwin"
    if step.get("1") is not None:
        re = emg.reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name)
        logger.info("all tables in[{}],re={}".format(schema, re))

    # ####1.2.从mysql/oracle/pg数据库反向工程，初始化表和字段元数据
    tables_list = ['index_mapping_t', 'index_date_t', 'index_decimal_t','index_text_t','index_int_t']
    if step.get("2") is not None:
        re = None
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
        entity_list = [{"entity_code": "ui_template", "table_name": "ui_template"},
                       {"entity_code": "ui_entity_rel", "table_name": "ui_entity_rel"},
                       {"entity_code": "ui_fields", "table_name": "ui_fields"}]
        re = mdi.initialize_md_entities_from_tables(user_id, tenant_id, entity_list)
        logger.info("all entity import[{}],re={}".format(schema, re))

    # ####3.mySql/oracle/pg的外键关系转成元数据实体关系。
    if step.get("4") is not None:
        re = None
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

    if step.get("7") is not None:
        # 插入到元数据实体表或者数据视图表，就要增加权限码；以及创建默认的实体字段，即填写不为空的字段（包括主键ID）。
        entity_type = "Entity"  # Entity或者View
        entity_codes = ['index_date_t','index_decimal_t','index_int_t']
        res = md.get_md_entities_id_by_code(entity_codes)
        ids = []
        if res is not None and len(res) > 0:
            for item in res:
                ids.append(item.get("md_entity_id"))

        # 角色权限
        re = rp.insert_entity_privilege(user_id, tenant_id, entity_type, ids)
        logger.info("insert_entity_privilege, entity:[{}],re={}".format(entity_codes, re))
        # 数据范围权限
        re = dp.insert_data_privilege(user_id, tenant_id, entity_type, ids)
        logger.info("insert_data_privilege, entity:[{}],re={}".format(entity_codes, re))

# ####erwin_model_graph.py
# # erwin文件反向工程，生成元数据存入表。
from config.config import cfg as config
from schema import metadata_eng_reverse as mdr
from mdata import metadata_initialize as mdi
from privilege import user_mngt as ur
import win32com.client

logger = config.logger
# 所有外键关系
all_rel_ref_list = []
# 所有Key信息
all_key_list = []


def read_erwin_file(filename, rel_only=False):
    # 源文件
    # filename = "D:\WorkDir\项目工作\合同中心\Contract_New202003.erwin"
    global all_rel_ref_list, all_key_list
    all_rel_ref_list = []
    all_key_list = []
    # 创建COM对象
    scapi = win32com.client.Dispatch('AllFusionERwin.SCAPI')
    # scapi=win32com.client.Dispatch('ADODB.Connection')
    # 建立与持久装置中模型的连接
    scPUnit = scapi.PersistenceUnits.Add(filename, "RDO=yes")
    # 建立存取内存中模型数据的连接
    scSession = scapi.Sessions.Add()
    scSession.Open(scPUnit, 0, 0)
    # 事务控制
    # scTranId = scSession.BeginTransaction()
    # 获取所有对象Relationship
    # scRObjects = scSession.ModelObjects.Collect(scSession.ModelObjects.Root, 'Relationship', 1)
    # 获取所有Entity模型对象
    scMObjects = scSession.ModelObjects.Collect(scSession.ModelObjects.Root, 'Entity', 1)
    all_columns_list = []
    all_table_list = []
    for scObj in scMObjects:
        # 产生table的元数据
        (schema, table_name, table_comment, tables_dict) = generate_Tables(scObj)
        if tables_dict is not None:
            all_table_list.append(tables_dict)
        logger.info("table mapping done,table_name={}".format(table_name))
        # 获取该Entity的所有Attribute对象
        scAttrObjects = scSession.ModelObjects.Collect(scObj, 'Attribute', 1)
        # 获取该Entity的所有key对象
        sckeyObjects = scSession.ModelObjects.Collect(scObj, 'Key_Group', 1)
        key_list = None
        for sckeyObject in sckeyObjects:
            pk = sckeyObject.Properties('Key_Group_Type').Value
            if pk is not None and pk == 'PK':
                sckeys = scSession.ModelObjects.Collect(sckeyObject, 'Key_Group_Member', 1)
                if sckeys is not None:
                    key_list = generate_key_list(schema, sckeys, table_name, table_comment)
        all_columns_list += generate_attributes(scAttrObjects, schema, table_name, table_comment, key_list, rel_only)

    return all_table_list, all_columns_list


def generate_key_list(schema, sckeys, table_name, table_comment):
    global all_key_list
    key_list = []
    for key in sckeys:
        # key_name = key.Properties('Name').Value
        key_name = key.Properties('Physical_Name').Value
        key_ref = key.Properties('Attribute_Ref').Value
        key_list.append(key_name)
        key_dict = {}
        key_dict["TABLE_SCHEMA"] = schema
        key_dict["TABLE_NAME"] = table_name
        key_dict["TABLE_COMMENT"] = table_comment
        key_dict["COLUMN_NAME"] = key_name
        key_dict["LONG_ID"] = key_ref
        all_key_list.append(key_dict)
    return key_list


def generate_relationship(tenant_id,file_name):
    global all_rel_ref_list, all_key_list
    read_erwin_file(file_name, True)
    if all_rel_ref_list is None or all_key_list is None:
        return None
    rel_list = []
    rel_key_list = []
    table_names = []
    for key in all_key_list:
        key_table_name = key.get("TABLE_NAME")
        if table_names.count(key_table_name) <= 0:
            table_names.append(key_table_name)
    entity_dict = get_entity_mapping(tenant_id, table_names)

    for item in all_rel_ref_list:
        # schema = item.get("TABLE_SCHEMA")
        table_name = item.get("TABLE_NAME")
        # table_comment = item.get("TABLE_COMMENT")
        col_name = item.get("COLUMN_NAME")
        col_id = item.get("REL_ATTR_REF")
        for key in all_key_list:
            # key_schema = key.get("TABLE_SCHEMA")
            key_table_name = key.get("TABLE_NAME")
            if key_table_name is None:
                continue
            key_table_comment = key.get("TABLE_COMMENT")
            key_name = key.get("COLUMN_NAME")
            key_id = key.get("LONG_ID")
            if key_id == col_id:
                item["REF_TABLE_NAME"] = key_table_name
                item["REF_TABLE_COMMENT"] = key_table_comment
                item["REF_COLUMN_NAME"] = key_name
                entity_fields_from = entity_dict.get(key_table_name)
                frm_field = get_entity_field_by_name(entity_fields_from, key_name)
                entity_fields_to = entity_dict.get(table_name)
                to_field = get_entity_field_by_name(entity_fields_to, col_name)
                if frm_field is None or to_field is None:
                    continue
                entity_dict1 = {}
                entity_dict1["rel_type"] = "1:N"
                frm_f = frm_field.get("md_fields_id")
                to_f = to_field.get("md_fields_id")
                entity_dict1["to_entity_id"] = to_field.get("md_entity_id")
                entity_dict1["to_field_id"] = to_f
                entity_dict1["from_entity_id"] = frm_field.get("md_entity_id")
                entity_dict1["from_field_id"] = frm_f
                rel_name = to_field.get("md_entity_name") + " AND " + frm_field.get("md_entity_name") + " RELATION"
                entity_dict1["md_entity_rel_desc"] = rel_name
                entity_dict1["active_flag"] = "Y"
                s1 = str(frm_f) if frm_f is not None else ""
                s2 = "-" + str(to_f) if to_f is not None else ""
                s = s1 + s2
                if rel_key_list is not None and rel_key_list.count(s) > 0:
                    continue
                rel_key_list.append(s)
                rel_list.append(entity_dict1)
                logger.info("generate entity relation from erwin,rel_name={}".format(rel_name))
                break
    return rel_list


def get_entity_field_by_name(fields, field_name):
    if fields is None:
        return None
    for item in fields:
        md_field_name = item.get("md_fields_name")
        if field_name is not None and field_name == md_field_name:
            return item

    return None


def get_entity_mapping(tenant_id, table_names):
    entities = mdi.query_entity_by_tenant(tenant_id, table_names)
    entity_dict = {}
    for item in entities:
        md_entity_code = item.get("md_tables_name")
        ent = entity_dict.get(md_entity_code)
        if ent is None:
            ls = []
            ls.append(item)
            entity_dict[md_entity_code] = ls
        else:
            ent.append(item)
    return entity_dict


def generate_Tables(scObj):
    schema = ""
    table_name = ""
    tables_dict = {}
    try:
        # table_name = scObj.Properties('Name').Value
        table_name = scObj.Properties('Physical_Name').Value
    except Exception as ex:
        logger.warning("generate table name failed,obj={}".format(scObj))
        return (schema, table_name, None)
    # 取Definition属性的值
    try:
        scDefineName = scObj.Properties('Definition').Value
        schema = scObj.Properties('Schema_Name').Value
    except Exception as ex:
        scDefineName = ''
    # 对象名赋值
    tables_dict["TABLE_NAME"] = table_name
    table_comment = scDefineName
    tables_dict["TABLE_COMMENT"] = table_comment
    tables_dict["TABLE_SCHEMA"] = schema
    # tables_list.append(tables_dict)
    return (schema, table_name, table_comment, tables_dict)


# 产生属性对象
def generate_attributes(scAttrObjects, schema, table_name, table_comment, key_list, rel_only=False):
    global all_rel_ref_list
    columns_list = []
    fields_list = []
    is_null = None
    for scAttrObj in scAttrObjects:
        col_dict = {}
        try:
            scAttrName = scAttrObj.Properties('Physical_Name').Value
            if scAttrName is None or len(scAttrName.strip()) <= 0 or scAttrName == "%AttName":
                scAttrName = scAttrObj.Properties('Name').Value
        except Exception as ex:
            scAttrName = ''
            continue
        data_type, is_key, long_Id = None, None, None
        try:
            if rel_only:
                if scAttrObj.Properties('Parent_Attribute_Ref') is not None:
                    parent_attr_ref = scAttrObj.Properties('Parent_Attribute_Ref').Value
                    parent_rel_ref = scAttrObj.Properties('Parent_Relationship_Ref').Value
                    rel_ref = generate_rel_infos(table_name, scAttrName, parent_rel_ref, parent_attr_ref)
                    all_rel_ref_list.append(rel_ref)
                    if rel_only:
                        continue
        except:
            parent_attr_ref = ""

        try:
            scAttrDefineName = scAttrObj.Properties('Definition').Value
        except:
            scAttrDefineName = ""

        try:
            data_type = scAttrObj.Properties('Physical_Data_Type').Value
            # long_Id = scAttrObj.Properties('Long_Id').Value
            if data_type is None or len(data_type.strip()) <= 0:
                data_type = scAttrObj.Properties('Logical_Data_Type').Value
            is_key = ''
            if key_list is not None:
                for pk_item in key_list:
                    if pk_item == scAttrName:
                        is_key = 'PRI'
                        break
            is_null = scAttrObj.Properties('Null_Option_Type').Value
        except Exception as ex:
            data_type = ""
            is_null = "Y"
            is_key = ""
            logger.info("generate_attributes exception,{}".format(ex))
            # 对象名赋值
        # scAttrObj.Properties('Physical_Name').Value = scAttrName
        col_dict["TABLE_SCHEMA"] = schema
        col_dict["TABLE_NAME"] = table_name
        col_dict["TABLE_COMMENT"] = table_comment
        col_dict["COLUMN_NAME"] = scAttrName
        col_dict["COLUMN_COMMENT"] = scAttrDefineName
        new_type, precision, scale = convert_numberic(data_type)
        col_dict["DATA_TYPE"] = new_type
        col_dict["NUMERIC_PRECISION"] = precision
        col_dict["NUMERIC_SCALE"] = scale
        # col_dict["LONG_ID"] = long_Id
        is_null_flag = 'Y'
        if is_null is not None and is_null == 1:
            is_null_flag = 'N'
        col_dict["IS_NULLABLE"] = is_null_flag
        col_dict["COLUMN_KEY"] = is_key
        columns_list.append(col_dict)
        fields_list.append(scAttrName)
    logger.info("fields mapping done,table_name={},fied_name_list={}".format(table_name, fields_list))

    return columns_list


def generate_rel_infos(table_name, attr_name, parent_rel_ref, parent_attr_ref):
    obj = {}
    obj["TABLE_NAME"] = table_name
    obj["COLUMN_NAME"] = attr_name
    obj["REL_OBJ_REF"] = parent_rel_ref
    obj["REL_ATTR_REF"] = parent_attr_ref
    return obj


def convert_numberic(type):
    new_type = type
    precision = None
    scale = None
    if type is not None and type.count("(") > 0:
        icount = type.index("(")
        new_type = type[:icount]
        if type.count(",") > 0:
            i_d = type.index(",")
            s = type[icount + 1:i_d]
            precision = int(s.strip())
            if type.count(")") > 0:
                i_e = type.index(")")
                s = type[i_d + 1:i_e]
                try:
                    scale = int(s.strip())
                except:
                    scale = 0
        else:
            if type.count(")") > 0:
                i_e = type.index(")")
                s = type[icount + 1:i_e]
                try:
                    precision = int(s.strip())
                except:
                    precision = 0

    return new_type, precision, scale


##1.初始化表和字段信息，反向从erwin文件
def reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name):
    tables, columns = read_erwin_file(file_name)
    re = mdr.intialize_md_tables_from_schema(user_id, tenant_id, database_name, schema, tables, columns)
    return re


##2.初始化实体关系，反向从数据库的外键关系（前提：entity和fields等元数据已经生成）
def reverse_constraint(user_id, tenant_id, schema, file_name):
    const_list = generate_relationship(tenant_id,file_name)
    re = mdr.intialize_entity_rel_from_schema(user_id, tenant_id, schema, const_list, True)
    return re


if __name__ == '__main__':
    user = ur.get_user("admin")
    user_id = user.get("user_id")
    tenant_id = user.get("tenant_id")
    schema = "common"
    database_name = "mysql"
    # 数据库类类型mysql/oracle/pb
    db_type = 'mysql'

    # ##### 1.初始化表结构从erWin文件(注意文件路径写法d:/downloads/eSpace_File/xxx.erwin)。
    file_name = "d:/downloads/eSpace_File/123-new.erwin"
    # re = reverse_tables_columns(user_id, tenant_id, database_name, schema, file_name)
    # logger.info("all tables in[{}],re={}".format(schema, re))

    # ####4.元数据对象生成Neo4J图数据库信息。
    entity_code_list = ["xx_Lifecycle", "xx_Rel"]
    entity_catagory = 'XXX'  # 分类，增加一大类标签。
    # entity_code_list = None 为None，则初始化全部实体。
    # re = mdi.ini_entity_model_graph(tenant_id, entity_code_list, entity_catagory, schema)

import sqlite3
import typing
import pandas as pd
import json

import ast


class SqliteTools:

    def __init__(self, db_path, check_same_thread=False, isolation_level=None, timeout=10):
        self.db_path = db_path
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=check_same_thread,
            isolation_level=isolation_level,
            timeout=timeout
        )
        self.cursor = self.conn.cursor()

    def sort_table_values(self, table_name: str, table_fields: dict) -> list:
        data = []
        for table_name in self.table_fields(table_name):
            value = table_fields.get(table_name)
            if isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            data.append(value)
        return data

    def to_list(self, sql, params=None) -> list:
        if params:
            res = pd.read_sql_query(sql, self.conn, params=params).to_dict(orient="records", into=dict)
        else:
            res = pd.read_sql_query(sql, self.conn).to_dict(orient="records", into=dict)
        if res:
            for i in res:
                for k, v in i.items():
                    if isinstance(v, str):
                        if (v.startswith("[") and v.endswith("]")) or \
                                (v.startswith("{") and v.endswith("}")):
                            try:
                                i[k] = ast.literal_eval(v)
                            except Exception as e:
                                print("json解析失败:", e, "value:", v)
            return res

    def table_fields(self, table_name):
        return [i[1] for i in self.cursor.execute(f"PRAGMA table_info({table_name})")]

    def create_table(self, table_name: str, table_fields, key: str = "id"):
        sql = f"create table if not exists {table_name} ("
        for field in table_fields:
            if field == key:  # 如果是id字段则设置为主键
                sql += f"{field} TEXT PRIMARY KEY,"
            else:
                sql += f"'{field}' TEXT,"
        sql = sql[:-1] + ")"
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, table_fields: dict):
        sql = f"insert into {table_name} values ("
        for field in table_fields.keys():
            sql += "?,"

        sql = sql[:-1] + ")"
        # 获取数据库列名称
        try:
            self.cursor.execute(sql, self.sort_table_values(table_name, table_fields))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("主键冲突:", e)

    def insert_many(self, table_name, data: typing.List[dict]):
        sql = f"insert into {table_name} values ("

        for field in self.table_fields(table_name):
            sql += "?,"
        sql = sql[:-1] + ")"

        data_list = []
        for table_fields in data:
            data_list.append(self.sort_table_values(table_name, table_fields))

        self.cursor.executemany(sql, data_list)
        self.conn.commit()

    def insert_and_update(self, table_name, table_fields: dict):
        sql = f"insert or replace into {table_name} values ("

        for field in table_fields.keys():
            sql += "?,"
        sql = sql[:-1] + ")"

        try:
            self.cursor.execute(sql, self.sort_table_values(table_name, table_fields))
        except sqlite3.IntegrityError as e:
            print("主键冲突:", e)
        self.conn.commit()

    def select(self, table_name: str, where: dict, values: dict = None):
        sql = f"select * from {table_name}"
        if where:
            sql += f" where "
            for field in where.keys():
                if isinstance(where[field], str):
                    sql += f"{field} = '{where[field]}' and "
                elif isinstance(where[field], int):
                    sql += f"{field} = {where[field]} and "
                else:
                    raise TypeError(f"不支持的类型:{type(where[field])}")
            sql = sql[:-4]
        if values:
            if values.get("order"):
                sql += f" order by {values.get('order')}"
            if values.get("limit"):
                sql += f" limit {values['limit']}"
            if values.get("offset"):
                sql += f" offset {values['offset']}"
        sql += ";"
        return self.to_list(sql)

    def update(self, table_name, update_fields: dict, where: dict):
        sql = f"update {table_name} set "
        for field in update_fields.keys():
            sql += f"{field} = '{update_fields[field]}',"
        sql = sql[:-1]
        for field in where.keys():
            sql += f" where {field} = {where[field]}"
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def delete(self, table_name, where=None):
        sql = f"delete from {table_name} "

        if where:
            sql += f"where {where}"

        self.cursor.execute(sql)
        self.conn.commit()

    def get(self, table_name, value: str, key: str = "id"):
        try:
            res = self.select(table_name, {key: value}, None)
            return res[0]
        except (IndexError, TypeError):
            return None

    def get_all(self, table_name):
        sql = f"select * from {table_name}"
        return self.to_list(sql)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

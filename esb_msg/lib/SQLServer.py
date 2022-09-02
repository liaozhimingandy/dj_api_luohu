# coding=utf-8
import pymssql
from pymssql import OperationalError
from pymssql._mssql import MSSQLDatabaseException


class SQLServer:
    def __init__(self, server, user, password, database):
        # 类的构造函数，初始化DBC连接信息
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cur = None

    def __get_connect(self):
        # 得到数据库连接信息，返回conn.cursor()
        if not self.database:
            raise (NameError, "没有设置数据库信息")

        # 连接不存在时创建,明显提高速度
        try:
            self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password,
                                        database=self.database, login_timeout=3)
        except (MSSQLDatabaseException, OperationalError) as e:
            raise MSSQLDatabaseException("连接数据库失败")

        # raise (NameError, "连接数据库失败")
        self.cur = self.conn.cursor()

    def exec_query(self, sql):
        """
        执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """
        if not self.cur:
            self.__get_connect()
        self.cur.execute(sql)  # 执行查询语句
        result = self.cur.fetchall()  # fetchall()获取查询结果
        # 查询完毕关闭数据库连接
        # self.conn.close()
        return result

    def exec_update(self, sql, value):
        """
        执行执行语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """
        if not self.cur:
            self.__get_connect()
        self.cur.execute(sql, value)  # 执行更新语句
        # 提交事务
        self.conn.commit()
        # 对象销毁时,关闭数据库连接
        # self.conn.close()
        return

    def __del__(self):
        """对象销毁时触发"""
        if self.cur:
            self.cur.close()
        # 对象销毁时,关闭数据库连接
        if self.conn:
            self.conn.close()


def main():
    msg = SQLServer(server="172.16.33.183", user="sa", password="Knt2020@lh", database="ESB_MSG-B")
    result = msg.exec_query(
        "SELECT TOP 1 * FROM MessageTagList")
    for item in result:
        print(item)


if __name__ == '__main__':
    main()

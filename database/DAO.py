from database.DB_connect import DBConnect
from model.product import Product
from model.method import Method


class DAO():

    @staticmethod
    def getMethods():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM go_methods"""
        cursor.execute(query,)
        for row in cursor:
            result.append(Method(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(extract(year from `Date`)) as anni
                    from go_daily_sales gds """
        cursor.execute(query, )
        for row in cursor:
            result.append(row['anni'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProduct():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_products"""
        cursor.execute(query, )
        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(idMap, metodo, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct (Product_number)
                    from go_daily_sales gds
                    where Order_method_code = %s and extract(year from gds.`Date`) = %s """
        cursor.execute(query, (metodo, anno,))
        for row in cursor:
            if idMap[row['Product_number']] is not None:
                result.append((idMap[row['Product_number']]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(metodo, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select p1, p2, ricavoTot1, ricavoTot2
                    from (select gds.Product_number as p1, SUM(gds.Unit_sale_price * gds.Quantity) as ricavoTot1
                            from go_daily_sales gds
                            where gds.Order_method_code = %s and extract(year from gds.`Date`) = %s
                            group by gds.Product_number) t1,
                            (select gds.Product_number as p2, SUM(gds.Unit_sale_price * gds.Quantity) as ricavoTot2
                                from go_daily_sales gds
                                where gds.Order_method_code = %s and extract(year from gds.`Date`) = %s
                                group by gds.Product_number) t2
                    where t1.p1 != t2.p2"""
        cursor.execute(query, (metodo, anno, metodo, anno,))
        for row in cursor:
            result.append((row['p1'],
                           row['p2'],
                           row['ricavoTot1'],
                           row['ricavoTot2']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRicavo(metodo, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gds.Product_number as p1, SUM(gds.Unit_sale_price * gds.Quantity) as ricavoTot1
                    from go_daily_sales gds, go_products p
                    where gds.Order_method_code = %s and extract(year from gds.`Date`) = %s and gds.Product_number = p.Product_number
                    group by p.Product_number"""
        cursor.execute(query, (metodo, anno))
        for row in cursor:
            result.append((row['p1'],
                           row['ricavoTot1']))

        cursor.close()
        conn.close()
        return result


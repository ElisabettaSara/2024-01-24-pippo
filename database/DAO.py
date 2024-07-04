from database.DB_connect import DBConnect
from model.product import Product
from model.method import Method


class DAO():

    @staticmethod
    def getMetodo():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select Order_method_type as tipo
                    from go_methods gm """
        cursor.execute(query, )
        for row in cursor:
            result.append(row["tipo"])

        cursor.close()
        conn.close()
        return result




    @staticmethod
    def getAnno():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(`Date` ) as anno
                    from go_daily_sales gds  """
        cursor.execute(query, )
        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProdotti(metodo, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select Product_number as prodotto
                    from go_daily_sales gds, go_methods gm 
                    where gm.Order_method_type = %s
                    and gm.Order_method_code = gds.Order_method_code 
                    and year(gds.`Date`)=%s"""
        cursor.execute(query, (metodo, anno,) )
        for row in cursor:
            result.append(row["prodotto"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPrezzi(metodo, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select Product_number as prodotto, sum(Quantity*Unit_sale_price) as ricavo  
                        from go_daily_sales gds, go_methods gm 
                        where gm.Order_method_type = %s
                        and gm.Order_method_code = gds.Order_method_code 
                        and year(gds.`Date`)=%s
                        group by Product_number"""
        cursor.execute(query, (metodo, anno,))
        for row in cursor:
            result.append((row["prodotto"], row["ricavo"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(metodo, anno,soglia):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select 	gds1.p1 as p1, gds2.p2 as p2, gds1.ricavoTot1 as ricavoTot1, gds2.ricavoTot2 as ricavoTot2
                    from (select gds.Product_number as p1, sum(gds.Unit_sale_price * gds.Quantity) as ricavoTot1
                        from go_daily_sales gds, go_methods gm 
                        where gds.Order_method_code = gm.Order_method_code and year(gds.`Date`) = %s and gm.Order_method_type =%s
                        group by gds.Product_number) gds1,
                        (select gds.Product_number as p2, sum(gds.Unit_sale_price * gds.Quantity) as ricavoTot2
                        from go_daily_sales gds, go_methods gm 
                        where gds.Order_method_code = gm.Order_method_code and year(gds.`Date`) = %s and gm.Order_method_type =%s
                        group by gds.Product_number) gds2
                    where gds1.p1 != gds2.p2 and gds1.ricavoTot1*(1+%s)<gds2.ricavoTot2"""
        cursor.execute(query, (anno, metodo, anno, metodo,soglia,))
        for row in cursor:
            result.append((row["p1"], row["p2"], row["ricavoTot1"], row["ricavoTot2"]))

        cursor.close()
        conn.close()
        return result






from models.database import DatabaseManager

class CategoryService:
    def __init__(self):
        self.db = DatabaseManager()

    #获取分类列表
    def get_categories(self, trans_type=None):
        query = "SELECT * FROM categories"
        params = []

        if trans_type:
            query += " WHERE type=?"
            params.append(trans_type)
        query += " ORDER BY type,name"
        return self.db.fetchall(query, params)

    def add_category(self,name,trans_type,color="#000000"):
        query = "INSERT INTO categories(name,type,color) VALUES(?,?,?)"
        self.db.execute_query(query,(name,trans_type,color))

    def delete_category(self,category_id):
        query = "DELETE FROM categories WHERE id=?"
        self.db.execute_query(query,(category_id,))


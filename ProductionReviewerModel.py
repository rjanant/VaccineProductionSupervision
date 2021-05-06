from Constants import connString
import pyodbc
class ProductionReviewerModel:
    # instance attribute
    def __init__(self, production_reviewer_id, production_reviewer_name="", is_active=False):
        self.production_reviewer_id = production_reviewer_id
        self.production_reviewer_name = production_reviewer_name
        self.is_active = is_active

    @staticmethod
    def get_all_production_reviewers():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionReviewerMaster ORDER BY productionReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = ProductionReviewerModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_production_reviewers_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT productionReviewerID, productionReviewerName FROM ProductionReviewerMaster WHERE isActive = 1 ORDER BY productionReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = ProductionReviewerModel(dbrow[0], dbrow[1])
            records.append(row)
        return records

    @staticmethod
    def get_production_reviewer_by_id(production_reviewer_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionReviewerMaster WHERE productionReviewerID = ?"
        cursor.execute(sqlcmd1, production_reviewer_id)
        record = None

        for dbrow in cursor.fetchall():
            record = ProductionReviewerModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_production_reviewer(production_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ProductionReviewerMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (production_reviewer_obj.production_reviewer_id,
                       production_reviewer_obj.production_reviewer_name,
                       production_reviewer_obj.is_active))

    @staticmethod
    def update_production_reviewer(production_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ProductionReviewerMaster SET productionReviewerName = ?, " \
                  "isActive = ? WHERE productionReviewerID = ?"
        cursor.execute(sqlcmd1, (production_reviewer_obj.production_reviewer_name,
                       production_reviewer_obj.is_active, production_reviewer_obj.production_reviewer_id))

    @staticmethod
    def delete_production_reviewer(production_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ProductionReviewerMaster WHERE productionReviewerID = ?"
        cursor.execute(sqlcmd1, (production_reviewer_obj.production_reviewer_id))



from Constants import connString
import pyodbc
class PackingReviewerModel:
    # instance attribute
    def __init__(self, packing_reviewer_id, packing_reviewer_name="", is_active=False):
        self.packing_reviewer_id = packing_reviewer_id
        self.packing_reviewer_name = packing_reviewer_name
        self.is_active = is_active

    @staticmethod
    def get_all_packing_reviewers():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM packingReviewerMaster ORDER BY packingReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = PackingReviewerModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_packing_reviewers_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT packingReviewerID, packingReviewerName FROM packingReviewerMaster WHERE isActive = 1 ORDER BY packingReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = PackingReviewerModel(dbrow[0], dbrow[1])
            records.append(row)
        return records

    @staticmethod
    def get_packing_reviewer_by_id(packing_reviewer_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM packingReviewerMaster WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1, packing_reviewer_id)
        record = None

        for dbrow in cursor.fetchall():
            record = PackingReviewerModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_packing_reviewer(packing_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        print("process_packing_reviewer_operation4444")
        sqlcmd1 = "INSERT INTO packingReviewerMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (packing_reviewer_obj.packing_reviewer_id,
                       packing_reviewer_obj.packing_reviewer_name,
                       packing_reviewer_obj.is_active))
        print("process_packing_reviewer_operation5555")

    @staticmethod
    def update_packing_reviewer(packing_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE packingReviewerMaster SET packingReviewerName = ?, " \
                  "isActive = ? WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1, (packing_reviewer_obj.packing_reviewer_name,
                       packing_reviewer_obj.is_active, packing_reviewer_obj.packing_reviewer_id))

    @staticmethod
    def delete_packing_reviewer(packing_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM packingReviewerMaster WHERE packingReviewerID = ?"
        cursor.execute(sqlcmd1, (packing_reviewer_obj.packing_reviewer_id))



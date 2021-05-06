from Constants import connString
import pyodbc
class InspectionReviewerModel:
    # instance attribute
    def __init__(self, inspection_reviewer_id, inspection_reviewer_name="", is_active=False):
        self.inspection_reviewer_id = inspection_reviewer_id
        self.inspection_reviewer_name = inspection_reviewer_name
        self.is_active = is_active

    @staticmethod
    def get_all_inspection_reviewers():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InspectionReviewerMaster ORDER BY InspectionReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = InspectionReviewerModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_inspection_reviewers_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT InspectionReviewerID, InspectionReviewerName FROM InspectionReviewerMaster WHERE isActive = 1 ORDER BY InspectionReviewerName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = InspectionReviewerModel(dbrow[0], dbrow[1])
            records.append(row)
        return records

    @staticmethod
    def get_inspection_reviewer_by_id(inspection_reviewer_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InspectionReviewerMaster WHERE InspectionReviewerID = ?"
        cursor.execute(sqlcmd1, inspection_reviewer_id)
        record = None

        for dbrow in cursor.fetchall():
            record = InspectionReviewerModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_inspection_reviewer(inspection_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO InspectionReviewerMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (inspection_reviewer_obj.inspection_reviewer_id,
                       inspection_reviewer_obj.inspection_reviewer_name,
                       inspection_reviewer_obj.is_active))

    @staticmethod
    def update_inspection_reviewer(inspection_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE InspectionReviewerMaster SET InspectionReviewerName = ?, " \
                  "isActive = ? WHERE InspectionReviewerID = ?"
        cursor.execute(sqlcmd1, (inspection_reviewer_obj.inspection_reviewer_name,
                       inspection_reviewer_obj.is_active, inspection_reviewer_obj.inspection_reviewer_id))

    @staticmethod
    def delete_inspection_reviewer(inspection_reviewer_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM InspectionReviewerMaster WHERE InspectionReviewerID = ?"
        cursor.execute(sqlcmd1, (inspection_reviewer_obj.inspection_reviewer_id))



from Constants import connString
import pyodbc
class InspectionInChargeModel:
    # instance attribute
    def __init__(self, inspection_in_charge_id, inspection_in_charge_name="", is_active=False):
        self.inspection_in_charge_id = inspection_in_charge_id
        self.inspection_in_charge_name = inspection_in_charge_name
        self.is_active = is_active

    @staticmethod
    def get_all_inspection_in_charges():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM inspectionInChargeMaster ORDER BY inspectionInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = InspectionInChargeModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_inspection_in_charges_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT inspectionInChargeID, inspectionInChargeName FROM inspectionInChargeMaster WHERE isActive = 1 ORDER BY inspectionInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = InspectionInChargeModel(dbrow[0], dbrow[1])
            records.append(row)

        return records

    @staticmethod
    def get_inspection_in_charge_by_id(inspection_in_charge_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM inspectionInChargeMaster WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1, inspection_in_charge_id)
        record = None

        for dbrow in cursor.fetchall():
            record = InspectionInChargeModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_inspection_in_charge(inspection_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO inspectionInChargeMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (inspection_in_charge_obj.inspection_in_charge_id,
                       inspection_in_charge_obj.inspection_in_charge_name,
                       inspection_in_charge_obj.is_active))

    @staticmethod
    def update_inspection_in_charge(inspection_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE inspectionInChargeMaster SET inspectionInChargeName = ?, " \
                  "isActive = ? WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1, (inspection_in_charge_obj.inspection_in_charge_name,
                       inspection_in_charge_obj.is_active, inspection_in_charge_obj.inspection_in_charge_id))

    @staticmethod
    def delete_inspection_in_charge(inspection_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM inspectionInChargeMaster WHERE inspectionInChargeID = ?"
        cursor.execute(sqlcmd1, (inspection_in_charge_obj.inspection_in_charge_id))



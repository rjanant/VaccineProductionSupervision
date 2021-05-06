from Constants import connString
import pyodbc
class PackingInChargeModel:
    # instance attribute
    def __init__(self, packing_in_charge_id, packing_in_charge_name="", is_active=False):
        self.packing_in_charge_id = packing_in_charge_id
        self.packing_in_charge_name = packing_in_charge_name
        self.is_active = is_active

    @staticmethod
    def get_all_packing_in_charges():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM packingInChargeMaster ORDER BY packingInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = PackingInChargeModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_packing_in_charges_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT packingInChargeID, packingInChargeName FROM packingInChargeMaster WHERE isActive = 1 ORDER BY packingInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = PackingInChargeModel(dbrow[0], dbrow[1])
            records.append(row)

        return records

    @staticmethod
    def get_packing_in_charge_by_id(packing_in_charge_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM packingInChargeMaster WHERE packingInChargeID = ?"
        cursor.execute(sqlcmd1, packing_in_charge_id)
        record = None

        for dbrow in cursor.fetchall():
            record = PackingInChargeModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_packing_in_charge(packing_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO packingInChargeMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (packing_in_charge_obj.packing_in_charge_id,
                       packing_in_charge_obj.packing_in_charge_name,
                       packing_in_charge_obj.is_active))

    @staticmethod
    def update_packing_in_charge(packing_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE packingInChargeMaster SET packingInChargeName = ?, " \
                  "isActive = ? WHERE packingInChargeID = ?"
        cursor.execute(sqlcmd1, (packing_in_charge_obj.packing_in_charge_name,
                       packing_in_charge_obj.is_active, packing_in_charge_obj.packing_in_charge_id))

    @staticmethod
    def delete_packing_in_charge(packing_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM packingInChargeMaster WHERE packingInChargeID = ?"
        cursor.execute(sqlcmd1, (packing_in_charge_obj.packing_in_charge_id))



from Constants import connString
import pyodbc
class ProductionInChargeModel:
    # instance attribute
    def __init__(self, production_in_charge_id, production_in_charge_name="", is_active=False):
        self.production_in_charge_id = production_in_charge_id
        self.production_in_charge_name = production_in_charge_name
        self.is_active = is_active

    @staticmethod
    def get_all_production_in_charges():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionInChargeMaster ORDER BY productionInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = ProductionInChargeModel(dbrow[0], dbrow[1], dbrow[2])
            records.append(row)
        return records

    @staticmethod
    def get_all_production_in_charges_id_names():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT productionInChargeID, productionInChargeName FROM ProductionInChargeMaster WHERE isActive = 1 ORDER BY productionInChargeName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():
            row = ProductionInChargeModel(dbrow[0], dbrow[1])
            records.append(row)

        return records

    @staticmethod
    def get_production_in_charge_by_id(production_in_charge_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionInChargeMaster WHERE productionInChargeID = ?"
        cursor.execute(sqlcmd1, production_in_charge_id)
        record = None

        for dbrow in cursor.fetchall():
            record = ProductionInChargeModel(dbrow[0], dbrow[1], dbrow[2])
        return record

    @staticmethod
    def insert_production_in_charge(production_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ProductionInChargeMaster VALUES(?,?,?)"
        cursor.execute(sqlcmd1, (production_in_charge_obj.production_in_charge_id,
                       production_in_charge_obj.production_in_charge_name,
                       production_in_charge_obj.is_active))

    @staticmethod
    def update_production_in_charge(production_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ProductionInChargeMaster SET productionInChargeName = ?, " \
                  "isActive = ? WHERE productionInChargeID = ?"
        cursor.execute(sqlcmd1, (production_in_charge_obj.production_in_charge_name,
                       production_in_charge_obj.is_active, production_in_charge_obj.production_in_charge_id))

    @staticmethod
    def delete_production_in_charge(production_in_charge_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ProductionInChargeMaster WHERE productionInChargeID = ?"
        cursor.execute(sqlcmd1, (production_in_charge_obj.production_in_charge_id))



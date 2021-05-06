from Constants import connString
import pyodbc
import time
class ProductionModel:
    def __init__(self, production_id, company_name="", vaccine_name="", production_batch_no="",
                 production_date_time=None,
                 raw_materials="", auxiliary_materials="", production_equipment_parameters="", abnormal_record="",
                 investigation_report="", expiry_date_time=None, actual_weight=0, production_in_charge="",
                 production_reviewer=""):
        self.production_id = production_id
        self.company_name = company_name
        self.vaccine_name = vaccine_name
        self.production_batch_no = production_batch_no
        self.production_date_time = production_date_time
        self.raw_materials = raw_materials
        self.auxiliary_materials = auxiliary_materials
        self.production_equipment_parameters = production_equipment_parameters
        self.abnormal_record = abnormal_record
        self.investigation_report = investigation_report
        self.expiry_date_time = expiry_date_time
        self.actual_weight = actual_weight
        self.production_in_charge = production_in_charge
        self.production_reviewer = production_reviewer

    @staticmethod
    def get_all_production():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionDetails ORDER BY vaccineName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():

            row = ProductionModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13])
            records.append(row)
        return records

    @staticmethod
    def get_production_by_id(production_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM ProductionDetails WHERE productionID = ?"
        cursor.execute(sqlcmd1, production_id)
        record = None

        for dbrow in cursor.fetchall():
            print(dbrow[0], dbrow[1], dbrow[2], dbrow[3], str(dbrow[4])[0:16].replace(" ", "T"), dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13])
            record = ProductionModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13])
        return record

    @staticmethod
    def insert_production(production_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO ProductionDetails (productionID, companyName, " \
                  "vaccineName, productionBatchNo, productionDateTime, rawMaterials, auxiliaryMaterials," \
                  "productionEquipmentParameters, abnormalRecord, investigationReport, expiryDateTime, actualWeight, " \
                  "productionIncharge, productionReviewer) " \
                  "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        print((production_obj.production_id,   production_obj.company_name,
                       production_obj.vaccine_name,             production_obj.production_batch_no,
                       production_obj.production_date_time,     production_obj.raw_materials,
                       production_obj.auxiliary_materials,      production_obj.production_equipment_parameters,
                       production_obj.abnormal_record,          "production_obj.investigation_report",
                       production_obj.expiry_date_time,         production_obj.actual_weight,
                       production_obj.production_in_charge,     production_obj.production_reviewer))
        cursor.execute(sqlcmd1, (production_obj.production_id,   production_obj.company_name,
                       production_obj.vaccine_name,             production_obj.production_batch_no,
                       production_obj.production_date_time,     production_obj.raw_materials,
                       production_obj.auxiliary_materials,      production_obj.production_equipment_parameters,
                       production_obj.abnormal_record,          production_obj.investigation_report,
                       production_obj.expiry_date_time,         production_obj.actual_weight,
                       production_obj.production_in_charge,     production_obj.production_reviewer))

    @staticmethod
    def update_production(production_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE ProductionDetails SET companyName = ?, vaccineName = ?, productionBatchNo = ?," \
                  "productionDateTime = ?, rawMaterials = ?, auxiliaryMaterials = ?," \
                  "productionEquipmentParameters = ?, abnormalRecord = ?," \
                  " expiryDateTime = ?, actualWeight = ?, productionIncharge= ?, productionReviewer=?" \
                  " WHERE productionID = ?"
        cursor.execute(sqlcmd1,  (production_obj.company_name,
                       production_obj.vaccine_name, production_obj.production_batch_no,
                       production_obj.production_date_time, production_obj.raw_materials,
                       production_obj.auxiliary_materials, production_obj.production_equipment_parameters,
                       production_obj.abnormal_record,
                       production_obj.expiry_date_time, production_obj.actual_weight,
                       production_obj.production_in_charge, production_obj.production_reviewer,
                       production_obj.production_id))

    @staticmethod
    def delete_production(production_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM ProductionDetails WHERE productionID = ?"
        cursor.execute(sqlcmd1, (production_obj.production_id))


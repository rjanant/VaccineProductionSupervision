from Constants import connString
import pyodbc
import time
class PackingModel:
    def __init__(self, packing_id, production_batch_no="", packing_batch_no="",
                 packing_date_time=None,
                 packing_form="", packing_materials="", packing_equipment="", abnormal_record="",
                 inspection_report="", investigation_report="", actual_weight=0, packing_in_charge="",
                 packing_reviewer=""):
        self.packing_id = packing_id
        self.production_batch_no = production_batch_no
        self.packing_batch_no = packing_batch_no
        self.packing_date_time = packing_date_time
        self.packing_form = packing_form
        self.packing_materials = packing_materials
        self.packing_equipment = packing_equipment
        self.abnormal_record = abnormal_record
        self.inspection_report = inspection_report
        self.investigation_report = investigation_report
        self.actual_weight = actual_weight
        self.packing_in_charge = packing_in_charge
        self.packing_reviewer = packing_reviewer

    @staticmethod
    def get_all_packing():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM PackingDetails ORDER BY packingBatchNo"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():

            row = PackingModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12])
            records.append(row)
        return records

    @staticmethod
    def get_packing_by_id(packing_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM PackingDetails WHERE packingID = ?"
        cursor.execute(sqlcmd1, packing_id)
        record = None

        for dbrow in cursor.fetchall():
            print(dbrow[0], dbrow[1], dbrow[2], dbrow[3], str(dbrow[4])[0:16].replace(" ", "T"), dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12])
            record = PackingModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12])
        return record

    @staticmethod
    def insert_packing(packing_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO PackingDetails (packingID, productionBatchNo, " \
                  "packingBatchNo, packingDateTime, packingForm, packingMaterials," \
                  "packingEquipment, abnormalRecord, inspectionReport, investigationReport, actualWeight, " \
                  "packingIncharge, packingReviewer) " \
                  "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
        print((packing_obj.packing_id,   packing_obj.production_batch_no,
                       packing_obj.packing_batch_no,       packing_obj.packing_date_time,
                        packing_obj.packing_form,          packing_obj.packing_materials,
                        packing_obj.packing_equipment,     packing_obj.abnormal_record,
                        "packing_obj.inspection_report",   "packing_obj.investigationReport",
                        packing_obj.actual_weight,          packing_obj.packing_in_charge,
                        packing_obj.packing_reviewer))
        cursor.execute(sqlcmd1, (packing_obj.packing_id,   packing_obj.production_batch_no,
                       packing_obj.packing_batch_no,       packing_obj.packing_date_time,
                        packing_obj.packing_form,          packing_obj.packing_materials,
                        packing_obj.packing_equipment,     packing_obj.abnormal_record,
                        "packing_obj.inspection_report",   "packing_obj.investigationReport",
                        packing_obj.actual_weight,          packing_obj.packing_in_charge,
                        packing_obj.packing_reviewer))

    @staticmethod
    def update_packing(packing_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE PackingDetails SET productionBatchNo = ?, packingBatchNo = ?, " \
                  "packingDateTime = ?, packingForm = ?, packingMaterials = ?," \
                  "packingEquipment = ?, abnormalRecord = ?,  " \
                  "  actualWeight = ?, packingIncharge= ?, packingReviewer=?" \
                  " WHERE packingID = ?"
        cursor.execute(sqlcmd1,  (packing_obj.production_batch_no,
                       packing_obj.packing_batch_no,
                       packing_obj.packing_date_time, packing_obj.packing_form,
                       packing_obj.packing_materials, packing_obj.packing_equipment,
                       packing_obj.abnormal_record,
                        packing_obj.actual_weight,
                       packing_obj.packing_in_charge, packing_obj.packing_reviewer,
                       packing_obj.packing_id))

    @staticmethod
    def delete_packing(packing_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM PackingDetails WHERE packingID = ?"
        cursor.execute(sqlcmd1, (packing_obj.packing_id))


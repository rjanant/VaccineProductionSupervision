from Constants import connString
import pyodbc
import time
class InoculationModel:
    def __init__(self, inoculation_id, production_batch_no="", vaccine_recipient_name="",
                 inoculation_date_time=None,
                 vaccine_recipient_aadhar_no="", vaccine_recipient_address="", vaccine_recipient_city="",
                 vaccine_recipient_state="",
                 vaccine_recipient_pincode="",  vaccine_recipient_country="",
                 vaccine_recipient_dob=None, inoculation_dose="",
                 inoculation_department="", inoculation_doctor_name="", inoculation_doctor_id="",
                 isBlockChainGenerated=False, prevHash="", hash=""):
        self.inoculation_id = inoculation_id
        self.production_batch_no = production_batch_no
        self.vaccine_recipient_name = vaccine_recipient_name
        self.inoculation_date_time = inoculation_date_time
        self.vaccine_recipient_aadhar_no = vaccine_recipient_aadhar_no
        self.vaccine_recipient_address = vaccine_recipient_address
        self.vaccine_recipient_city = vaccine_recipient_city
        self.vaccine_recipient_state = vaccine_recipient_state
        self.vaccine_recipient_pincode = vaccine_recipient_pincode
        self.vaccine_recipient_country = vaccine_recipient_country
        self.vaccine_recipient_dob = vaccine_recipient_dob
        self.inoculation_dose = inoculation_dose
        self.inoculation_department = inoculation_department
        self.inoculation_doctor_name = inoculation_doctor_name
        self.inoculation_doctor_id = inoculation_doctor_id
        self.isBlockChainGenerated = isBlockChainGenerated
        self.prevHash = prevHash
        self.hash = hash

    @staticmethod
    def get_all_inoculation():
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InoculationDetails ORDER BY vaccineRecipientName"
        cursor.execute(sqlcmd1)
        records = []

        for dbrow in cursor.fetchall():

            row = InoculationModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13], dbrow[14],
                                   dbrow[15], dbrow[16], dbrow[17])
            records.append(row)
        return records

    @staticmethod
    def get_inoculation_by_id(inoculation_id):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "SELECT * FROM InoculationDetails WHERE inoculationID = ?"
        cursor.execute(sqlcmd1, inoculation_id)
        record = None

        for dbrow in cursor.fetchall():
            print(dbrow[0], dbrow[1], dbrow[2], dbrow[3], str(dbrow[4])[0:16].replace(" ", "T"), dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13], dbrow[14])
            record = InoculationModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13], dbrow[14])
        return record

    @staticmethod
    def insert_inoculation(inoculation_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "INSERT INTO InoculationDetails (inoculationID, productionBatchNo, " \
                  "vaccineRecipientName, inoculationDateTime, vaccineRecipientAadharNo, vaccineRecipientAddress," \
                  "vaccineRecipientCity, vaccineRecipientState, vaccineRecipientPincode,  " \
                  "vaccineRecipientCountry, vaccineRecipientDob, " \
                  "inoculationDose, inoculationDepartment, " \
                  "inoculationDoctorName, inoculationDoctorID) " \
                  "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)"
        print((inoculation_obj.inoculation_id,                          inoculation_obj.production_batch_no,
                       inoculation_obj.vaccine_recipient_name,          inoculation_obj.inoculation_date_time,
                        inoculation_obj.vaccine_recipient_aadhar_no,    inoculation_obj.vaccine_recipient_address,
                        inoculation_obj.vaccine_recipient_city,         inoculation_obj.vaccine_recipient_state,
                        inoculation_obj.vaccine_recipient_pincode,      inoculation_obj.vaccine_recipient_country,
                        inoculation_obj.vaccine_recipient_dob,          inoculation_obj.inoculation_dose,
                        inoculation_obj.inoculation_department))
        cursor.execute(sqlcmd1, (inoculation_obj.inoculation_id,   inoculation_obj.production_batch_no,
                       inoculation_obj.vaccine_recipient_name,       inoculation_obj.inoculation_date_time,
                        inoculation_obj.vaccine_recipient_aadhar_no,          inoculation_obj.vaccine_recipient_address,
                        inoculation_obj.vaccine_recipient_city,     inoculation_obj.vaccine_recipient_state,
                        inoculation_obj.vaccine_recipient_pincode,   inoculation_obj.vaccine_recipient_country,
                        inoculation_obj.vaccine_recipient_dob,          inoculation_obj.inoculation_dose,
                        inoculation_obj.inoculation_department,             inoculation_obj.inoculation_doctor_name,
                        inoculation_obj.inoculation_doctor_id))

    @staticmethod
    def update_inoculation(inoculation_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "UPDATE InoculationDetails SET productionBatchNo = ?, vaccineRecipientName = ?, " \
                  "inoculationDateTime = ?, vaccineRecipientAadharNo = ?, vaccineRecipientAddress = ?," \
                  "vaccineRecipientCity = ?, vaccineRecipientState = ?," \
                  "vaccineRecipientPincode = ?, vaccineRecipientCountry= ?, vaccineRecipientDob=?, " \
                  "inoculationDose=?, inoculationDepartment = ?," \
                  "inoculationDoctorName = ? , inoculationDoctorID = ? " \
                  " WHERE inoculationID = ?"
        cursor.execute(sqlcmd1,  (inoculation_obj.production_batch_no,
                                inoculation_obj.vaccine_recipient_name,
                            inoculation_obj.inoculation_date_time, inoculation_obj.vaccine_recipient_aadhar_no,
                       inoculation_obj.vaccine_recipient_address, inoculation_obj.vaccine_recipient_city,
                       inoculation_obj.vaccine_recipient_state,
                       inoculation_obj.vaccine_recipient_pincode, inoculation_obj.vaccine_recipient_country,
                       inoculation_obj.vaccine_recipient_dob,   inoculation_obj.inoculation_dose,
                        inoculation_obj.inoculation_department,
                       inoculation_obj.inoculation_doctor_name, inoculation_obj.inoculation_doctor_id,
                       inoculation_obj.inoculation_id))

    @staticmethod
    def delete_inoculation(inoculation_obj):
        conn = pyodbc.connect(connString, autocommit=True)
        cursor = conn.cursor()
        sqlcmd1 = "DELETE FROM InoculationDetails WHERE inoculationID = ?"
        cursor.execute(sqlcmd1, (inoculation_obj.inoculation_id))


from flask import Flask, request, render_template, redirect, url_for
import os
import pypyodbc
import uuid
from RoleModel import RoleModel
from UserModel import UserModel
from Constants import connString

from ProductionModel import ProductionModel
from PackingModel import PackingModel
from InspectionModel import InspectionModel
from InoculationModel import InoculationModel

from ProductionInChargeModel import ProductionInChargeModel
from ProductionReviewerModel import ProductionReviewerModel

from PackingInChargeModel import PackingInChargeModel
from PackingReviewerModel import PackingReviewerModel

from InspectionInChargeModel import InspectionInChargeModel
from InspectionReviewerModel import InspectionReviewerModel
import time
from datetime import datetime
app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
user_name = ""
role_object = None
message = ""
msg_type = ""


def initialize():
    global message, msg_type
    message = ""
    msg_type = ""


def process_role(option_id):
    if option_id == 10:
        if role_object.can_role == False:
            return False
    if option_id == 20:
        if role_object.can_user == False:
            return False
    if option_id == 30:
        if role_object.can_production == False:
            return False
    if option_id == 40:
        if role_object.can_packing == False:
            return False
    if option_id == 50:
        if role_object.can_inspection == False:
            return False
    if option_id == 60:
        if role_object.can_inoculation == False:
            return False
    if option_id == 70:
        if role_object.can_production_in_charge == False:
            return False
    if option_id == 80:
        if role_object.can_production_reviewer == False:
            return False
    if option_id == 90:
        if role_object.can_packing_in_charge == False:
            return False
    if option_id == 100:
        if role_object.can_packing_reviewer == False:
            return False
    if option_id == 110:
        if role_object.can_inspection_in_charge == False:
            return False
    if option_id == 120:
        if role_object.can_inspection_reviewer == False:
            return False
    return True


@app.route('/')
def index():
    global user_id, user_name
    return render_template('Login.html')  # when the home page is called Index.hrml will be triggered.


@app.route('/processLogin', methods=['POST'])
def processLogin():
    global user_id, user_name, role_object
    print(1)
    user_name = request.form['user_name']
    password = request.form['password']
    conn1 = pypyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM UserTable WHERE userName = '" + user_name + "' AND password = '" + password + "' " \
                "AND isActive = 1";
    print(2)
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()

    cur1.commit()
    if not row:
        return render_template('Login.html', processResult="Invalid Credentials")
    user_id = row[0]
    user_name = row[3]

    cur2 = conn1.cursor()
    sqlcmd2 = "SELECT * FROM Role WHERE RoleID = '" + str(row[6]) + "'"
    cur2.execute(sqlcmd2)
    row2 = cur2.fetchone()

    if not row2:
        return render_template('Login.html', processResult="Invalid Role")

    role_object = RoleModel(row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6], row2[7], row2[8], row2[9], row2[10], row2[11], row2[12], row2[13])

    return render_template('Dashboard.html')


@app.route("/ChangePassword")
def changePassword():
    global user_id, user_name
    return render_template('ChangePassword.html')


@app.route("/ProcessChangePassword", methods=['POST'])
def processChangePassword():
    global user_id, user_name
    oldPassword = request.form['oldPassword']
    newPassword = request.form['newPassword']
    confirmPassword = request.form['confirmPassword']
    conn1 = pypyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd1 = "SELECT * FROM UserTable WHERE user_name = '" + user_name + "' AND password = '" + oldPassword + "'";
    cur1.execute(sqlcmd1)
    row = cur1.fetchone()
    cur1.commit()
    if not row:
        return render_template('ChangePassword.html', msg="Invalid Old Password")

    if newPassword.strip() != confirmPassword.strip():
        return render_template('ChangePassword.html', msg="New Password and Confirm Password are NOT same")

    conn2 = pypyodbc.connect(connString, autocommit=True)
    cur2 = conn2.cursor()
    sqlcmd2 = "UPDATE UserTable SET password = '" + newPassword + "' WHERE user_name = '" + user_name + "'";
    cur1.execute(sqlcmd2)
    cur2.commit()
    return render_template('ChangePassword.html', msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, user_name
    return render_template('Dashboard.html')


@app.route("/Information")
def Information():
    global message, msg_type
    return render_template('Information.html', msg_type=msg_type, message=message)


@app.route("/UserListing")
def UserListing():
    global user_id, user_name

    global message, msg_type, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    canRole = process_role(10)

    if canRole == False:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    conn2 = pypyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM UserTable ORDER BY user_name"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break

        conn3 = pypyodbc.connect(connString, autocommit=True)
        cursor3 = conn3.cursor()
        temp = str(dbrow[6])
        sqlcmd3 = "SELECT * FROM Role WHERE RoleID = '" + temp + "'"
        cursor3.execute(sqlcmd3)
        rolerow = cursor3.fetchone()
        roleModel = RoleModel(0)
        if rolerow:
            roleModel = RoleModel(rolerow[0], rolerow[1])
        else:
            print("Role Row is Not Available")

        row = UserModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], roleModel=roleModel)
        records.append(row)
    return render_template('UserListing.html', records=records)


@app.route("/UserOperation")
def UserOperation():
    global user_id, user_name

    global message, msg_type, role_object
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    canRole = process_role(10)

    if canRole == False:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.args.get('operation')
    unqid = ""

    rolesDDList = []

    conn4 = pypyodbc.connect(connString, autocommit=True)
    cursor4 = conn4.cursor()
    sqlcmd4 = "SELECT * FROM Role"
    cursor4.execute(sqlcmd4)
    print("sqlcmd4???????????????????????????????????????????????????????/", sqlcmd4)
    while True:
        roleDDrow = cursor4.fetchone()
        if not roleDDrow:
            break
        print("roleDDrow[1]>>>>>>>>>>>>>>>>>>>>>>>>>", roleDDrow[1])
        roleDDObj = RoleModel(roleDDrow[0], roleDDrow[1])
        rolesDDList.append(roleDDObj)

    row = UserModel(0)

    if operation != "Create":
        unqid = request.args.get('unqid').strip()
        conn2 = pypyodbc.connect(connString, autocommit=True)
        cursor = conn2.cursor()
        sqlcmd1 = "SELECT * FROM UserTable WHERE user_id = '" + unqid + "'"
        cursor.execute(sqlcmd1)
        dbrow = cursor.fetchone()
        if dbrow:

            conn3 = pypyodbc.connect(connString, autocommit=True)
            cursor3 = conn3.cursor()
            temp = str(dbrow[6])
            sqlcmd3 = "SELECT * FROM Role WHERE RoleID = '" + temp + "'"
            cursor3.execute(sqlcmd3)
            rolerow = cursor3.fetchone()
            roleModel = RoleModel(0)
            if rolerow:
                roleModel = RoleModel(rolerow[0], rolerow[1])
            else:
                print("Role Row is Not Available")
            row = UserModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], roleModel=roleModel)

    return render_template('UserOperation.html', row=row, operation=operation, rolesDDList=rolesDDList)


@app.route("/ProcessUserOperation", methods=['POST'])
def processUserOperation():
    global user_name, user_id
    operation = request.form['operation']
    unqid = request.form['unqid'].strip()
    user_name = request.form['user_name']
    emailid = request.form['emailid']
    password = request.form['password']
    contactNo = request.form['contactNo']
    isActive = 0
    if request.form.get("isActive") != None:
        isActive = 1
    roleID = request.form['roleID']

    conn1 = pypyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    sqlcmd = ""
    if operation == "Create":
        sqlcmd = "INSERT INTO UserTable( user_name,emailid, password,contactNo, isActive, roleID) VALUES('" + user_name + "','" + emailid + "', '" + password + "' , '" + contactNo + "', '" + str(
            isActive) + "', '" + str(roleID) + "')"
    if operation == "Edit":
        sqlcmd = "UPDATE UserTable SET user_name = '" + user_name + "', emailid = '" + emailid + "', password = '" + password + "',contactNo='" + contactNo + "',  isActive = '" + str(
            isActive) + "', roleID = '" + str(roleID) + "' WHERE user_id = '" + unqid + "'"
    if operation == "Delete":
        sqlcmd = "DELETE FROM UserTable WHERE user_id = '" + unqid + "'"

    if sqlcmd == "":
        return redirect(url_for('Information'))
    cur1.execute(sqlcmd)
    cur1.commit()
    conn1.close()
    return redirect(url_for("UserListing"))


'''
    Role Operation Start
'''


@app.route("/RoleListing")
def RoleListing():
    global message, msg_type
    print("role_object>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", role_object)
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    canRole = process_role(20)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    searchData = request.args.get('searchData')
    print(searchData)
    if searchData == None:
        searchData = "";
    conn2 = pypyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM Role WHERE roleName LIKE '" + searchData + "%'"
    print(sqlcmd1)
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break

        row = RoleModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6])

        records.append(row)

    return render_template('RoleListing.html', records=records, searchData=searchData)


@app.route("/RoleOperation")
def RoleOperation():
    global message, msg_type
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    canRole = process_role(120)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.args.get('operation')
    unqid = ""
    row = RoleModel(0, "", 0, 0, 0, 0)
    if operation != "Create":
        unqid = request.args.get('unqid').strip()

        conn2 = pypyodbc.connect(connString, autocommit=True)
        cursor = conn2.cursor()
        sqlcmd1 = "SELECT * FROM Role WHERE RoleID = '" + unqid + "'"
        cursor.execute(sqlcmd1)
        while True:
            dbrow = cursor.fetchone()
            if not dbrow:
                break
            row = RoleModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6])

    return render_template('RoleOperation.html', row=row, operation=operation)


@app.route("/process_roleOperation", methods=['POST'])
def process_roleOperation():
    global message, msg_type
    if role_object == None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    canRole = process_role(120)

    if canRole == False:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    print("process_role")

    operation = request.form['operation']
    if operation != "Delete":
        roleName = request.form['roleName']
        canRole = 0
        canUser = 0
        CL111 = 0
        CL222 = 0
        CL333 = 0

        if request.form.get("canRole") != None:
            canRole = 1
        if request.form.get("canUser") != None:
            canUser = 1
        if request.form.get("CL111") != None:
            CL111 = 1
        if request.form.get("CL222") != None:
            CL222 = 1
        if request.form.get("CL333") != None:
            CL333 = 1

    print(1)
    unqid = request.form['unqid'].strip()
    print(operation)
    conn3 = pypyodbc.connect(connString, autocommit=True)
    cur3 = conn3.cursor()

    sqlcmd = ""
    if operation == "Create":
        sqlcmd = "INSERT INTO Role (roleName, canRole, canUser, CL111, CL222, CL333) VALUES ('" + roleName + "', '" + str(
            canRole) + "', '" + str(canUser) + "', '" + str(CL111) + "', '" + str(CL222) + "', '" + str(CL333) + "')"
    if operation == "Edit":
        print("edit inside")
        sqlcmd = "UPDATE Role SET roleName = '" + roleName + "', canRole = '" + str(canRole) + "', canUser = '" + str(
            canUser) + "', CL111 = '" + str(CL111) + "', CL222 = '" + str(CL222) + "', CL333 = '" + str(
            CL333) + "' WHERE RoleID = '" + unqid + "'"
    if operation == "Delete":
        conn4 = pypyodbc.connect(connString, autocommit=True)
        cur4 = conn4.cursor()
        sqlcmd4 = "SELECT roleID FROM UserTable WHERE roleID = '" + unqid + "'"
        cur4.execute(sqlcmd4)
        dbrow4 = cur4.fetchone()
        if dbrow4:
            message = "You can't Delete this Role Since it Available in Users Table"
            msg_type = "Error"
            return redirect(url_for('Information'))

        sqlcmd = "DELETE FROM Role WHERE RoleID = '" + unqid + "'"
    print(operation, sqlcmd)
    if sqlcmd == "":
        return redirect(url_for('Information'))
    cur3.execute(sqlcmd)
    cur3.commit()

    return redirect(url_for('RoleListing'))


'''
    Role Operation End
'''


@app.route("/ProductionInChargeListing")
def production_in_charge_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(30)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = ProductionInChargeModel.get_all_production_in_charges()
    return render_template('ProductionInChargeListing.html', records=records)


@app.route("/ProductionInChargeOperation")
def production_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(30)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = ProductionModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = ProductionInChargeModel.get_production_in_charge_by_id(unique_id)

    return render_template('ProductionInChargeOperation.html', row=row, operation=operation)


@app.route("/ProcessProductionInChargeOperation", methods=['POST'])
def process_production_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_production_in_charge_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_production_in_charge = process_role(30)
    print("process_production_in_charge_operation11111")
    if not can_production_in_charge:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.form['operation']


    production_in_charge_obj = ProductionInChargeModel("", "")
    if request.form.get("is_active") is not None:
        production_in_charge_obj.is_active = 1

    if operation != "Delete":
        production_in_charge_obj.production_in_charge_name = request.form['production_in_charge_name']

    if operation == "Create":
        production_in_charge_obj.production_in_charge_id = uuid.uuid1()
        production_in_charge_obj.insert_production_in_charge(production_in_charge_obj)

    if operation == "Edit":
        production_in_charge_obj.production_in_charge_id = request.form['unique_id']
        production_in_charge_obj.update_production_in_charge(production_in_charge_obj)

    if operation == "Delete":
        production_in_charge_obj.production_in_charge_id = request.form['unique_id']
        production_in_charge_obj.delete_production_in_charge(production_in_charge_obj)

    return redirect(url_for('production_in_charge_listing'))


@app.route("/ProductionReviewerListing")
def production_reviewer_listing():
    global user_id, user_name, message, msg_type, role_object
    print("role_object", role_object)
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(80)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = ProductionReviewerModel.get_all_production_reviewers()
    return render_template('ProductionReviewerListing.html', records=records)


@app.route("/ProductionReviewerOperation")
def production_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(80)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = ProductionModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = ProductionReviewerModel.get_production_reviewer_by_id(unique_id)

    return render_template('ProductionReviewerOperation.html', row=row, operation=operation)


@app.route("/ProcessProductionReviewerOperation", methods=['POST'])
def process_production_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_production_reviewer_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_production_reviewer = process_role(30)
    print("process_production_reviewer_operation11111")
    if not can_production_reviewer:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.form['operation']


    production_reviewer_obj = ProductionReviewerModel("", "")
    if request.form.get("is_active") is not None:
        production_reviewer_obj.is_active = 1

    if operation != "Delete":
        production_reviewer_obj.production_reviewer_name = request.form['production_reviewer_name']

    if operation == "Create":
        production_reviewer_obj.production_reviewer_id = uuid.uuid1()
        production_reviewer_obj.insert_production_reviewer(production_reviewer_obj)

    if operation == "Edit":
        production_reviewer_obj.production_reviewer_id = request.form['unique_id']
        production_reviewer_obj.update_production_reviewer(production_reviewer_obj)

    if operation == "Delete":
        production_reviewer_obj.production_reviewer_id = request.form['unique_id']
        production_reviewer_obj.delete_production_reviewer(production_reviewer_obj)

    return redirect(url_for('production_reviewer_listing'))


@app.route("/PackingInChargeListing")
def packing_in_charge_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_packing = process_role(90)

    if not can_packing:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = PackingInChargeModel.get_all_packing_in_charges()
    return render_template('PackingInChargeListing.html', records=records)


@app.route("/PackingInChargeOperation")
def packing_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_packing = process_role(90)

    if not can_packing:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = PackingInChargeModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = PackingInChargeModel.get_packing_in_charge_by_id(unique_id)

    return render_template('PackingInChargeOperation.html', row=row, operation=operation)


@app.route("/ProcessPackingInChargeOperation", methods=['POST'])
def process_packing_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_packing_in_charge_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_packing_in_charge = process_role(90)
    print("process_packing_in_charge_operation11111")
    if not can_packing_in_charge:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.form['operation']


    packing_in_charge_obj = PackingInChargeModel("", "")
    if request.form.get("is_active") is not None:
        packing_in_charge_obj.is_active = 1

    if operation != "Delete":
        packing_in_charge_obj.packing_in_charge_name = request.form['packing_in_charge_name']

    if operation == "Create":
        packing_in_charge_obj.packing_in_charge_id = uuid.uuid1()
        packing_in_charge_obj.insert_packing_in_charge(packing_in_charge_obj)

    if operation == "Edit":
        packing_in_charge_obj.packing_in_charge_id = request.form['unique_id']
        packing_in_charge_obj.update_packing_in_charge(packing_in_charge_obj)

    if operation == "Delete":
        packing_in_charge_obj.packing_in_charge_id = request.form['unique_id']
        packing_in_charge_obj.delete_packing_in_charge(packing_in_charge_obj)

    return redirect(url_for('packing_in_charge_listing'))


@app.route("/PackingReviewerListing")
def packing_reviewer_listing():
    global user_id, user_name, message, msg_type, role_object
    print("role_object", role_object)
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_packing = process_role(100)

    if not can_packing:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = PackingReviewerModel.get_all_packing_reviewers()
    return render_template('PackingReviewerListing.html', records=records)


@app.route("/PackingReviewerOperation")
def packing_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_packing = process_role(100)

    if not can_packing:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = PackingReviewerModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = PackingReviewerModel.get_packing_reviewer_by_id(unique_id)

    return render_template('PackingReviewerOperation.html', row=row, operation=operation)


@app.route("/ProcessPackingReviewerOperation", methods=['POST'])
def process_packing_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_packing_reviewer_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))

    can_packing_reviewer = process_role(100)
    if not can_packing_reviewer:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.form['operation']


    packing_reviewer_obj = PackingReviewerModel("", "")
    if request.form.get("is_active") is not None:
        packing_reviewer_obj.is_active = 1
    if operation != "Delete":
        packing_reviewer_obj.packing_reviewer_name = request.form['packing_reviewer_name']
    if operation == "Create":
        packing_reviewer_obj.packing_reviewer_id = uuid.uuid1()
        packing_reviewer_obj.insert_packing_reviewer(packing_reviewer_obj)

    if operation == "Edit":
        packing_reviewer_obj.packing_reviewer_id = request.form['unique_id']
        packing_reviewer_obj.update_packing_reviewer(packing_reviewer_obj)

    if operation == "Delete":
        packing_reviewer_obj.packing_reviewer_id = request.form['unique_id']
        packing_reviewer_obj.delete_packing_reviewer(packing_reviewer_obj)

    return redirect(url_for('packing_reviewer_listing'))



@app.route("/InspectionInChargeListing")
def inspection_in_charge_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(110)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = InspectionInChargeModel.get_all_inspection_in_charges()
    return render_template('InspectionInChargeListing.html', records=records)


@app.route("/InspectionInChargeOperation")
def inspection_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(110)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = InspectionInChargeModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = InspectionInChargeModel.get_inspection_in_charge_by_id(unique_id)

    return render_template('InspectionInChargeOperation.html', row=row, operation=operation)


@app.route("/ProcessInspectionInChargeOperation", methods=['POST'])
def process_inspection_in_charge_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_inspection_in_charge_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_inspection_in_charge = process_role(110)
    print("process_inspection_in_charge_operation11111")
    if not can_inspection_in_charge:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.form['operation']


    inspection_in_charge_obj = InspectionInChargeModel("", "")
    if request.form.get("is_active") is not None:
        inspection_in_charge_obj.is_active = 1

    if operation != "Delete":
        inspection_in_charge_obj.inspection_in_charge_name = request.form['inspection_in_charge_name']

    if operation == "Create":
        inspection_in_charge_obj.inspection_in_charge_id = uuid.uuid1()
        inspection_in_charge_obj.insert_inspection_in_charge(inspection_in_charge_obj)

    if operation == "Edit":
        inspection_in_charge_obj.inspection_in_charge_id = request.form['unique_id']
        inspection_in_charge_obj.update_inspection_in_charge(inspection_in_charge_obj)

    if operation == "Delete":
        inspection_in_charge_obj.inspection_in_charge_id = request.form['unique_id']
        inspection_in_charge_obj.delete_inspection_in_charge(inspection_in_charge_obj)

    return redirect(url_for('inspection_in_charge_listing'))


@app.route("/InspectionReviewerListing")
def inspection_reviewer_listing():
    global user_id, user_name, message, msg_type, role_object
    print("role_object", role_object)
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(120)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = InspectionReviewerModel.get_all_inspection_reviewers()
    return render_template('InspectionReviewerListing.html', records=records)


@app.route("/InspectionReviewerOperation")
def inspection_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(120)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))
    operation = request.args.get('operation')
    row = InspectionReviewerModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = InspectionReviewerModel.get_inspection_reviewer_by_id(unique_id)

    return render_template('InspectionReviewerOperation.html', row=row, operation=operation)


@app.route("/ProcessInspectionReviewerOperation", methods=['POST'])
def process_inspection_reviewer_operation():
    global user_id, user_name, message, msg_type, role_object
    print("process_inspection_reviewer_operation")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_inspection_reviewer = process_role(120)
    print("process_inspection_reviewer_operation11111")
    if not can_inspection_reviewer:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))

    operation = request.form['operation']


    inspection_reviewer_obj = InspectionReviewerModel("", "")
    if request.form.get("is_active") is not None:
        inspection_reviewer_obj.is_active = 1

    if operation != "Delete":
        inspection_reviewer_obj.inspection_reviewer_name = request.form['inspection_reviewer_name']

    if operation == "Create":
        inspection_reviewer_obj.inspection_reviewer_id = uuid.uuid1()
        inspection_reviewer_obj.insert_inspection_reviewer(inspection_reviewer_obj)

    if operation == "Edit":
        inspection_reviewer_obj.inspection_reviewer_id = request.form['unique_id']
        inspection_reviewer_obj.update_inspection_reviewer(inspection_reviewer_obj)

    if operation == "Delete":
        inspection_reviewer_obj.inspection_reviewer_id = request.form['unique_id']
        inspection_reviewer_obj.delete_inspection_reviewer(inspection_reviewer_obj)

    return redirect(url_for('inspection_reviewer_listing'))


@app.route("/ProductionListing")
def production_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(30)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = ProductionModel.get_all_production()
    return render_template('ProductionListing.html', records=records)


@app.route("/ProductionOperation")
def production_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(30)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    production_in_charges = ProductionInChargeModel.get_all_production_in_charges_id_names()
    production_reviewers = ProductionReviewerModel.get_all_production_reviewers_id_names()
    operation = request.args.get('operation')
    row = ProductionModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = ProductionModel.get_production_by_id(unique_id)
    print("In Charge Records production_in_charges", len(production_in_charges))
    return render_template('ProductionOperation.html', row=row, operation=operation, production_in_charges=production_in_charges, production_reviewers=production_reviewers)


@app.route("/ProcessProductionOperation", methods=['POST'])
def process_production_operation():
    global user_id, user_name, message, msg_type, role_object
    print("ProcessProductionOperation1")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_production = process_role(30)

    if not can_production:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))
    production_obj = ProductionModel("", "")
    print("ProcessProductionOperation2")
    if len(request.files) != 0:
        file = request.files['investigation_report']
        if file.filename != '':
            production_obj.investigation_report = file.filename
            f = os.path.join('static/UPLOADED_FILES', production_obj.investigation_report)
            file.save(f)

    operation = request.form['operation']
    print("ProcessProductionOperation3")
    if operation != "Delete":
        production_obj.company_name = request.form['company_name']
        production_obj.vaccine_name = request.form['vaccine_name']
        production_obj.production_batch_no = request.form['production_batch_no']
        prd_date_time = request.form['production_date_time'].replace("T", " ")
        production_obj.production_date_time = datetime.strptime(prd_date_time, '%Y-%m-%d %H:%M')
        production_obj.raw_materials = request.form['raw_materials']
        production_obj.auxiliary_materials = request.form['auxiliary_materials']
        production_obj.production_equipment_parameters = request.form['production_equipment_parameters']
        production_obj.abnormal_record = request.form['abnormal_record']
        expiry_date_time = request.form['expiry_date_time'].replace("T", " ")
        production_obj.expiry_date_time = datetime.strptime(expiry_date_time, '%Y-%m-%d %H:%M')
        production_obj.actual_weight = request.form['actual_weight']
        production_obj.production_in_charge = request.form['production_in_charge']
        production_obj.production_reviewer = request.form['production_reviewer']
    print("ProcessProductionOperation4")
    if operation == "Create":
        production_obj.production_id = str(uuid.uuid1())
        production_obj.insert_production(production_obj)

    if operation == "Edit":
        production_obj.production_id = request.form['unique_id']
        production_obj.update_production(production_obj)

    if operation == "Delete":
        production_obj.production_id = request.form['unique_id']
        production_obj.delete_production(production_obj)

    return redirect(url_for('production_listing'))


@app.route("/PackingListing")
def packing_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_production = process_role(40)

    if not can_production:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = PackingModel.get_all_packing()
    return render_template('PackingListing.html', records=records)


@app.route("/PackingOperation")
def packing_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_packing = process_role(40)

    if not can_packing:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    packing_in_charges = PackingInChargeModel.get_all_packing_in_charges_id_names()
    packing_reviewers = PackingReviewerModel.get_all_packing_reviewers_id_names()
    operation = request.args.get('operation')
    row = PackingModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = PackingModel.get_packing_by_id(unique_id)
    print("In Charge Records packing_in_charges", len(packing_in_charges))
    return render_template('PackingOperation.html', row=row, operation=operation, packing_in_charges=packing_in_charges, packing_reviewers=packing_reviewers)


@app.route("/ProcessPackingOperation", methods=['POST'])
def process_packing_operation():
    global user_id, user_name, message, msg_type, role_object
    print("ProcessPackingOperation1")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_packing = process_role(40)

    if not can_packing:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))
    packing_obj = PackingModel("", "")
    print("ProcessPackingOperation2")
    if len(request.files) != 0:
        file = request.files['investigation_report']
        if file.filename != '':
            packing_obj.investigation_report = file.filename
            f = os.path.join('static/UPLOADED_FILES', packing_obj.investigation_report)
            file.save(f)

    operation = request.form['operation']
    print("ProcessPackingOperation3")
    if operation != "Delete":
        packing_obj.production_batch_no = request.form['production_batch_no']
        packing_obj.packing_batch_no = request.form['packing_batch_no']
        prd_date_time = request.form['packing_date_time'].replace("T", " ")
        packing_obj.packing_date_time = datetime.strptime(prd_date_time, '%Y-%m-%d %H:%M')
        packing_obj.packing_form = request.form['packing_form']
        packing_obj.packing_materials = request.form['packing_materials']
        packing_obj.packing_equipment = request.form['packing_equipment']
        packing_obj.abnormal_record = request.form['abnormal_record']
        packing_obj.actual_weight = request.form['actual_weight']
        packing_obj.packing_in_charge = request.form['packing_in_charge']
        packing_obj.packing_reviewer = request.form['packing_reviewer']
    print("ProcessPackingOperation4")
    if operation == "Create":
        packing_obj.packing_id = str(uuid.uuid1())
        packing_obj.insert_packing(packing_obj)

    if operation == "Edit":
        packing_obj.packing_id = request.form['unique_id']
        packing_obj.update_packing(packing_obj)

    if operation == "Delete":
        packing_obj.packing_id = request.form['unique_id']
        packing_obj.delete_packing(packing_obj)

    return redirect(url_for('packing_listing'))


@app.route("/InspectionListing")
def inspection_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(50)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = InspectionModel.get_all_inspection()
    return render_template('InspectionListing.html', records=records)


@app.route("/InspectionOperation")
def inspection_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inspection = process_role(50)

    if not can_inspection:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    inspection_in_charges = InspectionInChargeModel.get_all_inspection_in_charges_id_names()
    inspection_reviewers = InspectionReviewerModel.get_all_inspection_reviewers_id_names()
    operation = request.args.get('operation')
    row = InspectionModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = InspectionModel.get_inspection_by_id(unique_id)
    print("In Charge Records inspection_in_charges", len(inspection_in_charges))
    return render_template('InspectionOperation.html', row=row, operation=operation, inspection_in_charges=inspection_in_charges, inspection_reviewers=inspection_reviewers)


@app.route("/ProcessInspectionOperation", methods=['POST'])
def process_inspection_operation():
    global user_id, user_name, message, msg_type, role_object
    print("ProcessInspectionOperation1")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_inspection = process_role(50)

    if not can_inspection:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))
    inspection_obj = InspectionModel("", "")
    print("ProcessInspectionOperation2")
    if len(request.files) != 0:
        file = request.files['inspection_results']
        if file.filename != '':
            inspection_obj.inspection_results = file.filename
            f = os.path.join('static/UPLOADED_FILES', inspection_obj.inspection_results)
            file.save(f)

    operation = request.form['operation']
    print("ProcessInspectionOperation3")
    if operation != "Delete":
        print(1)
        inspection_obj.production_batch_no = request.form['production_batch_no']
        inspection_obj.dosage_form = request.form['dosage_form']
        print(2)
        prd_date_time = request.form['inspection_date_time'].replace("T", " ")
        inspection_obj.inspection_date_time = datetime.strptime(prd_date_time, '%Y-%m-%d %H:%M')
        inspection_obj.specification = request.form['specification']
        print(3)
        inspection_obj.inspection_standards = request.form['inspection_standards']
        inspection_obj.inspection_equipments = request.form['inspection_equipments']
        print(4)
        inspection_obj.inspection_observations = request.form['inspection_observations']
        inspection_obj.inspection_calculations = request.form['inspection_calculations']
        print(5)
        inspection_obj.inspection_in_charge = request.form['inspection_in_charge']
        inspection_obj.inspection_reviewer = request.form['inspection_reviewer']
    print("ProcessInspectionOperation4")
    if operation == "Create":
        inspection_obj.inspection_id = str(uuid.uuid1())
        inspection_obj.insert_inspection(inspection_obj)

    if operation == "Edit":
        inspection_obj.inspection_id = request.form['unique_id']
        inspection_obj.update_inspection(inspection_obj)

    if operation == "Delete":
        inspection_obj.inspection_id = request.form['unique_id']
        inspection_obj.delete_inspection(inspection_obj)

    return redirect(url_for('inspection_listing'))

@app.route("/InoculationListing")
def inoculation_listing():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inoculation = process_role(30)

    if not can_inoculation:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))

    records = InoculationModel.get_all_inoculation()
    return render_template('InoculationListing.html', records=records)


@app.route("/InoculationOperation")
def inoculation_operation():
    global user_id, user_name, message, msg_type, role_object
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('Information'))
    can_inoculation = process_role(30)

    if not can_inoculation:
        message = "You Don't Have Permission to Access User"
        msg_type = "Error"
        return redirect(url_for('Information'))


    operation = request.args.get('operation')
    row = InoculationModel("", "")
    if operation != "Create":
        unique_id = request.args.get('unique_id').strip()

        row = InoculationModel.get_inoculation_by_id(unique_id)

    return render_template('InoculationOperation.html', row=row, operation=operation)


@app.route("/ProcessInoculationOperation", methods=['POST'])
def process_inoculation_operation():
    global user_id, user_name, message, msg_type, role_object
    print("ProcessInoculationOperation1")
    if role_object is None:
        message = "Application Error Occurred. Logout"
        msg_type = "Error"
        return redirect(url_for('/'))
    can_inoculation = process_role(30)

    if not can_inoculation:
        message = "You Don't Have Permission to Access Role"
        msg_type = "Error"
        return redirect(url_for('Information'))
    inoculation_obj = InoculationModel("", "")
    print("ProcessInoculationOperation2")
    if len(request.files) != 0:
        file = request.files['investigation_report']
        if file.filename != '':
            inoculation_obj.investigation_report = file.filename
            f = os.path.join('static/UPLOADED_FILES', inoculation_obj.investigation_report)
            file.save(f)

    operation = request.form['operation']
    print("ProcessInoculationOperation3")
    if operation != "Delete":
        print(1)
        inoculation_obj.production_batch_no = request.form['production_batch_no']
        inoculation_obj.vaccine_recipient_name = request.form['vaccine_recipient_name']
        print(2)
        prd_date_time = request.form['inoculation_date_time'].replace("T", " ")
        inoculation_obj.inoculation_date_time = datetime.strptime(prd_date_time, '%Y-%m-%d %H:%M')
        dob_date_time = request.form['vaccine_recipient_dob'].replace("T", " ")
        inoculation_obj.vaccine_recipient_dob = datetime.strptime(dob_date_time, '%Y-%m-%d')
        print(2)
        inoculation_obj.vaccine_recipient_aadhar_no = request.form['vaccine_recipient_aadhar_no']
        inoculation_obj.vaccine_recipient_address = request.form['vaccine_recipient_address']
        print(3)
        inoculation_obj.vaccine_recipient_city = request.form['vaccine_recipient_city']
        inoculation_obj.vaccine_recipient_state = request.form['vaccine_recipient_state']
        print(4)
        inoculation_obj.vaccine_recipient_pincode = request.form['vaccine_recipient_pincode']
        inoculation_obj.vaccine_recipient_country = request.form['vaccine_recipient_country']
        print(5)
        inoculation_obj.inoculation_dose = request.form['inoculation_dose']
        inoculation_obj.inoculation_department = request.form['inoculation_department']
        print(6)
        inoculation_obj.inoculation_doctor_name = request.form['inoculation_doctor_name']
        inoculation_obj.inoculation_doctor_id = request.form['inoculation_doctor_id']
    print("ProcessInoculationOperation4")
    if operation == "Create":
        inoculation_obj.inoculation_id = str(uuid.uuid1())
        inoculation_obj.insert_inoculation(inoculation_obj)

    if operation == "Edit":
        inoculation_obj.inoculation_id = request.form['unique_id']
        inoculation_obj.update_inoculation(inoculation_obj)

    if operation == "Delete":
        inoculation_obj.inoculation_id = request.form['unique_id']
        inoculation_obj.delete_inoculation(inoculation_obj)

    return redirect(url_for('inoculation_listing'))


import os
import hashlib
import json


@app.route("/BlockChainGeneration")
def BlockChainGeneration():

    conn = pypyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM InoculationDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    sqlcmd = "SELECT COUNT(*) FROM InoculationDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null"
    cursor.execute(sqlcmd)
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksNotCreated = dbrow[0]
    return render_template('BlockChainGeneration.html', blocksCreated=blocksCreated, blocksNotCreated=blocksNotCreated)


@app.route("/ProcessBlockchainGeneration", methods=['POST'])
def ProcessBlockchainGeneration():

    conn = pypyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT COUNT(*) FROM InoculationDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd)
    blocksCreated = 0
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        blocksCreated = dbrow[0]

    prevHash = ""
    print("blocksCreated", blocksCreated)
    if blocksCreated != 0:
        connx = pypyodbc.connect(connString, autocommit=True)
        cursorx = connx.cursor()
        sqlcmdx = "SELECT * FROM InoculationDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY uniqueID"
        cursorx.execute(sqlcmdx)
        dbrowx = cursorx.fetchone()
        print(2)
        if dbrowx:
            uniqueID = dbrowx[0]
            conny = pypyodbc.connect(connString, autocommit=True)
            cursory = conny.cursor()
            sqlcmdy = "SELECT hash FROM InoculationDetails WHERE uniqueID < '" + str(
                uniqueID) + "' ORDER BY uniqueID DESC"
            cursory.execute(sqlcmdy)
            dbrowy = cursory.fetchone()
            if dbrowy:
                print(3)
                prevHash = dbrowy[0]
            cursory.close()
            conny.close()
        cursorx.close()
        connx.close()
    conn = pypyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()
    sqlcmd = "SELECT * FROM InoculationDetails WHERE isBlockChainGenerated = 0 or isBlockChainGenerated is null ORDER BY uniqueID"
    cursor.execute(sqlcmd)

    while True:
        sqlcmd1 = ""
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        unqid = str(dbrow[18])
        '''
        bdata = str(dbrow[1])+str(dbrow[2])+str(dbrow[3])+str(dbrow[4])+str(dbrow[5])+str(dbrow[6])+str(dbrow[7])+str(dbrow[8])+str(dbrow[9])\
                +str(dbrow[10])+str(dbrow[11])+str(dbrow[12])+str(dbrow[13])+str(dbrow[14])+str(dbrow[15])+str(dbrow[18])+str(dbrow[19])+str(dbrow[20])
        '''
        bdata = str(dbrow[1]) + str(dbrow[2]) + str(dbrow[3]) + str(dbrow[4])
        block_serialized = json.dumps(bdata, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()

        conn1 = pypyodbc.connect(connString, autocommit=True)
        cursor1 = conn1.cursor()
        sqlcmd1 = "UPDATE InoculationDetails SET isBlockChainGenerated = 1, hash = '" + block_hash + "', prevHash = '" + prevHash + "' WHERE uniqueID = '" + unqid + "'"
        cursor1.execute(sqlcmd1)
        cursor1.close()
        conn1.close()
        prevHash = block_hash
    return render_template('BlockchainGenerationResult.html')


@app.route("/BlockChainReport")
def BlockChainReport():

    conn = pypyodbc.connect(connString, autocommit=True)
    cursor = conn.cursor()

    sqlcmd1 = "SELECT * FROM InoculationDetails WHERE isBlockChainGenerated = 1"
    cursor.execute(sqlcmd1)
    conn2 = pypyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM InoculationDetails ORDER BY uniqueID DESC"
    cursor.execute(sqlcmd1)
    records = []

    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break



        row = InoculationModel(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4], dbrow[5], dbrow[6], dbrow[7],
                                  dbrow[8], dbrow[9], dbrow[10], dbrow[11], dbrow[12], dbrow[13], dbrow[14],
                                   dbrow[15], dbrow[16], dbrow[17])
        records.append(row)

    return render_template('BlockChainReport.html', records=records)


if __name__ == "__main__":
    app.run()

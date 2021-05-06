
dbrow[0], dbrow[1], dbrow[2], dbrow[3]


class AAADataModel:
    # instance attribute
    def __init__(self, FL111, FL222="", FL333="", FL444 = "", isActive=False):
        self.FL111=FL111
        self.FL222=FL222
        self.FL333=FL333
        self.FL444=FL444
        self.CL111=CL111

from AAADataModel import AAADataModel

@app.route("/AAAListing")
def AAAListing():
    conn2 = pypyodbc.connect(connString, autocommit=True)
    cursor = conn2.cursor()
    sqlcmd1 = "SELECT * FROM AAA"
    cursor.execute(sqlcmd1)
    records = []
    
    while True:
        dbrow = cursor.fetchone()
        if not dbrow:
            break
        row = AAAModel(listAAA)
        records.append(row)
    return render_template('AAAListing.html', records=records)


@app.route("/AAAOperation")
def AAAOperation():
    operation = request.args.get('operation')
    unqid = ""
    
    row = AAAModel(0)

    if operation != "Create" :
        unqid = request.args.get('unqid').strip()
        conn2 = pypyodbc.connect(connString, autocommit=True)
        cursor = conn2.cursor()
        sqlcmd1 = "SELECT * FROM AAA WHERE FL111 = '"+unqid+"'"
        cursor.execute(sqlcmd1)
        while True:
            dbrow = cursor.fetchone()
            if not dbrow:
                break
            row = AAADataModel(listAAA)
        
    return render_template('AAAOperation.html', row = row, operation=operation )




@app.route("/ProcessAAAOperation",methods = ['POST'])
def processAAAOperation():
    global FL222, userID
    operation = request.form['operation']
    unqid = request.form['unqid'].strip()
    FL222 = request.form['FL222']
    FL333 = request.form['FL333']
    FL444 = request.form['FL444']
    
    CL111 = 0
    if request.form.get("CL111") != None :
        CL111 = 1
    conn1 = pypyodbc.connect(connString, autocommit=True)
    cur1 = conn1.cursor()
    
    
    if operation == "Create" :
        sqlcmd = "INSERT INTO AAA( FL222,FL333,CL111) VALUES('"+FL222+"','"+FL333+"' ,'"+str(CL111)+"')"
    if operation == "Edit" :
        sqlcmd = "UPDATE AAA SET FL222 = '"+FL222+"', FL333 = '"+FL333+"',FL444 = '"+FL444+"', CL111 = '"+str(CL111)+"' WHERE FL111 = '"+unqid+"'"  
    if operation == "Delete" :

        sqlcmd = "DELETE FROM AAA WHERE FL111 = '"+unqid+"'" 

    cur1.execute(sqlcmd)
    cur1.commit()
    conn1.close()
    return redirect(url_for("AAAListing"))


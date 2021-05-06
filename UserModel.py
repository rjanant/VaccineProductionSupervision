class UserModel:
    # instance attribute
    def __init__(self, userID, userName="", emailid="", password="", contactNo="", isActive=False, roleID=0, roleModel=None):
        self.userID=userID
        self.userName=userName
        self.emailid = emailid
        self.password=password
        self.contactNo = contactNo
        self.isActive=isActive
        self.roleID = roleID
        self.roleModel = roleModel
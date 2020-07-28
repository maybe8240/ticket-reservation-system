
class AdminInfo():
    def __init__(self, raw_admin):
        self.admins = []
        self.raw_admin = raw_admin
        self.__parse()

    def __parse(self):
        for admin in self.raw_admin:
            temp_admin = {}
            temp_admin['nickname'] = admin.nickname
            temp_admin['role'] = admin.role
            self.admins.append(temp_admin)


class CompanyInfo():
    def __init__(self, raw_company):
        self.companys = []
        self.raw_company = raw_company
        self.__parse()

    def __parse(self):
        for company in self.raw_company:
            temp_company = {}
            temp_company['company_name'] = company.company_name
            temp_company['En_name'] = company.En_name
            self.companys.append(temp_company)

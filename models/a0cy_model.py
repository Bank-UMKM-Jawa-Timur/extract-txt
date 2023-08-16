class A0CYModel:
    def __init__(self, field, froms, to, length, desc):
        self.field = field
        self.froms = froms
        self.to = to
        self.length = length
        self.desc = desc

    def init_list():
        list1 = A0CYModel("CYSTAT", 1, 1, 1, "Status Record")
        list2 = A0CYModel("CYCODE", 2, 4, 3, "Currency Code")
        list3 = A0CYModel("CYNAME", 1, 1, 1, "Currency Name")
        list4 = A0CYModel("CYDTLC", 1, 1, 1, "Tanggal Diubah")
        list5 = A0CYModel("CYDECI", 1, 1, 1, "Decimal Point")
        all_list = []
        all_list.append(list1)
        all_list.append(list2)
        all_list.append(list3)
        all_list.append(list4)
        all_list.append(list5)
        return all_list

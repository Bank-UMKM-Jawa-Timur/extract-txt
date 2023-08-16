class LLOANModel:
    def __init__(self, field, froms, to, length, desc):
        self.field = field
        self.froms = froms
        self.to = to
        self.length = length
        self.desc = desc

    def init_list():
        list1 = LLOANModel("L0STAT", 1, 1, 1, "Status Record")
        list2 = LLOANModel("L0STAD", 2, 2, 1, "Status Data")
        list3 = LLOANModel("L0BRCA", 3, 4, 2, "Wilayah")
        list4 = LLOANModel("L0BRCD", 5, 7, 3, "Branch")
        list5 = LLOANModel("L0CSNO", 8, 15, 8, "Customer code")
        all_list = []
        all_list.append(list1)
        all_list.append(list2)
        all_list.append(list3)
        all_list.append(list4)
        all_list.append(list5)
        return all_list
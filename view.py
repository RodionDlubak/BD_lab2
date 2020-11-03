from tabulate import tabulate


class View:
    def print(self, data):
        columns, rows = data
        arr = [];
        for r in rows:
            arr.append([r[0], r[1], r[2], r[3]])
        print(tabulate(arr, headers=columns, tablefmt='orgtbl'))

    def print_2(self, data):
        columns, rows = data
        arr = [];
        for r in rows:
            arr.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]])
        print(tabulate(arr, headers=columns, tablefmt='orgtbl'))

    def print_3(self, data):
        columns, rows = data
        arr = [];
        for r in rows:
            arr.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11]])
        print(tabulate(arr, headers=columns, tablefmt='orgtbl'))

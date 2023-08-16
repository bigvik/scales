import sqlite3
import config


class Datasaver:

    def __init__(self, data) -> None:
        if data: self.data = data
        self.db = config.DB

    def set_data(self,data):
        self.data = data

    def save_data(self):
        destinations = {'xls':self.to_xls, 'sql':self.to_sql}
        destinations[self.db]()

    def to_xls(self):
        from openpyxl import load_workbook
        xl = load_workbook('weight_list.xlsx')
        xl_sheet = xl.active
        xl_sheet.append(self.data)
        xl.save('weight_list.xlsx')

    def to_sql(self):
        con = sqlite3.connect('measurements.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS weight(
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    brutto INT,
                    netto INT,
                    tara INT,
                    dest TEXT);
                    """)
        con.commit()
        cur.execute("INSERT INTO weight(date, brutto, netto, tara, dest) VALUES(?, ?, ?, ?, ?);", self.data)
        con.commit()


if __name__ == "__main__":
    pass
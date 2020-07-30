import pickle
from typing import Any, List

import questionary
from tabulate import tabulate


class Program:
    def __init__(self) -> None:
        print("-" * 100)
        print("Welcome to the program!")
        print("-" * 100)
        self.emptyError = "Data Set is Currently Empty,\nInsert some data first!"

    def run(self):
        self.createFiles()
        self.actionChoose()

    def actionChoose(self):
        choices: List[Any] = [
            "ADD A NEW MEDICINE".capitalize(),
            "MODIFY MEDICINE BASED ON MED_ID".capitalize(),
            "DELETE MEDICINE BASED ON MED_ID".capitalize(),
            "SHOW ALL MEDICINE DATA".capitalize(),
            "PURCHASE MEDICINE AND GENERATE BILL".capitalize(),
            "EXIT",
        ]
        while True:
            resp = questionary.select(
                "Choose an action: ", choices, default=choices[-1]
            ).ask()
            if resp == choices[0]:
                self.newMed()
            elif resp == choices[1]:
                self.modifyData()
            elif resp == choices[2]:
                self.delMed()
            elif resp == choices[3]:
                self.showAll()
            elif resp == choices[4]:
                self.purchase()
            elif resp == choices[5]:
                print("You have chosen to exit!")
                exit()
            else:
                print("An error occurred!")
                exit()

    def createFiles(self) -> None:
        with open("medicine.dat", "wb") as target:
            obj = []
            pickle.dump(obj, target)
            target.close()
        return

    def newMed(self):
        cont = True
        while cont:
            with open("medicine.dat", "rb") as fileObj:
                curData: List[List[Any]] = pickle.load(fileObj)
                fileObj.close()
                CUR_IDS = [row[0] for row in curData]
            while True:
                med_id = str(input("Enter the Medicine I.D. : "))
                if med_id.isalnum() == True and len(med_id) == 3:
                    if med_id in CUR_IDS:
                        print("This ID is already taken!")
                    else:
                        break
                else:
                    print("Try again!")
                    print("Hint: The I.D. should be alphanumeric and 3 digits")

            while True:
                med_name = str(input("Enter the Medicine Name: "))
                if 1 <= len(med_name) <= 30:
                    break
                else:
                    print(
                        "Medicine Name should not be empty and should be less than 30 characters!"
                    )

            while True:
                med_desc = str(input("Enter a short description (50 chars max): "))
                if 5 <= len(med_desc) <= 50:
                    break
                else:
                    print("Try again!")

            while True:
                medPrice = str(input("Enter the price of the medicine: "))
                medQty = str(input("Enter the quantity of the medicine: "))
                medReQty = str(input("Enter the reorder quantity of the medicine: "))
                if int(medPrice) > 0 and int(medQty) > 0 and int(medReQty) > 0:
                    medPrice = int(medPrice)
                    medQty = int(medQty)
                    medReQty = int(medReQty)
                    break
                else:
                    print("Try again!")

            toBeIns = [med_id, med_name, med_desc, medPrice, medQty, medReQty]
            curData.append(toBeIns)
            with open("medicine.dat", "wb") as file:
                pickle.dump(curData, file)
                file.close()

            cont = questionary.confirm(
                "Do you wish to continue?(y/n)", default=False
            ).ask()

    def modifyData(self):
        with open("medicine.dat", "rb") as file:
            data: List[List[Any]] = pickle.load(file)
            file.close()
        if len(data) == 0:
            print(self.emptyError)
            return
        ids = []
        for row in data:
            if row[0] not in ids:
                ids.append(row[0])
        modId = questionary.autocomplete(
            "Enter the I.D. for which you want to modify details: ",
            ids,
            validate=lambda val: val in ids,
        ).ask()
        modRow = []
        modIndex = 0
        for row in data:
            if row[0] == modId:
                modRow = row
                modIndex = data.index(row)
                data.remove(modRow)
                break
        while True:
            newName = str(input("Enter the new name(Enter for skip): "))
            if newName.rstrip(" ").lstrip(" ") == "":
                break
            else:
                modRow[1] = newName.rstrip(" ").lstrip(" ")
                break
        while True:
            newDesc = str(input("Enter the new description(Enter for skip): "))
            if newDesc.rstrip(" ").lstrip(" ") == "":
                break
            else:
                modRow[2] = newDesc.rstrip(" ").lstrip(" ")[:30]
                break

        # Price Loop
        while True:
            newPrice = str(input("Enter the new price(Entry for skip): "))
            if newPrice.rstrip(" ").lstrip(" ") == "":
                break
            else:
                modRow[3] = int(newPrice)
                break

        # Reorder qty loop
        while True:
            newQty = str(input("Enter the new quantity(Enter for skip): "))
            if newQty.rstrip(" ").lstrip(" ") == "":
                break
            else:
                modRow[4] = int(newQty)
                break

        # Reorder qty loop
        while True:
            newReQty = str(input("Enter the new Reorder Quantity(Enter for skip): "))
            if newReQty.rstrip(" ").lstrip(" ") == "":
                break
            else:
                modRow[5] = int(newReQty)
                break

        data.insert(modIndex, modRow)

        with open("medicine.dat", "wb") as fileObject:
            pickle.dump(data, fileObject)
            fileObject.close()
        return

    def delMed(self):
        cont = True
        while cont:
            with open("medicine.dat", "rb") as file:
                data: List[List[Any]] = pickle.load(file)
                file.close()
            if len(data) == 0:
                print(self.emptyError)
                return
            IDS = [row[0] for row in data]
            delId = questionary.autocomplete(
                "Choose the I.D. for which you want to delete record: ",
                choices=IDS,
                validate=lambda val: val in IDS,
            ).ask()
            for row in data:
                if row[0] == delId:
                    data.remove(row)
                    break
            with open("medicine.dat", "wb") as fh:
                pickle.dump(data, fh)
                fh.close()
            cont = questionary.confirm(
                "Do you wish to continue?(y/n):", default=False
            ).ask()

    def showAll(self):
        with open("medicine.dat", "rb") as file:
            data = pickle.load(file)
            file.close()
        if len(data) == 0:
            print(self.emptyError)
            return
        print(
            tabulate(
                data,
                headers=[
                    "MED_ID",
                    "MED_NAME",
                    "MED_DESC",
                    "PRICE",
                    "QUANTITY",
                    "REORDER_QTY",
                ],
                tablefmt="fancy_grid",
            )
        )
        return

    def purchase(self):
        with open("medicine.dat", "rb") as fileObject:
            data: List[List[Any]] = pickle.load(fileObject)
            fileObject.close()
        if len(data) == 0:
            print(self.emptyError)
            return
        IDS = [row[0] for row in data]
        billID = questionary.autocomplete(
            "Enter the ID of the Medicine that you want to buy: ",
            choices=IDS,
            validate=lambda val: val in IDS,
        ).ask()

        bill_row = []

        for row in data:
            if row[0] == billID:
                bill_row = row
                break

        while True:
            billQty = str(input("Enter the quantity that you want: "))
            if int(billQty) <= 0:
                print("QTY cannot be <= 0!\nTry Again!")
            else:
                billQty = int(billQty)
                break

        totalPrice = bill_row[3] * billQty

        billContent = [
            [billID, bill_row[1], bill_row[2], bill_row[3], billQty, totalPrice]
        ]
        print(
            tabulate(
                tabular_data=billContent,
                headers=["ID", "NAME", "DESC", "PRICE", "QTY", "TOTAL PRICE"],
                tablefmt="fancy_grid",
            )
        )
        return


if __name__ == "__main__":
    app = Program()
    app.run()

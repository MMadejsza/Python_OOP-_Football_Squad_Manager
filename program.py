
# ? Course        Software Development 1
# ? Assessment    Coursework #2
# ? Name          Maciej Madejsza
# ? Student ID    MAD21541198
# ? Date          2022.11.29
# ? Last update   2022.12.06 23:50

#!______________________Classes, functions, variables used in program flow___________________________
import math
from datetime import datetime
from tabulate import tabulate

# - Creating class as a template for grades. Now we have 5 but may be more in the future. Each grade has it's rate and salary assigned


class Grade:
    def __init__(self, threshold, salary):
        self.threshold = threshold,
        self.salary = salary,

# - Creating class as container with variables and serving them methods specifically dealing with Finance of the club


class Finances:
    def __init__(self):
        self.grade1 = Grade(80, "At least 1000")
        self.grade2 = Grade(60, "Between 700 and 1000")
        self.grade3 = Grade(45, "Between 500 and 700")
        self.grade4 = Grade(30, "Between 400 and 500")
        self.grade5 = Grade(0, "Below 400")

    # - Function calculating rating. Takes players features into arguments
    def calculate_rating(self, speedRate, shootingRate, passingRate, defendingRate, dribblingRate, physicalityRate):
        score = (speedRate + shootingRate + passingRate +
                 defendingRate + dribblingRate + physicalityRate) * 100 / 30
        # - round to have two digits
        return round(score, 2)

    # - Function calculating salary. Takes players rating as an argument and following logic below assigns salary
    def calculate_salary(self, score):
        if(score >= self.grade1.threshold[0]):
            return self.grade1.salary[0]
        elif(score >= self.grade2.threshold[0]):
            return self.grade2.salary[0]
        elif(score >= self.grade3.threshold[0]):
            return self.grade3.salary[0]
        elif(score >= self.grade4.threshold[0]):
            return self.grade4.salary[0]
        else:
            return self.grade5.salary[0]

# - Creating class as a template for players. We can have up to 100 of them, each one has the same variables and integrated methods to serve them


class Player:
    # - finances object with all its methods will be passed in here to be used in setting score + salary
    def __init__(self, finances, ID, name, dob, speedRate, shootingRate, passingRate, defendingRate, dribblingRate, physicalityRate):
        self.ID = ID
        self.name = name
        self.dob = dob
        self.age = ''  # - empty for later fill up
        self.speedRate = speedRate
        self.shootingRate = shootingRate
        self.passingRate = passingRate
        self.defendingRate = defendingRate
        self.dribblingRate = dribblingRate
        self.physicalityRate = physicalityRate
        self.score = finances.calculate_rating(self.speedRate,
                                               self.shootingRate,
                                               self.passingRate,
                                               self.defendingRate,
                                               self.dribblingRate,
                                               self.physicalityRate)
        self.salary = finances.calculate_salary(self.score)

    # - calculates players age based on date of birth
    def setAge(self):
        today = datetime.today()
        dob = self.dob
        self.age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
    # - Pulls out players data on request in table row format as the program is designed to store and fetch data from tables

    def getProfile(self):
        row = [self.ID, self.name, self.dob,
               self.age, self.score, self.salary]
        return row

# - Creating class as container with variables and serving them methods specifically dealing with input data storage - players bank of the club


class CatalogueOfPlayers:
    # - variables are hidden, not accessible by "." notation and that's why we have functions to pull them out. It prevents from unwanted operating on these data and changing them if the program will be further developed
    __catalogue = []
    # - Table layout headers
    __headers = [" UID", "Name", "D.o.B", " Age", "  Score", "Salary Range"]

    # - returns array of players on request
    def getCatalogue(self):
        return self.__catalogue

    # - returns amount of players on request
    def amountOfPLayers(self):
        return len(self.__catalogue)

    # - adds player to the bank
    def addPLayer(self, player):
        self.__catalogue.append(player)

    # - displays players in form of table, takes custom message and trigger if should be exported to a separate file. By default, function only display players in the terminal
    def showPlayers(self, message, export="null"):
        # - Custom rule to sort by, existing players (by ID as first[0] position in player object)
        def sortBy(player):
            return int(player[0])
        catalogueToShow = []
        for player in self.__catalogue:
            # - append profile as a row for table
            catalogueToShow.append((player.getProfile()))
        # - sorts them to display
        catalogueToShow.sort(key=sortBy)
        # - anchors headers in front of players - 1st position
        catalogueToShow.insert(0, self.__headers)
        # - calls and assign function creating table from given data. First row as headers for table. Rest of features to exactly reflect specification
        tabulatedCatalogue = tabulate(catalogueToShow, headers="firstrow", tablefmt="simple", colalign=(
            "right", "left", "left", "right", "right", "left"))
        print(message, tabulatedCatalogue,)
        # - if optional argument given, export to file with fixed name from specification
        if (export == "export"):
            print("\nResults generated in the file 'players.txt' as well.\n")
            playersTxt = open("./players.txt", "a")  # - in append mode
            playersTxt.write("\n")  # - function takes only 1 argument always
            playersTxt.write("Generated: ")
            playersTxt.write(str(datetime.today()))  # - log data
            playersTxt.write("\n")
            playersTxt.write(tabulatedCatalogue)
            playersTxt.close()  # - close file to save

    # - Function to fetch data if external file is given. Takes finances "library" and path of file to fetch from
    def fetchData(self, finances, path):
        # - opens, takes what program needs and closes the file
        takenFile = open(
            path)
        takenFileRows = takenFile.readlines()
        takenFile.close()
        # - cuts off table's header as the program gives it's own one
        takenFileRows.pop(0)
        for playerRow in takenFileRows:
            # - transform each row containing player's data as an array to work with
            playerRowAsArray = playerRow.split(", ")  # -
            ID = playerRowAsArray[0]
            name = playerRowAsArray[1]
            # - destroys ISO format STRING into simple numbers to create later on object from these numbers
            extractedDate = playerRowAsArray[2].split(
                "-")
            dob = datetime(int(extractedDate[0]), int(
                extractedDate[1]), int(extractedDate[2])).date()
            speedRate = int(playerRowAsArray[3])
            shootingRate = int(playerRowAsArray[4])
            passingRate = int(playerRowAsArray[5])
            defendingRate = int(playerRowAsArray[6])
            dribblingRate = int(playerRowAsArray[7])
            physicalityRate = int(playerRowAsArray[8])
            player = Player(finances, ID, name, dob, speedRate, shootingRate, passingRate,
                            defendingRate, dribblingRate, physicalityRate)
            player.setAge()
            # - adds complete player's profile to club's catalogue of players
            self.addPLayer(self, player)

# - Because specification requires 2 "main" functions / program flows, this function containing new player form is extracted to global scope. Uses clubs storage structure and finances like libraries with their methods


def inputForm(catalogueOfPlayers, finances):
    def stringInputValidation(inputName):
        while True:  # - loop forever
            # - following specification there's only 1 input "name" for name and among so many nationalities I gave up on case sensitivity and amount of words
            try:
                inputDatum = input(inputName).strip()
                for symbol in inputDatum:
                    # - no integers accepted across the name
                    if(symbol.isdigit()):
                        print("\nIntegers inside the name?")
                        raise ValueError
            except ValueError:  # - catches any unexpected error and prints following specification
                print("The rating you entered was invalid.\n")
                continue  # - return to initial condition while True what means repeats whole procedure
            if(inputDatum == ""):  # - catches empty input and do following:
                print('The rating you entered was invalid.',
                      "\nMust be one word please.\n")
                continue  # - like above
            else:  # - if input is like expected - return it to assign to variable

                return inputDatum

    def integerInputValidation(inputName, catalogueOfPlayers="null"):

        while True:  # - loop forever
            try:
                # - inputs give string type data - we have to wrap them in float() function to accept floats at all and then wrap into math.ceil() to get integer. thanks to math.ceil(), in case of input letter we fall into next exception as well
                # - extra variable to compare length later.
                inputID = input(inputName).strip()
                inputScore = math.ceil(float(inputID))
            except ValueError:  # - catches input letter
                print("The rating you entered was invalid",
                      "\nInteger please\n")
                continue  # - give extra chance as in previous validation

            if (inputName == "ID: "):  # - If it's used for ID
                # - fetch number of players
                numberOfPLayers = catalogueOfPlayers.amountOfPLayers(
                    catalogueOfPlayers)
                # - flag to check if ID is detected
                flag = 0
                if (len(inputID) != 2):  # - ID must have exactly 2 digits
                    print("The rating you entered was invalid",
                          "\nInteger please - exactly 2 digits.\n")
                    continue
                elif (inputScore < 0 or inputScore > 99):  # - catches ID exceeding range
                    print("The rating you entered was invalid",
                          "\nNumbers 0-99 please.\n")
                    continue  # - like above
                elif (numberOfPLayers):  # - if there are already players in club catalogue, take them
                    catalogue = catalogueOfPlayers.getCatalogue(
                        catalogueOfPlayers)
                    for player in catalogue:  # - and check ID of each one if exists
                        if (inputID == player.ID):
                            print("ID exists - ID must be unique")
                            flag = 1  # - if detected, set the flag
                if (flag):  # - if flag is 1
                    flag = 0  # - change it back at start again
                    continue
                else:  # - if flag isn't raised return input
                    return inputID
            elif (inputScore < 0 or inputScore > 5):  # - catches rating exceeding range
                print("The rating you entered was invalid",
                      "\nNumbers 0-5 please.\n")
                continue  # - like above
            else:  # - if input is like expected - return it to assign to variable
                return inputScore

    def getDob():
        while True:  # - loop forever
            try:
                year = int(input("Year: ").strip())
                month = int(input("Month: ").strip())
                day = int(input("Day: ").strip())
                # - gives iso format date
                dob = datetime(year, month, day).date()
            except ValueError:  # - catches input letter
                print("The D.o.B is invalid",
                      "\nDate spelling mistake.\n")
                continue  # - give extra chance as in previous validation
            return dob

    ID = integerInputValidation("ID: ", catalogueOfPlayers)
    name = stringInputValidation("Name: ")
    dob = getDob()

    # - Print message about next stage of fetching skills rates
    print('\nNow, please assign the rate from 0-5 to each skill. (Floats will be rounded UP in calculation!)\n')

    # - Collect skills rates by inputs in validation functions
    speedRate = integerInputValidation("Speed rate: ")
    shootingRate = integerInputValidation("Shooting rate: ")
    passingRate = integerInputValidation("Passing rate: ")
    defendingRate = integerInputValidation("Defending rate: ")
    dribblingRate = integerInputValidation("Dribbling rate: ")
    physicalityRate = integerInputValidation("Physicality rate: ")

    # - Now create/instantiate Python object based on following, previously created pattern as "player's profile" and based on input data.
    player = Player(finances, ID, name, dob, speedRate, shootingRate, passingRate,
                    defendingRate, dribblingRate, physicalityRate)
    player.setAge()
    catalogueOfPlayers.addPLayer(catalogueOfPlayers, player)

#!______________________Proper program flow 2 versions___________________________


def main():
    catalogueOfPlayers = CatalogueOfPlayers
    finances = Finances()
    print("\nCreate player's account to store stats and get suggested salary! \nLet's start with creating player's ID (2-digit number) in the system\n")
    while True:
        inputForm(catalogueOfPlayers, finances)
        numberOfPLayers = catalogueOfPlayers.amountOfPLayers(
            catalogueOfPlayers)
        print(numberOfPLayers)

        if (numberOfPLayers >= 3):
            answer = input(
                "\nDo you want to add more players? (Yes/Y/No/N)").upper()
            if (answer == "YES" or answer == "Y"):
                continue
            elif (answer == "NO" or answer == "N"):
                break
            else:
                continue
        if (numberOfPLayers == 99):
            print("End of program's capacity. We ran out of IDs")
            break
    catalogueOfPlayers.showPlayers(
        catalogueOfPlayers, "\nFinal Results: \n", "export")


def advanced(path):  # main
    catalogueOfPlayers = CatalogueOfPlayers
    finances = Finances()
    catalogueOfPlayers.fetchData(catalogueOfPlayers, finances, path)
    catalogueOfPlayers.showPlayers(catalogueOfPlayers, "\nFetched Results: \n")
    numberOfPLayers = catalogueOfPlayers.amountOfPLayers(
        catalogueOfPlayers)
    while True:
        if (numberOfPLayers >= 3):
            answer = input(
                "\nDo you want to add more players? (Yes/Y/No/N)").upper()
            if (answer == "YES" or answer == "Y"):
                inputForm(catalogueOfPlayers, finances)
            elif (answer == "NO" or answer == "N"):
                break
            else:
                continue
        if (numberOfPLayers == 99):
            print("End of program's capacity. We ran out of IDs")
            break

    # - Appreciate the hustle by printing thanks + print player's score + print player's salary
    print("\nThank you very much - players profiles are complete.\n")
    # - show players and export them
    catalogueOfPlayers.showPlayers(
        catalogueOfPlayers, "Final Results: \n", "export")


# main()
advanced("./PlayerData.txt")


# ? Resources:
# ? https://developer.mozilla.org/en-US/
# ? https://www.w3schools.com/
# ? https://stackoverflow.com/

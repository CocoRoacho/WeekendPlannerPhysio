# feiertagsliste erstellen, bearbeiten, ausgeben

import json
from datetime import date, timedelta

# file to work with
ft_file= "../data/Feiertagsliste.json"


class Feiertage():
    """ object Feiertage for storing a list of all workfree Feiertage 
        and 
            expand this list: add_new_year(self)
            clean list / delete years from json-file that are older than 1 year: ???


        self.datafile: file where the feiertagsliste is stored


        self.ft_datastream: main dict; loaded from json-file and maybe somehow changed by functions
        self.ft_alle: alle Feiertage in a list - not separated by years...
        self.ft_names: list of names of all used Feiertage
        self.last_year: the last year stored in datastream; ideally the actual year(?)

    """
    
    LIST_FTAGE = [
        ["Neujahr", 1, 1],
        ["Karfreitag", None, 0],
        ["Ostersonntag", None, 2],
        ["Ostermontag", None, 3],
        ["Tag der Arbeit", 1, 5],
        ["Himmelfahrt", None, 41],
        ["Pfingstsonntag", None, 51],
        ["Pfingstmontag", None, 52],
        ["Deutsche Einheit", 3, 10],
        ["Reformationstag", 31, 10],
        ["Heilig Abend", 24, 12],
        ["Weihnachtsfeiertag 1", 25, 12],
        ["Weihnachtsfeiertag 2", 26, 12],
        ["Silvester", 31, 12]
    ]
    
    ft_alle = None
    ft_names = None
    last_year = None
    ft_dic = None

    def __init__(self, datafile):
        self.datafile = datafile
        self.ft_datastream = load_json(self.datafile)
                
        self.fill_ft_set()

  
    def fill_ft_set(self):
        """ get values for init variables """
        
        self.ft_alle =  get_list_for_all_years(self.ft_datastream)
        self.ft_dic = {item[0] : item[1] for item in self.ft_alle}
        self.last_year = int(list(self.ft_datastream.keys())[-1])
        if not self.ft_names:
            self.ft_names = {ftx[0] for ftx in self.ft_alle}
            

    def add_new_year(self, year, month, day):
        """ adds a new year to json-file datastream """
        
        # prepare new dict for appending to datastream
        nextyear_ft = {year : {}}
        nextyear_newitem = nextyear_ft[year]
        date_karfreitag = date(year, month, day)
                
            
        for ftage_entry in self.LIST_FTAGE:
            if ftage_entry[1]: # dann ein Feiertag mit immer gleichem Datum
                nextyear_newitem[ftage_entry[0]] = f"{year}-{ftage_entry[2]}-{ftage_entry[1]}"
            
            elif ftage_entry[2] == 0: # statt monat eine "0" -> ich brauche die daten für den entsprechenden Karfreitag
                                
                # get to new dict...
                nextyear_newitem[ftage_entry[0]] = str(date_karfreitag)

            else:
                # bei anderen "ungleichen" Feiertagen das Datum errechnen...
                nextyear_newitem[ftage_entry[0]] = str(date_karfreitag + timedelta(ftage_entry[2]))

        
        # new created dict attach to datastream
        self.ft_datastream.update(nextyear_ft)

        self.clean_up_after()
                

    def clean_up_after(self):
        """ updating der attributes / variables
            save data to file
        """

        # update object attributes
        self.fill_ft_set()

        # save new list of feiertage as json-file
        save_json(self.datafile, self.ft_datastream)


    def delete_old_fts(self):
        """ delete feiertage which are older than let's say one year or so... """
        
        old_fts = [year for year in self.ft_datastream if int(year) < self.last_year - 1]

        for item in old_fts:
            del self.ft_datastream[item]

        # und nun noch speichern!!!
        self.clean_up_after()


    def add_new_ft(file_ft):
         """ add a new feiertag, maybe a temporary feiertag """
     
         pass
 
     
    def del_one_ft(file_ft):
         """ deletes one feiertag, maybe a temporary feiertag, specify a year from when... """
     
         pass     


    def __str__(self):
        """ the text you get when calling for the string """

        strng = ""
        for item in self.ft_datastream:
            strng += str(item) + "\n"
            for subitem in self.ft_datastream[item]:
                strng += f"  {subitem}: {self.ft_datastream[item][subitem]}\n"

        return strng
            

# D.R.Y: ist bereits in create_minions_class!!!! 
def load_json(file_name):
    """ loads datasequence from a json file """
    
    with open (file_name, "r") as datenfile:
                return json.load(datenfile)


def save_json(file_name, datastream):
    """ creates datasequence and saves as json """
        
    # serialize and save data
    with open(file_name, "w") as datenfile_mitarb:
        json.dump(datastream, datenfile_mitarb, indent=4)


def print_list_for_year(ft_liste, year):
    """ prints feiertage filtered by year to terminal """

    try:
        for ft_item in ft_liste[year].items():
            print(ft_item[0], " : ", ft_item[1])
    except KeyError:
        print(f"{year} is not in data!")


def get_list_for_year(ft_liste, year):
    """ returns feiertage filtered by year """

    return list(ft_liste[year].items())
    
    
def get_list_for_all_years(ft_liste):
    """ returns feiertage in one list """
    
    return [ft_item for ft_jahr in ft_liste for ft_item in ft_liste[ft_jahr].items()]
    
    

     


# ------------------------------------------------------

if __name__ == "__main__":

    """
    # filter for year
    jahr = "2022"
    print_list_for_year(liste, jahr)

    print("\n"*2)


    f_days = get_list_for_all_years(liste)
    #print(f_days)
    for item in f_days:
        print(item)
    """

    print("\n", "-"*5, " end of line ", "-"*5, "\n")
        

    ftxl = Feiertage(ft_file)
    """ creates an object from self created class Feiertage """

    print("1.:")
    print(ftxl)

    print("\n", "-"*5, " end of line ", "-"*5, "\n")

    #List line by line alle Feiertage
    for ftitem in ftxl.ft_alle:
        print(ftitem)

    print("")
    
    #list of all used Feiertage
    print("2.:")
    for ftnameitem in ftxl.ft_names:
        print(ftnameitem)
    
    print("")        
        
    #print("Add new Year!!!", ftxl.last_year + 1)    
    #ftxl.add_new_year(ftxl.last_year + 1, 4, 7)
    
    print("")        
    
    # -------------------------------
    # filter for year
    jahr = str(ftxl.last_year) #"2022"
    print(f"Filtered for {jahr}")
    print_list_for_year(ftxl.ft_datastream, jahr)

    print("\n"*2)

    # delete old stuff
    print("delete old stuff")
    ftxl.delete_old_fts()

    print("")
    print(ftxl)

    print("")
    print("last:")
    for xx in ftxl.ft_alle:
        print(xx)
        
    print("\nft_alle:")
    print(ftxl.ft_alle)
    print("\n"*3)
    
    for item in ftxl.ft_alle:
        print(item[0], " --> ", item[1])
        
    feierdic = {item[0]: item[1] for item in ftxl.ft_alle}
    print(feierdic)
    
    #---
    print("\n\n.ft_dic: ")
    print(ftxl.ft_dic)
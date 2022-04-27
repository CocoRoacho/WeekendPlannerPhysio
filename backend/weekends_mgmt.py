"""
iterate from starting date to enddate
compare with feiertagen, filtere diese und wochenenden raus

"""

from datetime import date, timedelta
from random import choice, randint
import backend.Mitarbeiter_mgmt as cmc
#import Mitarbeiter_mgmt as cmc


MINIONS= ["Petra", "Marco", "Ines", "Katrin", "Kerstin", "Michael"]

MONATE= ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

"""
feiertage= {
"2021-10-31" : "Reformationstag",
"2021-12-24" : "Heilig Abend",
"2021-12-25" : "Weihnachtsfeiertag 1",
"2021-12-26" : "Weihnachtsfeiertag 2",
"2021-12-31" : "Silvester",
"2022-01-01" : "Neujahr",
"2022-04-15" : "Karfreitag",
"2022-04-17" : "Ostersonntag",
"2022-04-18" : "Ostermontag",
"2022-05-01" : "Tag der Arbeit",
"2022-05-26" : "Himmelfahrt",
"2022-06-05" : "Pfingstsonntag",
"2022-06-06" : "Pfingstmontag",
"2022-10-03" : "Deutsche Einheit",
"2022-10-31" : "Reformationstag",
"2022-12-24" : "Heilig Abend",
"2022-12-25" : "Weihnachtsfeiertag 1",
"2022-12-26" : "Weihnachtsfeiertag 2",
"2022-12-31" : "Silvester",
"2023-01-01" : "Neujahr",
}
"""
#"""
fts_new = {
        "Neujahr": "2022-01-01",
        "Karfreitag": "2022-04-15",
        "Ostersonntag": "2022-04-17",
        "Ostermontag": "2022-04-18",
        "Tag der Arbeit": "2022-05-01",
        "Himmelfahrt": "2022-05-26",
        "Pfingstsonntag": "2022-06-05",
        "Pfingstmontag": "2022-06-06",
        "Deutsche Einheit": "2022-10-03",
        "Reformationstag": "2022-10-31",
        "Heilig Abend": "2022-12-24",
        "Weihnachtsfeiertag 1": "2022-12-25",
        "Weihnachtsfeiertag 2": "2022-12-26",
        "Silvester": "2022-12-31"
}
#"""
    
    


def make_plan(s_date, e_date, feiertage):
    """ pairs the date for the weekend plan 
 -  needs start and end date """
    
    # preparing the initial dates
    
    print("weekends type: ", type(s_date))
    # if in date type:
    if type(s_date) == date:
        date1 = s_date -timedelta(1)
    else:
        date1 = date(s_date[0], s_date[1], s_date[2])-timedelta(1)
    print("date1: ", date1, " -> ", type(date1))

    if type(e_date) == date:
        last_date = e_date
    else:        
        last_date = date(e_date[0], e_date[1], e_date[2])
    print("last_date: ", last_date, " -> ", type(last_date))
        
        

    datenliste= []


    # iterate til end_date and sort out usual weekdays
    while date1 < last_date:
        date1 += timedelta(1)
        this_date = f"{date1.year}-{str(date1.month).zfill(2)}-{str(date1.day).zfill(2)}" #must be this format: "2021-12-24"

  
        # weekday continue if not weekend in feiertag
        if date1.weekday() < 5 and not this_date in feiertage.values():
            continue
        
        if this_date in feiertage.values():
            datenliste.append(date1)        
            #print(date1, " : feiertag")
        
        else:
            datenliste.append(date1)
            #print(date1, " : weekend")


#    make pairs for every weekend include freedays as well...

# f.e. if thursday = feiertag: pair with next weekend --> maybe okay?
    dienste= []
    done_dates= []

    helplist= []

    for datum in datenliste:

        if datum in done_dates:
            continue
        
        done_dates.append(datum)
        helplist.append(datum)
    
        for d in range(datenliste.index(datum)+1, len(datenliste)):
            next_datum= datenliste[d]
                    
            if (next_datum - datum).days > 4:
                break
        
            if not next_datum in done_dates:
                done_dates.append(next_datum)
            if not next_datum in helplist:
                helplist.append(next_datum)
            
            
        dienste.append(helplist)
        helplist=[]

    # Dienste mit maximal 3 Tagen...            
    for dienst in dienste:
        
        if len(dienst)>3:
        
            dienste.append(dienst[2:])
            dienste[dienste.index(dienst)]= dienst[0:2]
                                           
    return sorted(dienste)


def get_month_name(z):
    """ takes a number and returns the month name """
    return MONATE[z-1]


def build_date_tag(w):
    """ returns the dict with the duties (paired days as 1 listitem) """
    
    anzahl_tage= len(w) #len = 1, 2 oder 3
    
    mon1 = get_month_name(w[0].month)
    
    # nur ein Tag Dienst
    if anzahl_tage == 1:
        return f"{w[0].day}. {mon1} {w[0].year}"
        
    else: #mehr als ein Tag Dienst
    
        # check same or different years
        years= [c.year for c in w]
        if min(years) != max(years):
                
            if anzahl_tage == 2:
                mon2= get_month_name(w[1].month)
                return f"{w[0].day}. {mon1}/{w[1].day}. {mon2} {w[1].year}"
            if anzahl_tage == 3:
                # mittlerer tag monat1 oder monat3
                if w[1].month == w[0].month:
                    mon2= get_month_name(w[2].month)
                    return f"{w[0].day}./{w[1].day}. {mon1}/{w[2].day}. {mon2} {w[2].year}"
            
                if w[1].month == w[2].month:
                    mon2= get_month_name(w[2].month)
                    return f"{w[0].day}. {mon1}/{w[1].day}./{w[2].day}. {mon2} {w[2].year}"
                
        else:            
            # same or different month?
            months= [c.month for c in w]
            if min(months) != max(months):
                
                # different months:
                if anzahl_tage == 2:
                    mon2= get_month_name(w[1].month)
                    return f"{w[0].day}. {mon1}/{w[1].day}. {mon2} {w[1].year}"
                if anzahl_tage == 3:
                    # mittlerer enty:  wie 1.monat
                    if w[1].month == w[0].month:
                        mon2= get_month_name(w[2].month)
                        return f"{w[0].day}./{w[1].day}. {mon1}/{w[2].day}. {mon2} {w[2].year}"
                     
                    # mittlerer enty:  wie 2.monat      
                    if w[1].month == w[2].month:
                        mon2= get_month_name(w[2].month)
                        return f"{w[0].day}. {mon1}/{w[1].day}./{w[2].day}. {mon2} {w[2].year}"
                        
            else: # same month
                if anzahl_tage == 2:
                    return f"{w[0].day}./{w[1].day}. {mon1} {w[1].year}"
                if anzahl_tage == 3:
                    return f"{w[0].day}./{w[1].day}./{w[2].day}. {mon1} {w[2].year}"
                        


# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

# make a class for dienste
class Dienste():
    """ """
    def __init__(self, name, daten, ft_dict):
        self.name = name
        self.daten = daten
        self.feiertag_name = None #feiertag_name
        self.opfer = None
        self.check_feiertag(ft_dict)
        
    def check_feiertag(self, feiertage):
        """ checks if datum == feiertag 
            gruppiert: 
              Ostern (aus Karfreitag, O-Sonn- & Montag)
              Weihnachten (aus Heilig Abend + Weih-feiertage)
              Pfingsten...
              Silvester...
        """
        
        # check for Feiertag or not:
        for datum in self.daten:
            datumsstring = str(datum)
            
            for ftag in feiertage:
                if datumsstring == feiertage[ftag]:
                    if 'karf' in ftag.lower() or 'oster' in ftag.lower():
                        self.feiertag_name = 'Ostern'
                
                    elif 'pfingst' in ftag.lower():
                        self.feiertag_name = 'Pfingsten'
                
                    elif 'heilig' in ftag.lower() or 'weihnacht' in ftag.lower():
                        self.feiertag_name = 'Weihnachten'
                
                    elif 'silvester' in ftag.lower() or 'neujahr' in ftag.lower():
                        self.feiertag_name = 'Silvester/Neujahr'
                
                    else:
                        self.feiertag_name = ftag
                    break
            

    def __str__(self):
        return self.name
        
            
    def __repr__(self):
        return f"{self.name}: \n\
Daten: {self.daten} \n\
Feiertag: {self.feiertag_name}"

 
# create and fill object dienste from class
def create_dienste_obj(start_date, end_date, feiert_dict):
    """ take args: 
        start_date, end_date as list: [yyyy, m, d] (items type int)
        feiert_dict as dict: {"Neujahr": "yyyy-mm-dd",...}
        
    and create an object from class Dienste """
    
    print("start: ", start_date)
    print("end: ", end_date)
    print("feiert_dict: ", feiert_dict)
    
    print("feiertype: ", type(feiert_dict))
    
    # prepare weekends list
    weekends= make_plan(start_date, end_date, feiert_dict)
    
    print("wknds: ", weekends)
    
    # create an Dienste Class object
    return [Dienste(build_date_tag(dienst), dienst, feiert_dict) for dienst in weekends]
    
    
    
                                                                                           
                                                                      
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_        

# start here!

if __name__ == "__main__":



    # Zeitraum
    start= [2022, 3, 25] #[2021, 12, 24]
    end= [2022, 6, 8] # was wenn dies ein Samstag ist, dann addiere noch ein paar Tage...
    
    start= date(2022, 3, 25)
    end= date(2022, 6, 8)
    
    dienste = create_dienste_obj(start, end, fts_new)

    ###weekends= make_plan(start_date, end_date)


    #
    # -- deprecated?? -----------
    #weekend_plan = {build_date_tag(day): day for day in weekends}
    #
    #for m in weekend_plan:
    #    spaces= " " * (32-len(m))
    #    print(f"{m}:{spaces}{list(weekend_plan[m])}")
    # /-- deprecated?? -----------    

    # create an Dienste Class object
    ###dienste = [Dienste(build_date_tag(dienst), dienst) for dienst in weekends]

    #"""
    print("\ndienst class:")

    for die in dienste:
        spaces= " " * (23-len(die.name))  
        print(f"{die}:{spaces}{die.daten}; {die.feiertag_name}")
    print("\n"*7)
    #"""                        
    
    # TODO:
        # wo soll gesplittet werden wenn 5Tage eingeteilt werden müssen? make a userinput???
    
    

    file_name = "mitarb_daten[test].json" #"mitarb_daten[v2].json"

    # create mitarbeiter objects
    mitarbeiter = cmc.create_minions(file_name)


    # -- deprecated?? -----------
    # save json
    #cmc.save_json(file_name, mitarbeiter)
    
    # ??? brauche ich minions_list?
    #minions_list =list for easy class instance building
    minions_list = [ma.minion_name for ma in mitarbeiter]
    
    #candidates = list for searching the right minion, minions in list are available yet
    #candidates = sorted(minions_list) 
    # sortiert nach last_turn_count; kleinste zuerst

    print("\n"*2)

    #cmc.show_all_minions(mitarbeiter)
    #print(f"minions_list: {minions_list}")
    
    # ? brauche ich das?    
    datum_list= [weekend_plan[wp] for wp in weekend_plan] # datum to look for a minion
                
    for x in weekend_plan: #range(len(datum_list)):
        print(f"\ngesuchtes Datum: {x}") #datum_list[x]}")



    # /-- deprecated?? -----------

    # Durchschnittliche Anzahl von Diensten pro Minion
    dienstdurchschnitt= round(len(dienste)/len(mitarbeiter), 2)


    for dienst_datum in dienste:

        #new_ma = cmc.get_minion(weekend_plan[x][0], mitarbeiter, dienstdurchschnitt, feiertag)
        new_ma = cmc.get_minion(dienst_datum.daten[0], mitarbeiter, dienstdurchschnitt, dienst_datum.feiertag_name)
        print(f"\n     Diesen Dienst wird {new_ma} übernehmen!")
        #cmc.count_up_dienst(mitarbeiter, new_ma)
        print(f"        {new_ma.minion_name}\tDienste: {new_ma.count} von: {len(datum_list)}")
        #weekend_plan[x] = new_ma
        dienst_datum.opfer = new_ma
   
    

    # erstellter Dienstplan ordenlich geprintet
    for die in dienste:
        weshift = f"{die.name} {die.feiertag_name}" if die.feiertag_name else die.name
        spaces= " " * (50-len(weshift))
        print(f"{weshift}:{spaces}{die.opfer}")
    
    #for m in weekend_plan:
    #    spaces= " " * (32-len(m))
    #    print(f"{m}:{spaces}{weekend_plan[m]}")

    print("\n")
    # Übersicht über die Anzahl der Dienste pro Mitarbeiter
    for ma in mitarbeiter:
        print(f"{ma}: {ma.count} / {len(dienste)}")
    
    
    # save a json_file:
    cmc.save_json(file_name, mitarbeiter)    

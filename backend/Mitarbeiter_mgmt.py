#pylint:disable=W0631

from datetime import date, timedelta
from random import choice, randint
import json


class Minion():
    '''
        Mitarbeiter für die Dienstliste
        
        Attributes
        ----------
        minion_id: lfd nummer damit einfach auf dieses objekt zugegriffen werden kann
        minion_name: Mitarbeiter name
        
        last_turn_count: wieviel Dienste im letzten Plan
        (minions mit weniger Diensten im letzten turnus beginnen im neuem plan)
        urlaub: Zeitraum wann Urlaub (evtl 6versions, oder list mit allen Terminen)
        last_years: welche Feiertage in den letzten 5 Jahren Dienst war
        
        Functions
        ---------
        display_minion: Mitarbeiter Status anzeigen
        
    '''
    
    # count: wie oft bereits vergebene Dienste
    count = 0 #counter
    ## nicht hier speichern...!???

    def __init__(self, minion_id, minion_name, last_dienst, last_years, urlaub, wunschfrei, wunschdienst, ftage_aktuell):

        self.minion_id = minion_id
        self.minion_name = minion_name
        self.last_dienst = last_dienst
        self.last_years = last_years    # letzte Feiertagsdienste als liste
        self.urlaub = urlaub
        self.wunschfrei = wunschfrei # hier können wunschfrei-termine abgelegt werden
        self.wunschdienst = wunschdienst # hier können wunschdienst-termine abgelegt werden
        self.feiertage = {
            'Ostern': 0, 
            'Tag der Arbeit': 0, 
            'Himmelfahrt': 0, 
            'Pfingsten': 0, 
            'Deutsche Einheit': 0, 
            'Reformationstag': 0, 
            'Weihnachten': 0, 
            'Silvester/Neujahr': 0
        }
        self.feiertage_dieses_jahr = ftage_aktuell #[0, 0, 0, 0, 0, 0, 0, 0] 
        
        self.fill_feiertage()
        # initialisieren der Feiertage von liste (zb: [ 0, 0, 1, 0, 1, 0, 0, 0]) für letzte 6 Jahre
        # je später der dienst war umso höher der Wert: Addierung von 0, 1, 2, 4, 8, 16, 32...
        
        
    def fill_feiertage(self):
        """ übernehme die letzten Feiertage der json file und ordne den jeweiligen variablen im dictionary zu """  
        for jahrindex, jahr in enumerate(self.last_years):
            for ftindex, ft in enumerate(jahr[:8]):              
                if jahrindex == 0 and ft == 1:
                    self.feiertage[list(self.feiertage.keys())[ftindex]] = 1
             
                else:                        
                    if ft: # == 1
                        self.feiertage[list(self.feiertage.keys())[ftindex]] += (2**jahrindex)
                        
                    
    def feiertag_dieses_jahr_abhaken(self, feiertag_name):
        """ notiert den Feiertagsdienst für dieses Jahr in der Liste """
        
        # getting the index for feiertag from self.feiertage
        fday_index = list(self.feiertage.keys()).index(feiertag_name)
        
        # sets the list on a specific item to 1
        self.feiertage_dieses_jahr[fday_index] = 1
               
    
    def display_last_years_duties(self):
        """ prints a list of last years feiertagsdienste """
    
        print("\n\tFeiertagsdienste der letzten Jahre:")
        for item in self.last_years:
            print(f"\t\t{item}")
    
    
    def display_urlaub(self):
        """ prints a list with holiday dates """
        
        if self.urlaub:
            print("\n\tUrlaubsplanung:")
            for item in self.urlaub:
                print(f"\t\tvon: {item[0]} bis {item[1]}")
    
    
    def display_minion(self):
        """ prints an oversight of the called object """
        
        print(f"\nMitarbeiter:\t{self.minion_name}\tid: {self.minion_id}\n \
 \tDienste in diesem Turnus:\t{self.count}\n \
 \tDienstindex vom letzten Turnus:\t{self.last_dienst}\n \
 \twunschdienst: {self.wunschdienst}\n \
 \twunschfrei: {self.wunschfrei}")
        self.display_last_years_duties()
        self.display_urlaub()
        
        
    def raise_count(self):
        """ raises the counter for actual duties by 1 """
        self.count += 1
        
        
    def get_json_set(self):
        """ returns a list to save as value in a json file """
                
        return{
            "last_dienst": self.last_dienst, #? ist das die richtige Zuordnung?
            "last_feiertage": self.last_years, 
            "aktuelle_feiertage": self.feiertage_dieses_jahr,
            "urlaub": self.urlaub,
            "wunschfrei": self.wunschfrei,
            "wunschdienst": self.wunschdienst
            }


    def check_urlaub(self, dienst_datum):
        """ uses datum and checks if this date is inside a holiday + 2 days before and after, if they are weekend.
        returns True if urlaub,
        returns False if NOT urlaub"""
       
        for zeitraum in self.urlaub:
            
            zeit1 = date(zeitraum[0][2], zeitraum[0][1], zeitraum[0][0])
            zeit2 = date(zeitraum[1][2], zeitraum[1][1], zeitraum[1][0])
            zeit3 = dienst_datum #date(dienst_datum[2], dienst_datum[1], dienst_datum[0])
         
            return bool(zeit1 - timedelta(2) <= zeit3 <= zeit2 + timedelta(2))

            # schaue hier am Besten nach, das nicht nur +/- 2 Tage gecheckt werden, sondern 
            # checke (evtl. voriges und) folgendes WE bzw. Abstand... ??? 


    # ??? could be normal function?
    def check_dates_match(self, wunschdatum, dienst_datum):
        """ uses dienst_datum and checks if this date is equal to wunschdatum
        returns True if dates match,
        returns False if NO match"""
       
        zeit1 = date(wunschdatum[2], wunschdatum[1], wunschdatum[0])
        zeit2 = dienst_datum
         
        return bool(zeit1 in (zeit2, zeit2 + timedelta(1), zeit2 + timedelta(2)))

    
    # ??? could be normal function?
    def frei_vor_wunschdienst(self, wd_date, dienst_date, diff_days):
        """ damit der Minion in den zwei Wochen vor seinem wunschdienst quasi kein Dienst hat... 
        wd_date = Datum Wunschdienst
        dienstdate = Datum des aktuellen Dienstes
        days = Anzahl der Tage die zwischen beiden Daten liegen sollen
        
        returns True bei match"""
        wunschdienst = date(wd_date[2], wd_date[1], wd_date[0])

        differenz= (wunschdienst - dienst_date).days
        
        return bool(0 < differenz < diff_days)
    
    # ??? normal function?
    def prioritize_binary_lists(self, binary_lst):
        """ returns a list with the values for prioritizing the Feiertage. needs a list with sublists with 0 and 1's """
        
        p_lst = []
        for column in range(len(binary_lst[0])):
            pbl= [item[column] for item in reversed(binary_lst)]

            p_lst.append(pbl.index(1)+1if 1 in pbl else 7)

        return p_lst
    
    
    def __str__(self):
        """ the text you get when calling for the string """
        return self.minion_name
        
    def __repr__(self):
        """ for debugging, sends you information """
        return f"{self.minion_name}: {self.last_dienst}, {self.count}; {self.urlaub}"
        
    def __eq__(self, other):
        """ uses equality functions on attribute minion_name """
        return self.minion_name == other


    def __lt__(self, other):
        """ uses less than functions on attribute last_turn_count """
        return self.last_dienst < other.last_dienst
        
        
    def __le__(self, other):
        """ uses less equal functions on attribute last_turn_count """
        return self.last_dienst <= other.last_dienst


#_-_-_-________-_-_-_


def show_all_minions(classlist):
    """ displays all objects with attributes... """
    for ma in classlist:
        ma.display_minion()

    print("\n")
 
    
def access_minion(classlist, name):
    """ returns the minion_id """
    return classlist[classlist.index(name)].minion_id
              
# ???
def count_up_dienst(classlist, name):
     """ minion_count += 1 """
     classlist[access_minion(classlist, name)].raise_count()      
             

def save_json(file_name, classlist):
    """ creates datasequence and saves as json """
    
    # the datasequence creation
    json_file2save= {m.minion_name : m.get_json_set() for m in classlist}
        
    # serialize and save data
    with open(file_name, "w") as datenfile_mitarb:
        json.dump(json_file2save, datenfile_mitarb, indent=4)

    
def load_json(file_name):
    """ loads datasequence from a json file """
    
    with open (file_name, "r") as datenfile_mitarb:
                return json.load(datenfile_mitarb)
                

def compare_w_average_count(ma_count, list_of_counts):
    """ returns a comparison from minion.count with average counts of minions 
    true when count > average    
    """
    
    return bool(ma_count > round((sum(list_of_counts) / len(list_of_counts))))
    
    
def average_duties(ma_count, turn_avg):
    """ returns True wenn ma_count > durchschnitt """
    return bool(ma_count > turn_avg)


def set_last_dienst_to_new_values(classlist):
    """ alle self.last_dienst values (ausser 6) um 1 erhöhen """

    for c in classlist:
        if c.last_dienst != 6:
            c.last_dienst += 1


# ??? ist das überhaupt so notwendig? check mal die funktion!!!      
def prioritize_by_value(dictio, x):
    """ recursive function: looks if x is in dict
        if not: call again with x-1 
        returns item with highest value """
    
    if x < 0:
        print("your Datasequence seems incorrect!")

    for k, v in dictio.items():
        if v == x:
            return k
    k = prioritize_by_value(dictio, x-1)
    return k
    # evtl. wenn mehrere items mit gleichen values, dann randomisiere die Auswahl!!! o.ä.!!!


# ???                  
def who_s_next(ma_data, itemcolumn):
    
    #create a dict:
        
    data_dic= {m.minion_name: m.prioritize_binary_lists(m.last_years) for m in ma_data}
     
    for dd in data_dic:
        print(dd, ": ", data_dic[dd][itemcolumn])
    
    cnt = itemcolumn
    d_lst= []
    #for cnt in range(10):
    for d in data_dic:
        if data_dic[d][cnt] == max([item[cnt] for item in data_dic.values()]):    
            print("Feiertag, ", cnt, ": ", d)
            d_lst.append(d)
     
    return d
        

#_____

def create_minions(dataseq):
    """ create the minion objects with data from json file"""            
    
    # load json-file:
    daten_mitarb= load_json(dataseq)

    # creating minion objects
    employee= [Minion(ma_id, # id based on list index(enumerate)
    d_ma, # minion name 
    daten_mitarb[d_ma]["last_dienst"], # last_dienste,
    daten_mitarb[d_ma]["last_feiertage"], # last years feiertagsdienste
    daten_mitarb[d_ma]["urlaub"], # urlaub
    daten_mitarb[d_ma]["wunschfrei"], # wunschfrei
    daten_mitarb[d_ma]["wunschdienst"], # wunschdienst
    daten_mitarb[d_ma]["aktuelle_feiertage"])
    for ma_id, d_ma in enumerate(daten_mitarb.keys())]
    
    return employee


# ???
def create_priolist_feiertag(classlist, feiertag):
    """ returns a list of minions that are best choices for duty on specific celebrations day
    
    choice is based of min values and corresponding minions """
    
    priolist= {kandit.minion_name : kandit.feiertage[feiertag] for kandit in classlist}
    
    #print(f"{search}:\n{priolist}\n\nbester Kandidat: {min(priolist.values())}")
    
    best_kandits = {bk for bk in priolist if priolist[bk] == min(priolist.values())}
    
    return best_kandits
    
    
def get_minion(s_datum, classlist, dienst_ds, feiertag = None):
    """            
    new get_minions()!    

    s_datum : Datum das gesucht wird als date-object
    classlist : List of Minion-objects
    dienst_ds : Durchschnittliche Dienstanzahl pro minion
    feiertag: wenn Datum ein Feiertag ist...qaa
    
    checke das nach Möglichkeit nicht mehr Dienste als Durchschnitt sind

    """
       
    # check Feiertag
    if feiertag:
        print(f"  {feiertag}: Feiertagsdienst!\n")
        
        #erstelle values list aus vorigen Jahren:
        values_letzte_jahre = feiertags_values(collect_feiertage(feiertag, classlist))
    
        actual_fdays_list = [sum(ma.feiertage_dieses_jahr) for ma in classlist]

        values_dieses_jahr = feiertags_values(actual_fdays_list)
        
        feiertags_calc = add_feiertagsvalues(values_letzte_jahre, values_dieses_jahr)
        #print(f"\nFeiertagsberechnung:\n\
#  letzte Jahre:{values_letzte_jahre}\n\
#  dieses Jahr:{values_dieses_jahr}\n\
#  insgesamt: {feiertags_calc}\n")
        
        
        
    
        
        #candidates_dict:
            # checke Feiertagsvalue und passe Werte an, im Sinne von, 
            # je länger der Feiertagsdienst her, und andere feiertage dieses 
            # Jahr noch nicht eingetragen, desto höher die Chance Bester Kandidat zu sein...
    
    # checke ob ein minion Wunschdienst will!    
    for ma_wd in classlist:
        if ma_wd.wunschdienst: # if not empty list
            for wd in ma_wd.wunschdienst:
                if ma_wd.check_dates_match(wd, s_datum):
                    print(f"     {ma_wd} will wunschdienst!")
                    set_last_dienst_to_new_values(classlist) #raise last_dienst counter by 1
                    ma_wd.last_dienst = 1
                    ma_wd.raise_count()
                    return ma_wd
                    # evtl speichere erst in candidates_dict mit value 9???

#    # checke nach Urlaub
#    for ma_u in classlist:        
#        if ma_u.urlaub: # if not empty list
#            if not ma_u.check_urlaub(s_datum):
#                #speichere in candidates_dict wenn kein Urlaub
#                candidates_dict[ma_u.minion_name] = ma_u.last_dienst
#            else:
#                candidates_dict[ma_u.minion_name] = 0
#                print(f"{ma_u} hat Urlaub!")
#                
#    print(f"{candidates_dict} : freshly after U-check...")                

   # potentielle we-kandidaten als Prioritätenliste
   # {ma : ma.last_dienst}
    candidates_dict = {}
    #print(f"{candidates_dict} : freshly created...")

    # checke nach Urlaub und erstelle candidates_list
    for ma_u in classlist:        
        if ma_u.urlaub: # if not empty list
            if not ma_u.check_urlaub(s_datum):
                #speichere in candidates_dict wenn kein Urlaub
                candidates_dict[ma_u.minion_name] = ma_u.last_dienst + 2
            else:
                candidates_dict[ma_u.minion_name] = 0
                print(f"     {ma_u} hat Urlaub!")
                
#    print(f"{candidates_dict} : freshly after U-check...")                

        
    # checke nach wunschfrei
    for ma_wf in classlist:
        if ma_wf.wunschfrei: # if not empty list
            for wf in ma_wf.wunschfrei:
                if ma_wf.check_dates_match(wf, s_datum):
                    print(f"     {ma_wf} hat wunschfrei!")
                    candidates_dict[ma_wf.minion_name] = 1 # wird nur in candidates auf 1 gesetzt, nicht im object

#    print(f"{candidates_dict} : after wunschfrei...")                    

    # 1-2 Wochen VOR Wunschdienst KEIN WE-Dienst
    # # wenn minion bis Wunschdienst < 2 Wochen, setze count auf 0 und dann mach was mit!!!
    for ma_vwd in classlist:
        if ma_vwd.wunschdienst:
            for wd in ma_vwd.wunschdienst:
                if ma_vwd.frei_vor_wunschdienst(wd, s_datum, 8):
                    if not candidates_dict[ma_vwd.minion_name] <= 1: # wenn der Minion schon vorheriges WE Dienst oder Urlaub hatte...
                        candidates_dict[ma_vwd.minion_name] = 3 # wird nur in candidates auf 0 gesetzt, nicht im object
                        print(f"     {ma_vwd} kein Abstand zum Wunschdienst!")
                elif ma_vwd.frei_vor_wunschdienst(wd, s_datum, 15):
                    if not candidates_dict[ma_vwd.minion_name] <= 1: # wenn der Minion schon vorheriges WE Dienst oder Urlaub hatte...
                        candidates_dict[ma_vwd.minion_name] = 4 # wird nur in candidates auf 0 gesetzt, nicht im object
                        print(f"     {ma_vwd} zu kurzer Abstand zum Wunschdienst!")

    
    set_last_dienst_to_new_values(classlist) #raise last_dienst counter by 1

    #print("\n")
    
    
    # if feiertag: add feiertags_calc zu candidates_dict
    if feiertag:
        for i_index, i in enumerate(candidates_dict):
            candidates_dict[i] += feiertags_calc[i_index]
    
       # print(f"{candidates_dict} : nach killist...")    
    
    # beginne check mit last_dienst - nimm minion mit höchstem wert!
    for ma_now in classlist:
       if ma_now == prioritize_by_value(candidates_dict, max(candidates_dict.values())):
           ma_now.last_dienst = 1
           ma_now.raise_count()
           if feiertag:
               ma_now.feiertag_dieses_jahr_abhaken(feiertag)
               #print(ma_now.feiertage_dieses_jahr)
           return ma_now

    # was wenn ALLE nicht können???
    #print(candidates_dict)


def collect_feiertage(feiertag, classlist):
    plist_feiertage = [x.feiertage[feiertag] for x in classlist]
    #print(plist_feiertage)
    return plist_feiertage
    
    
def feiertags_values(listobjekt):
    """ return prioritätsvalues für eine list von ints
         höchstes item bekommt 0 dann absteigend + 1"""
    sorted_list = []
    for item in sorted(listobjekt)[::-1]:
        if not item in sorted_list:
            sorted_list.append(item) 

    values = [sorted_list.index(position) for position in listobjekt]
    return values
    

def add_feiertagsvalues(list1, list2):
        """ adds the two lists 
        lastyears feiertagsdienstvalues 
        and 
        thisyears feiertagsdienstvalues 
        and 
        returns a list with added values """
        
        return [list1[p] + list2[p] for p in range(len(list1))]
        

#________________________________________


if __name__ == '__main__':
    
    filename = "mitarb_daten[test].json" #"mitarb_daten[v2].json" #"mitarb_daten.json"
    mitarbeiter = create_minions(filename)
    
    #minions_list =list for easy class instance building
    minions_list = list(mitarbeiter) #[ma for ma in mitarbeiter]
    print(minions_list[0])
    print(mitarbeiter[1])
    print("\n"*2)
    
    #mitarbeiter[5].wunschdienst = (4, 12, 2021)
    mitarbeiter[1].wunschfrei.append([4, 12, 2021])
    mitarbeiter[0].wunschfrei.append([4, 12, 2021])
    
    mitarbeiter[1].wunschfrei.append([15, 4, 2022])
    mitarbeiter[1].wunschfrei.append([1, 5, 2022])
    mitarbeiter[5].wunschfrei.append([1, 5, 2022])
    
    mitarbeiter[3].feiertag_dieses_jahr_abhaken('Ostern')
    
    for e in mitarbeiter:
        e.display_minion()   
     
    #datum= (4, 12, 2021) # datum to look for a minion
    datum = date(2022, 5, 1)
    print(f"gesuchtes Datum: {datum}")
    fday = 'Tag der Arbeit'  #'Weihnachten'  # 'Ostern'
    
    #only for testing purposes:
#   

#    print("\n"*2)

#    

#    #mitarbeiter[5].wunschdienst = (4, 12, 2021)

#    mitarbeiter[1].wunschfrei = (4, 12, 2021)

#    mitarbeiter[0].wunschfrei = (4, 12, 2021)

#    

    this_ma = get_minion(datum, mitarbeiter, 2, fday)
    
    print(f"Diesen Dienst wird {this_ma} übernehmen!")




    #_-_-_-_letzte feiertage:_-_-_-_
    
#    for kandi in mitarbeiter:
#        if kandi == 'Marco':
#            print(f"{kandi}:")
#            for y in kandi.last_years:
#                print(y[:8])
#            for f in kandi.feiertage.items():
#                print(f)

    for kandi in mitarbeiter:
        print(f"\n{kandi}:")
        #for y in kandi.last_years:
            #print(y[:8])
        for f in kandi.feiertage.items():
            if fday in f[0]:
                print("  ", f)


    
    #feiertag_dieses_jahr_abhaken(mitarbeiter[1], fday)
    #mitarbeiter[3].feiertag_dieses_jahr_abhaken(fday)
    
    xlist =  create_priolist_feiertag(mitarbeiter, fday)
    print(f"\n{fday}\n{xlist}\n\
    {list(mitarbeiter[0].feiertage.keys()).index(fday)}")
    
    
#    for kandi in mitarbeiter:
#        print(f"\n{kandi}:\n\
#        {kandi.feiertage_dieses_jahr}: {sum(kandi.feiertage_dieses_jahr)}")
    
    print(f"\nVorjahres Feiertagsbilanz für {fday}:")            
    ft_values1= feiertags_values(collect_feiertage(fday, mitarbeiter))
    print(ft_values1)
    
    print("Allgemeine Feiertagsbilanz für dieses Jahr:")
    actual_fdays_l = [sum(kandi.feiertage_dieses_jahr) for kandi in mitarbeiter]
    print(actual_fdays_l)
    ft_values2= feiertags_values(actual_fdays_l)
    print(ft_values2)
    
    print("")
    print(add_feiertagsvalues(ft_values1, ft_values2))
    

    # save a json_file:
    #save_json(filename, mitarbeiter)
        
        
        
        
    
    #xxx: name of ma
    
    #xxx.display_last_years_duties()
    
    ###print("\n"*2)
    
    
    #_-_-_-_load save datasequence_-_-_-_
    
    # save a json-file:
    ###save_json("mitarb_daten.json")
    
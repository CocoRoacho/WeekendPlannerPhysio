from kivy.lang import Builder

from kivymd.app import MDApp

from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from kivymd.theming import ThemableBehavior

from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem, ILeftBody, OneLineAvatarListItem, OneLineAvatarIconListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
#from kivymd.uix.card import MDCard

from kivymd.theming import ThemableBehavior
from kivy.uix.modalview import ModalView
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivymd.color_definitions import colors, palette

from libs.dialog_change_theme import DPDialogChangeTheme
from libs.feiertage import Feiertage

from backend.Mitarbeiter_mgmt import Minion, create_minions, get_minion
from backend.weekends_mgmt import Dienste, create_dienste_obj 
#, ... ???????????????



import datetime

feiertage_file= "./data/Feiertagsliste.json"

testlist = [
    ["18./19. Dezember 2021","" , "Marco"],
    ["24./25./26. Dezember 2021", "Weihnachten", "Katrin"],
    ["31. Dezember/1./2. Januar 2022", "Silvester/Neujahr", "Michael"],
    ["8./9. Januar 2022","" , "Petra"],
    ["15./16. Januar 2022","" , "Ines"],
    ["22./23. Januar 2022","" , "Marco"],
    ["29./30. Januar 2022","" , "Kerstin"],
    ["5./6. Februar 2022","" , "Michael"],
    ["12./13. Februar 2022","" , "Katrin"],
    ["19./20. Februar 2022","" , "Marco"],
    ["26./27. Februar 2022","" , "Petra"],
    ["5./6. März 2022","" , "Ines"],
    ["12./13. März 2022","" , "Kerstin"],
    ["19./20. März 2022","" , "Michael"],
    ["26./27. März 2022","" , "Katrin"],
    ["2./3. April 2022","" , "Marco"],
    ["9./10. April 2022","" , "Petra"],
    ["15./16. April 2022","Ostern" , "Ines"],
    ["17./18. April 2022","Ostern" , "Michael"],
    ["23./24. April 2022","" , "Kerstin"],
    ["30. April/1. Mai 2022","Tag der Arbeit" , "Katrin"],
    ["7./8. Mai 2022","" , "Marco"],
    ["14./15. Mai 2022","" , "Petra"],
    ["21./22. Mai 2022","" , "Ines"],
    ["26./28./29. Mai 2022", "Himmelfahrt", "Michael"],
    ["4./5./6. Juni 2022", "Pfingsten", "Katrin"]
    ]


def my_date_format(dateobj):
        """ formats the datetime modul to my likings --> dd/mm/yyyy """
        return f"{dateobj.day}/{dateobj.month}/{dateobj.year}"



class MyDienstplanScreen(MDScreen):
    
    
    #def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        
        #self.date_from = StringProperty(None)
        #self.date_to = StringProperty(None)
     

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        #print(instance, value, date_range)
        
        app= MDApp.get_running_app()
        

        # Error catching, wenn user inputs strange values!!!!!
        app.date_from = date_range[0]
        app.date_to = date_range[-1]
        
        datefrom= my_date_format(app.date_from)
        datetil= my_date_format(app.date_to)
        print(f"\nvon: {datefrom} bis: {datetil}\n")
        self.ids.btn_date.text = f"{datefrom} - {datetil}"


    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        # right now nothing will be called


    def show_date_picker(self):
        """ set to ask for a date range """
        
        date_dialog = MDDatePicker(
            mode="range", 
            min_year=2020, 
            max_year=2070)

        date_dialog.bind(
            on_save=self.on_save, 
            on_cancel=self.on_cancel)

        date_dialog.open()


    def start_planning(self):
        """ start button for collecting all needed data and begin weekend planning """

        #self.date_from
        #self.date_to
        
        app= MDApp.get_running_app()
        
        if self.ids.btn_date.text != "Zeitraum": #self.date_from and self.date_to:
        
            print(f"Die Planung für den Zeitraum von {app.date_from} bis {app.date_to} beginnt!")

            """
            # fill mdlist with items for testing...

            for litem in testlist:
                if litem[1]: # == Feiertag
                    self.ids.container.add_widget(
                        ThreeLineListItem(text=litem[0], secondary_text=litem[2], tertiary_text=litem[1])
                    )
                else:
                    self.ids.container.add_widget(
                        TwoLineListItem(text=litem[0], secondary_text=litem[2])
                    )
            """                    

            # run weekendplanner w arg date_from, date_to,  app.feiertage
            
            # create dienste objects
            dienste = create_dienste_obj(app.date_from, app.date_to, app.feiertage.ft_dic)
            
            # Durchschnittliche Anzahl von Diensten pro Minion
            dienstdurchschnitt= round(len(dienste)/len(mitarbeiter), 2)
            print(f"dienstdurchschnitt: {dienstdurchschnitt}")
            
            # find minion for dienste
            for dienst in dienste:
                
                dienst.opfer = get_minion(dienst.daten[0], mitarbeiter, dienstdurchschnitt, dienst.feiertag_name)
                #dienst.opfer = dienstmaker

             # output as listitem   
            for dienst in dienste:
                if dienst.feiertag_name: # dann feiertag = True
                    self.ids.container.add_widget(
                        TwoLineListItem(text=dienst.name, secondary_text=str(dienst.opfer), tertiary_text=dienst.feiertag_name)
                    )
                else:
                    self.ids.container.add_widget(
                        TwoLineListItem(text=dienst.name, secondary_text=str(dienst.opfer))
                    )

        else:
            print("Erst den Zeitraum festlegen!!!")
            self.dialog = MDDialog(
                text= "Erst den Zeitraum festlegen!!!"
                )
            self.dialog.open()


class FeiertagEditScreen(MDScreen):
    
   
    def fill_feiertage(self):
        """ loads the list of feiertage from a json file """      
        
        app= MDApp.get_running_app()

        if not app.feiertage: # create if not exist?
            app.feiertage = Feiertage(feiertage_file)

        self.update_listwidget()

        #for feiertagitem in app.feiertage.ft_alle:
        #    self.ids.feiertags_container.add_widget(
        #        OneLineListItem(text=f"{feiertagitem[0]}: {feiertagitem[1]}"))
            

    def update_listwidget(self):
        """ at first delete all child widgets dann fülle upgedatete Daten wieder auf """

        self.ids.feiertags_container.clear_widgets()

        app= MDApp.get_running_app()

        for feiertagitem in app.feiertage.ft_alle:
            self.ids.feiertags_container.add_widget(
                OneLineListItem(text=f"{feiertagitem[0]}: {feiertagitem[1]}"))


    '''
    def update_feiertage_list(self):
        """ update Feiertag object liste alle Feiertage... """

        app= MDApp.get_running_app()

        if app.feiertage: # if exist?
            app.feiertage.fill_ft_set()
    '''


    def cleanup_olds(self):
        """ clean up old data, feiertage older than 1 year... """
        
        app= MDApp.get_running_app()
        
        if app.feiertage: # if exist?
            app.feiertage.delete_old_fts()

        # update kivy app listwidget
        self.update_listwidget()
        #self.fill_feiertage()


    def close_dialog(self, obj):
        """ """

        # close dialog
        self.dialog.dismiss()
        
        # open datepicker
        app= MDApp.get_running_app()
        self.show_date_picker(app.feiertage.last_year + 1)


    def add_next_year(self):
        """ expands List of feiertage """
        
        
        #get values for karfreitag of the year you want

        # infobox
        self.dialog = MDDialog(
            text= "Geben Sie das Datum für den Karfreitag des betreffenden Jahres an.",
            buttons=[
                MDFlatButton(
                    text="Okay",
                    #theme_text_color="Custom",
                    #text_color=get_color_from_hex("#344954"),
                    #text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

        
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        #print(instance, value, date_range)
        
        app= MDApp.get_running_app()
               
        if app.feiertage: # if exist?
            app.feiertage.add_new_year(value.year, value.month, value.day)

            # update kivy app listwidget
            #self.fill_feiertage()
            self.update_listwidget()



    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        # right now nothing will be called


    def show_date_picker(self, kf_year):
        """ set to ask for a date range """
        date_dialog = MDDatePicker(
            year=kf_year, 
            month=4, 
            day=1, 
            min_year=kf_year - 2, 
            max_year=kf_year + 23, 
            radius=[9, 9, 9, 26])
        
        date_dialog.bind(
            on_save=self.on_save, 
            on_cancel=self.on_cancel)
        
        date_dialog.open()



class ContentBox(MDBoxLayout):
    pass


class pdatalistitem(OneLineAvatarIconListItem):
    pass


class OneLineListItem_w_input(OneLineListItem):
    pass


class P_card(MDCard):
    name_lbl = StringProperty(None)


class MyPersonalScreen(MDScreen):
    
    def update_minion_cards(self):
        """ free basegrid from all widgets to create everything new... """

        for ma in mitarbeiter:

            self.ids.minion_basegrid.clear_widgets()

        self.fill_minion_cards()
           
    
    def fill_minion_cards(self):
        """ creates the custom MDCards, fill them with data and expansion panel """

        
        # create and integrate the cards
        for ma in mitarbeiter:

            self.ids.minion_basegrid.add_widget(P_card(name_lbl=f"[b]{ma.minion_name}[/b]"))

        # include the expansion panels in the cards
        for child in self.ids.minion_basegrid.children:

            ma_name= child.name_lbl[3:-4]

            print("text: ", ma_name)


            #datenvorbereitung! # build as function !!!
            for minion in mitarbeiter:
                if minion == ma_name:
                    u_dates = [f"{uitem[0][0]}.{uitem[0][1]}.{uitem[0][2]} - {uitem[1][0]}.{uitem[1][1]}.{uitem[1][2]}" for uitem in minion.urlaub]
                    wfrei_dates = [f"{uitem[0]}.{uitem[1]}.{uitem[2]}" for uitem in minion.wunschfrei]
                    wdienst_dates = [f"{uitem[0]}.{uitem[1]}.{uitem[2]}" for uitem in minion.wunschdienst]

            categories = {"Urlaub": u_dates, 
                          "Wunschdienst": wfrei_dates, 
                          "Wunschfrei": wdienst_dates
                          }

            
            for cat in categories: #["Urlaub", "Wunschdienst", "Wunschfrei"]: # evtl add krank???

                # creates a root widget of my custom widget
                content = ContentBox()

                # add subitems / children
                # was wenn daten fehler auslösen?
                #try:
                #    textdata= datastream[ma_name][cat.lower()] if datastream[ma_name][cat.lower()] else ""
                
                for item in categories[cat]:
                    content.add_widget(pdatalistitem(text=item))

                # letztes widget etwas anders
                content.add_widget(OneLineListItem_w_input(text=f"               {cat} hinzufügen"))

                # do the panels finally
                child.add_widget(
                    MDExpansionPanel(
                        on_open=self.panel_open,
                        on_close=self.panel_close,
                        #icon=f"{images_path}kivymd_logo.png",
                        content=content,
                        panel_cls=MDExpansionPanelOneLine(text=cat),
                    )
                )

        
    def panel_open(self, *args):
        """ when panel opens ?"""
        Animation(
            height=(self.root.ids.box.height + self.root.ids.content.height)
            - self.theme_cls.standard_increment * 2,
            d=0.2,
        ).start(self.root.ids.box)

    
    def panel_close(self, *args):
        """ when panel closes ?"""
        Animation(
            height=(self.root.ids.box.height - self.root.ids.content.height)
            + self.theme_cls.standard_increment * 2,
            d=0.2,
        ).start(self.root.ids.box)




    

        

class MySettingsScreen(MDScreen):
    pass


class WEDienstPlaner(MDScreen):
    #base layout as backend 
    pass








class NavRailApp(MDApp):
    
    date_from = None
    date_to = None
    
    feiertage = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        # default theme
        self.theme_cls.primary_palette = "Lime"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style="Dark"
        
        # app settings defaults
        self.title = "Wochenend Dienstplaner"

        # variables
        self.dialog_change_theme = None
        self.data_dialog = None
        
     
    def find_roots(self):
        print("self")
        print(self)

        print("root")
        print(dir(self.root))

        print("=======" * 5)
        print("\nself.root.manager: ")
        if not self.root.manager == None:
            for item in self.root.manager:
                print(item)
        print("\n")

        print("=======" * 5)
        print("\nself.root.ids: ")
        for item in self.root.ids:
            print(item)
        print("\n")

        print("screen_manager.ids")
        print(self.root.ids.screen_manager.ids)
        print("=======" * 5)
        
        print("=======" * 5)
        print(f"root: {self.root}")
        print("dir(root)")
        self.find_roots()
        

        print("=======" * 5)
        
        
    def build(self):
        """ initialisation process related """

        self.root = WEDienstPlaner()
        
        
        #print(f"Nav rail state: {self.root.ids.rail.rail_state}") # shows the state of the navrail: open or close


    def rail_open(self):
        """ for opening and closing of the navrail widget """

        if self.root.ids.rail.rail_state == "open":
            self.root.ids.rail.rail_state = "close"
        else:
            self.root.ids.rail.rail_state = "open"


    def switch_theme_style(self):
        """ switch between dark and light mode """
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        )
        #????self.root.ids.backdrop.ids._front_layer.md_bg_color = [0, 0, 0, 0]


    def show_dialog_change_theme(self):
        if not self.dialog_change_theme:
            self.dialog_change_theme = DPDialogChangeTheme()
            self.dialog_change_theme.set_list_colors_themes()
        self.dialog_change_theme.open()


       



    def on_start(self):
        """Creates a list of items with examples on start screen."""

        Builder.load_file("./libs/dialog_change_theme.kv")

        # create the personalscreen for startup by accessing the method from (class) MyPersonalScreen
        print("self.root.ids.screen_manager.get_screen : ", dir(self.root.ids.screen_manager.get_screen('personal')))
        self.root.ids.screen_manager.get_screen('personal').fill_minion_cards()


if __name__ == "__main__":

    # 1. prepare data:

    # create minions from file
    ma_dienstdaten_file = "./data/mitarb_dienst_daten.json"

    # create mitarbeiter objects
    mitarbeiter = create_minions(ma_dienstdaten_file)

    print(type(mitarbeiter))
    print(type(mitarbeiter[0]))
    print(mitarbeiter[0].minion_id)

    for m in mitarbeiter:
        print(m)

    # 2. load Feiertage from file

    # 3. start app gui



    NavRailApp().run()



#####################################
#                                   #  
#   utf-8 coding gone wrong...      #
#                                   #
# >> hex(ord('Ä'))                  #
#                                   #
# --> '0xc4'                        #
#                                   #
# --> string = u"\u00c4nderung"...  #
#                                   #
#####################################
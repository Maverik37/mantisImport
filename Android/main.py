from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from tools import DatabaseHelper, StationInfo
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

# Builder.load_file("main.kv")

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        #On appelle la classe DatabaseHelper
        try:
            self.bdd = DatabaseHelper()
            self.bdd.initiate_db()
            tab_box = self.ids.table
            self.tableau=""
        except Exception as e:
            pass
    pass

    def on_pre_enter(self, *largs):
        bdd = DatabaseHelper()
        stations = bdd.select_stations()
        tab_box = self.ids.table
        tab_box.clear_widgets()
        infos = StationInfo(stations)
        data = infos.get_gazole_price()
        if data is None:
            data = [("pas de","données")]
        self.tableau = MDDataTable(
            use_pagination=False,
            size_hint=(.4, .8),
            pos_hint={"center_x": .5, "top": .85},
            column_data=[
                ("Station", dp(40)),
                ("Prix", dp(30)),
            ],
            row_data=data,
        )
        tab_box.add_widget(self.tableau)

class AjoutScreen(Screen):

    def __init__(self, **kwargs):
        super(AjoutScreen,self).__init__(**kwargs)

    def bdd_add_id(self):
        id = self.ids.station_id.text
        conn = DatabaseHelper()
        conn.add_stations_id(id)
    pass
class DeleteStationScreen(Screen):
    def __init__(self, **kwargs):
        super(DeleteStationScreen, self).__init__(**kwargs)
        self.tableau = self.ids.table_liste_stations
        self.tableau = ""
        self.checked = []

    def on_pre_enter(self, **kwargs):
        bdd = DatabaseHelper()
        stations = bdd.select_stations()
        tab_box = self.ids.table_liste_stations
        tab_box.clear_widgets()
        data = StationInfo(stations).get_station_liste()
        if data is None:
            data = [("pas de","données")]
        self.tableau = MDDataTable(
            use_pagination=False,
            check=True,
            size_hint=(.1, .8) ,
            pos_hint={"center_x": .5, "center_y": .4},
            column_data=[
                ("Station", dp(40)),
                ("id", dp(30)),
            ],
            row_data=data,
        )
        tab_box.add_widget(self.tableau)
        self.tableau.bind(on_check_press=self.on_check_press)
    def on_check_press(self,instance_table,current_row):
        '''Called when the check box in the table row is checked.'''
        if self.checked is None:
            self.checked.append(current_row)
        elif current_row not in self.checked:
            self.checked.append(current_row)
        else:
            index_to_delete = self.checked.index(current_row)
            del self.checked[index_to_delete]
        return self.checked

    def delete_station(self):
        id_to_delete = []
        bdd = DatabaseHelper()
        for id in self.checked:
            id_to_delete.append(id[-1])
        print(id_to_delete)
        bdd.delete_stations(id_to_delete)

    pass
class MainApp(MDApp):

    def build(self):
        self.icon = "Icon/fuel.png"
        screenmanager = MDScreenManager()
        screenmanager.add_widget(MenuScreen(name="menu"))
        screenmanager.add_widget(AjoutScreen(name="addnewstations"))
        screenmanager.add_widget(DeleteStationScreen(name="deletestation"))
        return screenmanager

    def return_home(self):
        self.root.current = "menu"


MainApp().run()
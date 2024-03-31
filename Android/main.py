from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from tools import DatabaseHelper, get_gazole_price
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
        data = get_gazole_price(stations)
        self.tableau = MDDataTable(
            use_pagination=False,
            size_hint=(.2, 0.5),
            pos_hint={"center_x": .5, "center_y": .5},
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

class MainApp(MDApp):

    def build(self):
        self.icon = "Icon/fuel.png"
        screenmanager = MDScreenManager()
        screenmanager.add_widget(MenuScreen(name="menu"))
        screenmanager.add_widget(AjoutScreen(name="addnewstations"))
        return screenmanager

    def return_home(self):
        self.root.current = "menu"


MainApp().run()
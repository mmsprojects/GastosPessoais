from kivy.lang import Builder
#from PIL import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivymd.uix.spinner import MDSpinner
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.slider import MDSlider
from kivymd.uix.toolbar import MDToolbar, MDBottomAppBar
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton, MDRaisedButton, MDFloatingActionButton,MDIconButton
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.chip import MDChip, MDChooseChip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.icon_definitions import md_icons
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64
import ssl
#ssl._create_default_https_context = ssl._create_unverified_context
import time
import datetime
import sqlite3
#import psycopg2
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
from kivmob import KivMob, TestIds, RewardedListenerInterface
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

#matplotlib
from kmplot.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from plyer import vibrator
from kivy.utils import platform
#from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
#from kivy.uix.button import Button
from functools import partial
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,Permission.CAMERA])

from kivymd.uix.filemanager import MDFileManager
import shutil
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
import cv2
import numpy as np
import urllib.request
#from kivy_garden.zbarcam import ZBarCam
from pyzbar.pyzbar import decode
from kivy.core.window import Window
#Window.size = (425, 700)
#Window.size = (700, 1000)

class SQLite_DB():
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def select(self, query):
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.fetchall()

    def update(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def delete(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
        lf.conn.commit()
        return self.cur.fetchall()

    def update(self, query):
        self.cur.execute(query)
        self.conn.commit()

class InitialScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))
        self.window = MDBoxLayout(orientation="vertical",size=(1,1),pos=self.pos)
        #self.window = MDGridLayout()
        #self.window.cols = 1
        self.add_widget(self.window)
        self.window.add_widget(MDLabel(text="",halign="center",size_hint=(1, .3)))
        # image
        self.window.add_widget(Image(source="icon.png"))
        self.window.add_widget(MDLabel(text="", halign="center", size_hint=(1, .3)))
        self.window.add_widget(MDLabel(text="", halign="center", size_hint=(1, .3)))
        self.window.add_widget(MDLabel(text="", halign="center", size_hint=(1, .3)))
        self.grid = MDFloatLayout()#spacing= (50, 50),padding= (50, 50)
        #self.grid.cols = 3
        #self.grid = MDBoxLayout(orientation='horizontal')
        ##
        tela_size = self.size
        icon_size = int(tela_size[0]*0.8)
        self.icon_size = int(tela_size[0]*0.8)
        self.button_relatorio = MDIconButton(text = "Relatórios",icon='relatorio4.png',pos_hint= {"center_x": .8, "center_y": .5},user_font_size= str(icon_size))
        self.button_relatorio.bind(on_press=self.relatorio)
        self.grid.add_widget(self.button_relatorio)

        self.button_backup = MDIconButton(text = "backup", icon='db_backup.png', pos_hint= {"center_x": .8, "center_y": .1},user_font_size= str(icon_size))
        self.button_backup.bind(on_press=self.backup)
        self.grid.add_widget(self.button_backup)

        self.button_restore = MDIconButton(text = "restore", icon='restore_db.png', pos_hint= {"center_x": .5, "center_y": .1},user_font_size= str(icon_size))
        self.button_restore.bind(on_press=self.restore)
        self.grid.add_widget(self.button_restore)

        self.button_add_account = MDIconButton(text = "add_account", icon='add_acount.png', pos_hint= {"center_x": .8, "center_y": .3},user_font_size= str(icon_size))
        self.button_add_account.bind(on_press=self.add_conta)
        self.grid.add_widget(self.button_add_account)

        self.button_edit_account = MDIconButton(text = "edit_account", icon='edit_acount.png', pos_hint= {"center_x": .5, "center_y": .3},user_font_size= str(icon_size))
        self.button_edit_account.bind(on_press=self.edit_conta)
        self.grid.add_widget(self.button_edit_account)

        self.button_add_expense = MDIconButton(text = "add_expense", icon='add_expense.png', pos_hint= {"center_x": .2, "center_y": .5},user_font_size= str(icon_size))
        self.button_add_expense.bind(on_press=self.add_gasto)
        self.grid.add_widget(self.button_add_expense)

        self.button_qr_code = MDIconButton(text = "qr_code_scanner", icon='qrcode_scan.png', pos_hint= {"center_x": .5, "center_y": .5},user_font_size= str(icon_size))
        self.button_qr_code.bind(on_press=self.qr_code)
        self.grid.add_widget(self.button_qr_code)

        self.button_csv = MDIconButton(text = "csv", icon='csv.png', pos_hint= {"center_x": .2, "center_y": .1},user_font_size= str(icon_size))
        self.button_csv.bind(on_press=self.callback_iniciar)
        self.grid.add_widget(self.button_csv)

        self.button_table = MDIconButton(text = "table", icon='table.png', pos_hint= {"center_x": .2, "center_y": .3},user_font_size= str(icon_size))
        self.button_table.bind(on_press=self.tabela)
        self.grid.add_widget(self.button_table)
        # Label welcome
        self.label_welcome = MDLabel(text="",halign="center",size_hint=(1, .6))
        self.window.add_widget(self.label_welcome)
        # button
        self.button_iniciar = MDRoundFlatButton(text="Iniciar", pos_hint= {"center_x": .5, "center_y": .4})
        self.button_iniciar.bind(on_press=self.callback_iniciar)
        #self.window.add_widget(self.button_iniciar)


        self.add_widget(self.grid)
        # Label by
        self.label_by = MDLabel(text="",halign="center",size_hint=(1, .6))
        self.window.add_widget(self.label_by)

    def callback_iniciar(self, instance):
        GastosPessoais.ads.show_banner()
        #self.manager.current = "home_screen"
        print(self.size)
        #self.button_add_expense.user_font_size = str(self.icon_size)

    def add_gasto(self,instance):
        self.manager.current = "gasto_screen"
    def qr_code(self,instance):
        print("qr_code")
        self.manager.current = "camera_screen"
    def relatorio(self,instance):
        sql = """select nome
                 from pessoas"""
        data = self.sqlite_database.select(sql)
        menu_items = []
        for row in data:
            menu_items.append({"text": row['nome'],"viewclass": "OneLineListItem","on_release": partial(self.menu_callback,row['nome'])})

        self.menu = MDDropdownMenu(
            caller=self.button_relatorio,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, item):
        self.relatorio_pessoa = item
        self.manager.screens[2].relatorio_pessoa = item
        self.menu.dismiss()
        self.goRelatorio()
        print(item)
    def goRelatorio(self):
        self.manager.current = "relatorio_screen"
        self.manager.screens[5].plot_grid.clear_widgets()
        self.manager.screens[5].plotar_graficos()
    def tabela(self,instance):
        print("qr_code")
        self.manager.current = "home_screen"
    def add_conta(self,instance):
        print("qr_code")
        self.manager.current = "add_acount_screen"
    def edit_conta(self,instance):
        print("qr_code")
        self.manager.current = "edit_acount_screen"
    def csv(self,instance):
        print("csv")
    def backup(self,instance):
        print("qr_code")
        self.manager.screens[2].backup(instance)
    def restore(self,instance):
        print("qr_code")
        self.manager.screens[2].restore(instance)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.window = MDBoxLayout(orientation="vertical")
        self.window.cols = 1

        self.add_widget(self.window)


        # image
        self.window.add_widget(Image(source="icon.png"))



        # User
        self.user = MDTextField(multiline=False, hint_text='Usuário')
        self.window.add_widget(self.user)

        # Password
        self.password = MDTextField(multiline=False, password=True, hint_text = "Senha")
        self.window.add_widget(self.password)

        # button
        self.button = MDRectangleFlatButton(text="OK")
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

    def conect(self):
        #self.database = Database(str(self.user.text.replace(" ","")),str(self.password.text.replace(" ","")))
        print(self.sqlite_database)
        print(self.user.text)
        print("conectou")
    def callback(self, instance):
        self.label_welcome.text = "Hi " + self.password.text
        self.conect()
        self.manager.current = "home_screen"

    def on_enter(self):
        print("ok")

# 0
    def inserir_gasto(self,instance): #
        if(self.button_date.text!="Selecionar Data/Hora"):
            print("inserir")
            nome_pessoa = self.spinner_pessoa.text
            tipo_gasto = self.spinner_tipo_gasto.text
            data_str = self.button_date.text
            dt, hr = data_str.split()
            print(dt, hr)
            dia, mes, ano = dt.split("/")
            if(len(dia)==1):
                dia = "0"+dia
            if(len(mes)==1):
                mes = "0"+mes
            hora, minuto = hr.split(":")
            if(len(hora)==1):
                hora = "0"+hora
            if(len(minuto)==1):
                minuto = "0"+minuto
            data_string = dia+"/"+mes+"/"+ano[2:]+" "+hora+":"+minuto+":00"

            date_time_obj = datetime.datetime.strptime(data_string, '%d/%m/%y %H:%M:%S')
            print(date_time_obj)
            cnpj = self.cnpj.text
            nome_empresa = self.nome_empresa.text
            valor = float(self.valor.text)
            sql = f"""INSERT INTO gastos_pessoais(id,pessoa_id,tipo_gasto,data,cnpj_empresa,nome_empresa,valor) 
                            VALUES ((SELECT max(id)+1 from gastos_pessoais),(SELECT id from pessoas where nome = '{nome_pessoa}'),
                                    (select valor from tipos_gastos where nome = '{tipo_gasto}'),'{date_time_obj}','{cnpj}','{nome_empresa}',{valor});"""
            #print(sql)

    def ret_chip_gasolina(self,instance):
        self.tp_gasto = "Gasolina"
        print(self.tp_gasto)
    def ret_chip_alimentacao(self,instance):
        self.tp_gasto = "Alimentação"
        print(self.tp_gasto)
    def ret_chip_saida(self,instance):
        self.tp_gasto = "Saída"
        print(self.tp_gasto)
    def ret_chip_outro(self,instance):
        self.tp_gasto = "Outro"
        print(self.tp_gasto)
    def goToHome(self,*args):
        self.manager.current = "home_screen"
    def getTime(self,*args):
        print("ok")
    def getDate(self,*args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        date_dialog.open()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))

        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)

        #Upper bar
        self.toptoolbar = MDToolbar(title="Gastos Pessoais",)
        self.toptoolbar.left_action_items = [["home", self.goInicial]]
        self.toptoolbar.right_action_items = [["reload", self.reloadTable]]
        self.window.add_widget(self.toptoolbar)
        # Toolbar bottom
        # self.bottomtool = MDBottomAppBar()
        # self.toolbar_bottom = MDToolbar( icon="plus-circle-outline" )
        # #self.toolbar_bottom.on_action_button
        # self.bottomtool.add_widget(self.toolbar_bottom)
        # self.window.add_widget(self.bottomtool)

        #self.qtd = self.getrowsnum()
        self.gastos_table = MDDataTable(
            size_hint=(1, 6),
            check = True,
            pos_hint= {"center_x": 1, "center_y": 1},
            use_pagination=True,
            rows_num = 5,
            sorted_on="i",
            sorted_order="DSC",
            column_data=[
                ("i",dp(10)),
                ("ID", dp(10)),
                ("Conta", dp(20)),
                ("Tipo", dp(30)),
                ("Data", dp(40)),
                ("Cnpj", dp(30)),
                ("Empresa", dp(70)),
                ("Valor", dp(20)),
                ("Obs", dp(30))
            ]
        )
        self.window.add_widget(self.gastos_table)
        self.float_layout = MDFloatLayout()
        self.button_add = MDFloatingActionButton(icon="plus",
                                                 pos_hint= {"center_x": .8, "center_y": 2.0},
                                                 #elevation= 50,
                                                 user_font_size=40)
        self.button_add.bind(on_press=self.gasto_)
        self.float_layout.add_widget(self.button_add)
        # self.button_send_email = MDFloatingActionButton(icon="email-send",
        #                                          pos_hint= {"center_x": .8, "center_y": 1.3},
        #                                          #elevation= 50,
        #                                          user_font_size=40)
        # self.button_send_email.bind(on_press=self.email_)
        # self.float_layout.add_widget(self.button_send_email)

        self.button_backup = MDFloatingActionButton(icon="backup-restore",
                                                 pos_hint= {"center_x": .6, "center_y": 2.0},
                                                 #elevation= 50,
                                                 user_font_size=40)
        self.button_backup.bind(on_press=self.backup)
        self.float_layout.add_widget(self.button_backup)

        self.button_restore = MDFloatingActionButton(icon="file-restore-outline",
                                                 pos_hint= {"center_x": .4, "center_y": 2.0},
                                                 #elevation= 50,
                                                 user_font_size=40)
        self.button_restore.bind(on_press=self.restore)
        self.float_layout.add_widget(self.button_restore)

        self.button_relatorio = MDFloatingActionButton(icon="chart-line",
                                                 pos_hint= {"center_x": .2, "center_y": 2.0},
                                                 #elevation= 50,
                                                 user_font_size=40)

        self.button_relatorio.bind(on_press=self.open_menu)

        self.float_layout.add_widget(self.button_relatorio)

        self.button_lines = MDFloatingActionButton(icon="table-row-plus-after",
                                                 pos_hint= {"center_x": .2, "center_y": 1.3},
                                                 #elevation= 50,
                                                 user_font_size=40)

        #self.button_lines.bind(on_press=self.open_menu)
        #self.float_layout.add_widget(self.button_lines)

        self.button_delete = MDFloatingActionButton(icon="delete-outline",
                                                 pos_hint= {"center_x": .7, "center_y": 3.3},
                                                 #elevation= 50,
                                                 user_font_size=40)

        self.button_delete.bind(on_press=self.deleteRow)
        self.float_layout.add_widget(self.button_delete)

        self.button_add_user = MDFloatingActionButton(icon="account-plus-outline",
                                                      pos_hint={"center_x": .5, "center_y": 3.3},
                                                      # elevation= 50,
                                                      user_font_size=40)

        self.button_add_user.bind(on_press=self.addUser)
        self.float_layout.add_widget(self.button_add_user)


        self.button_edit_user = MDFloatingActionButton(icon="account-edit-outline",
                                                    pos_hint={"center_x": .3, "center_y": 3.3},
                                                    # elevation= 50,
                                                    #size_hint=(.05, .05),
                                                    #size=(600, 20),
                                                    user_font_size=40)

        self.button_edit_user.bind(on_press=self.editUser)
        self.float_layout.add_widget(self.button_edit_user)

        # self.button_camera = MDFloatingActionButton(icon="qrcode-scan",
        #                                             pos_hint={"center_x": .1, "center_y": 3.3},
        #                                             # elevation= 50,
        #                                             #size_hint=(.05, .05),
        #                                             #size=(600, 20),
        #                                             user_font_size=40)
        #
        # self.button_camera.bind(on_press=self.goCamera)
        # self.float_layout.add_widget(self.button_camera)

        self.window.add_widget(MDLabel())
        self.window.add_widget(MDLabel())
        self.window.add_widget(MDLabel())
        #self.window.add_widget(MDLabel())
        self.window.add_widget(self.float_layout)
        #self.gastos_rows = self.getTable()
        #self.gastos_table.row_data = self.gastos_rows
    def goInicial(self,instance):
        self.manager.current = "inicial_screen"
    def goCamera(self,instance):
        #self.manager.screens[8].camera.play = True
        self.manager.current = "camera_screen"
    def backup(self,instance):
        print("backup")
        self.dialog_backup = MDDialog(
        text='Deseja criar um backup do banco de dados na pasta "Downloads"?', buttons=[MDRaisedButton(text="Cancelar", on_press=self.backup_cancel),MDRaisedButton(text="OK", on_press=self.fazer_backup)],)  #
        self.dialog_backup.open()

    def backup_cancel(self,instance):
        self.dialog_backup.dismiss()

    def fazer_backup(self,instance):
        self.dialog_backup.dismiss()
        self.downloads = '/storage/emulated/0/Download'
        if(platform == 'android'):
            try:
                shutil.copyfile(os.path.join(self.app_path, 'database1.db'), os.path.join(self.downloads, 'database.db'))
                dlg = MDDialog(
                    text='Backup criado com sucesso na pasta "Downloads"!',
                    buttons=[MDRaisedButton(text="OK", on_press=lambda x: dlg.dismiss())],)  #
                dlg.open()
            except:
                dlg = MDDialog(
                    text="Problema ao criar o Backup! Banco de dados vazio!",
                    buttons=[MDRaisedButton(text="OK", on_press=lambda x: dlg.dismiss())], )  #
                dlg.open()
    def restore(self,instance):
        print("restore")
        self.downloads = '/'
        if(platform == 'android'):
            self.downloads = '/storage/emulated/0/Download'
            print(self.downloads)
            #print(self.manager)
            # path = '/data/user/0/'  # path to the directory that will be opened in the file manager
        self.file_manager = MDFileManager(
            exit_manager=lambda x: self.file_manager.close(),  # function called when the user reaches directory tree root
            select_path=self.fazer_restore,  # function called when selecting a file/directory
        )
        self.file_manager.show(self.downloads)
    # def restore_cancel(self,instance):
    #     self.dialog_restore.dismiss()
    def fazer_restore(self,path):
        print("fazer restore")
        print(path)
        if(os.path.basename(path)=='database.db'):
            shutil.copyfile(path,os.path.join(self.app_path, 'database1.db'))
            self.file_manager.close()
            dlg2 = MDDialog(
                text='Backup do banco de dados restaurado com sucesso!',
                buttons=[MDRaisedButton(text="OK", on_press=lambda x: dlg2.dismiss())], )  #
            dlg2.open()
        else:
            self.file_manager.close()
            dlg2 = MDDialog(
                text='Problema ao restaurar o backup! Arquivo database.db não encontrado!',
                buttons=[MDRaisedButton(text="OK", on_press=lambda x: dlg2.dismiss())], )  #
            dlg2.open()
    def addUser(self, instance):
        print("add user")
        self.manager.current = "add_acount_screen"

    def editUser(self, instance):
        print("edit user")
        self.manager.current = "edit_acount_screen"
    def open_menu(self,instance):
        sql = """select nome
                 from pessoas"""
        data = self.sqlite_database.select(sql)
        menu_items = []
        for row in data:
            menu_items.append({"text": row['nome'],"viewclass": "OneLineListItem","on_release": partial(self.menu_callback,row['nome'])})

        self.menu = MDDropdownMenu(
            caller=self.button_relatorio,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
    def menu_callback(self, item):
        self.relatorio_pessoa = item
        self.menu.dismiss()
        self.goRelatorio()
        print(item)

    def sort_on_id(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1]))

    def sort_on_data(self,data):
        return sorted(data, key=lambda l: sum([int(l[-2].split(":")[0]) * 60, int(l[-2].split(":")[1])]))
    def getrowsnum(self):
        sql = "SELECT count(id) qtd from gastos_pessoais"
        data = self.sqlite_database.select(sql)
        for row in data:
            qtd = row['qtd']
        return int(qtd)

    def auto_complete(self):
        selected_rows = self.gastos_table.get_row_checks()
        if(len(selected_rows)==1):
            for row in selected_rows:
                print(row)
                tipo = row[3]
                cnpj = row[5]
                nome_empresa = row[6]
            #self.manager.screens[3].chip_contas.on_touch_down(True)
            self.manager.screens[3].cnpj.text = cnpj
            self.manager.screens[3].nome_empresa.text = nome_empresa
        # else:
        #     self.manager.screens[3].cnpj.text = ""
        #     self.manager.screens[3].nome_empresa.text = ""
    def deleteRow(self,instance):
        selected_rows = self.gastos_table.get_row_checks()
        all_rows = self.gastos_table.row_data
        print(selected_rows)
        #print(all_rows)
        ids = []
        for row in selected_rows:
            if int(row[1]) not in ids:
                ids.append(int(row[1]))
        print(ids)
        # for x in range(0,len(selected_rows)):
        #     for i,row in enumerate(all_rows):
        #         if row[1] in ids:
        #             all_rows.remove(row)
        #             break
        #     self.gastos_table.row_data = all_rows
        sql = "DELETE FROM gastos_pessoais WHERE id in {}".format(str(ids).replace("[","(").replace("]",")"))
        self.sqlite_database.delete(sql)
        print(sql)
        self.gastos_table.row_data = self.getTable()

    def getTable(self):
        print("filling table")
        sql = """SELECT 
                gp.id as i,
                gp.id ,
                ps.nome as pessoa,
                tp.nome as tipo_gasto,
                data,
                cnpj_empresa,
                nome_empresa,
                gp.valor,
                gp.obs
                FROM gastos_pessoais gp
                LEFT JOIN tipos_gastos tp ON gp.tipo_gasto = tp.valor
                LEFT JOIN pessoas ps ON gp.pessoa_id = ps.id
                ORDER BY gp.id DESC
                --WHERE ps.id = 1"""
        print(sql)
        data = self.sqlite_database.select(sql)
        row_list = []
        for row in data:
            row_list.append((row['i'],
                             row['id'],
                             row['pessoa'],
                             row['tipo_gasto'],
                             row['data'],
                             row['cnpj_empresa'],
                             row['nome_empresa'],
                             row['valor'],
                             row['obs']))
        print(row_list)
        return row_list

    def eraseTable(self):
        self.gastos_table.row_data = []

    def reloadTable(self,instance):
        self.eraseTable()
        self.gastos_table.row_data = self.getTable()

    def changer(self, *args):
        self.manager.current = "home_screen"

    def gasto_(self,instance):
        self.auto_complete()
        self.manager.current = "gasto_screen"
        #self.ads = KivMob(TestIds.APP)
        #self.dlg = MDDialog(text="Inserir gasto", type="custom", content_cls = gasto())
        #self.dlg = MDDialog(text="Inserir gasto", type="custom", content=content)
        #self.dlg.open()

    def email_(self,instance):
        self.manager.current = "email_screen"

    def goRelatorio(self):
        self.manager.current = "relatorio_screen"
        self.manager.screens[5].plot_grid.clear_widgets()
        self.manager.screens[5].plotar_graficos()


class GastoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_time = datetime.datetime.strptime("12:30:00", '%H:%M:%S')
        self.last_year = 2021
        self.last_month = 7
        self.last_day = 31
        self.tp_gasto = None
        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)
        #(self.window.add_widget(MDLabel())
        #Button Inserir

        self.toptoolbar = MDToolbar(size=(600, 5),size_hint=(1, .1))#size_hint=(None, None),
        self.toptoolbar.right_action_items = [["qrcode-scan", self.goCamera]]
        self.window.add_widget(self.toptoolbar)
        self.top_grid = MDGridLayout()
        self.top_grid.cols = 4

        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goToHome)
        self.top_grid.add_widget(self.button_voltar)
        self.top_grid.add_widget(MDLabel())
        self.top_grid.add_widget(MDLabel())
        self.button_apagar = MDRectangleFlatButton(text="Limpar")
        self.button_apagar.bind(on_press=self.erasee)
        self.top_grid.add_widget(self.button_apagar)
        self.window.add_widget(self.top_grid)
        # spinner pessoa
        #self.window.add_widget(MDLabel(text=""))

        sql = """SELECT *
                 FROM pessoas
                      """

        self.app_path = os.path.dirname(os.path.abspath(__file__))

        try:
            self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))

            data = self.sqlite_database.select(sql)
            pessoas = ()
            for row in data:
                pessoas = pessoas + (row['nome'],)



            self.spinner_pessoa = Spinner(
                text='Usuário',
                values= pessoas,
                background_color=(0.500, 0.5, 0.5, 0.5),
                # size_hint=(None, None),
                #size=(600, 20),
                pos_hint={'center_x': .5, 'center_y': .2}
            )
            self.window.add_widget(self.spinner_pessoa)
        except:
            pass
        #self.window.add_widget(self.spinner_tipo_gasto)

        self.grid_tipo = MDGridLayout()
        self.grid_tipo.cols = 1

        self.choose_chip = MDChooseChip()

        self.chip_alimentacao = MDChip(text="Alimentação",selected_chip_color=(.21176470535294, .098039627451, 1, 1),icon='food',size_hint=(0.5, None))
        self.chip_alimentacao.bind(on_press=self.ret_chip_alimentacao)

        self.choose_chip.add_widget(self.chip_alimentacao)

        self.chip_gasolina = MDChip(text="Gasolina",selected_chip_color=(.21176470535294, .098039627451, 1, 1),icon='gas-station',size_hint=(0.5, None))
        self.chip_gasolina.bind(on_press=self.ret_chip_gasolina)
        self.choose_chip.add_widget(self.chip_gasolina)

        self.chip_saida = MDChip(icon='party-popper',text="Saída",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_saida.bind(on_press=self.ret_chip_saida)
        self.choose_chip.add_widget(self.chip_saida)

        self.chip_investimento = MDChip(icon='currency-usd',text="Investimento",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_investimento.bind(on_press=self.ret_chip_investimento)
        self.choose_chip.add_widget(self.chip_investimento)

        self.chip_educacao = MDChip(icon='book-education-outline',text="Educação",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_educacao.bind(on_press=self.ret_chip_educacao)
        self.choose_chip.add_widget(self.chip_educacao)

        self.chip_contas = MDChip(icon='home-currency-usd',text="Contas",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_contas.bind(on_press=self.ret_chip_contas)
        self.choose_chip.add_widget(self.chip_contas)

        self.chip_cartao = MDChip(icon='credit-card-outline',text="Cartão",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_cartao.bind(on_press=self.ret_chip_cartao)
        self.choose_chip.add_widget(self.chip_cartao)

        self.chip_outro = MDChip(icon='bookmark-outline',text="Outro",selected_chip_color=(.21176470535294, .098039627451, 1, 1),size_hint=(0.5, None))
        self.chip_outro.bind(on_press=self.ret_chip_outro)
        self.choose_chip.add_widget(self.chip_outro)

        #self.grid_tipo.add_widget(self.choose_chip)
        self.window.add_widget(self.choose_chip)

        # Button DateTime
        self.button_date = MDRectangleFlatButton(text="Selecionar Data",size_hint= (.5,.6),pos_hint= {"center_x": .5, "center_y": .4})#,icon="calendar")
        self.button_date.bind(on_press=self.getDate)
        self.window.add_widget(self.button_date)

        self.button_hora = MDRectangleFlatButton(text="Selecionar Hora",size_hint= (.5,.6),pos_hint= {"center_x": .5, "center_y": .4})#,icon="calendar")
        self.button_hora.bind(on_press=self.getTime)
        self.window.add_widget(self.button_hora)
        #cnpj
        self.cnpj = MDTextField(multiline=False,hint_text='Cnpj')
        self.window.add_widget(self.cnpj)

        #nome_empresa
        self.nome_empresa = MDTextField(multiline=False,hint_text='Empresa')
        self.window.add_widget(self.nome_empresa)

        #Valor
        self.valor = MDTextField(multiline=False, input_filter='float',hint_text='Valor')
        self.window.add_widget(self.valor)

        #obs
        self.obs = MDTextField(multiline=False,hint_text='Observação')
        self.window.add_widget(self.obs)
        # Button Inserir gasto
        self.button_inserir_gasto = MDRectangleFlatButton(text="Inserir Gasto!", pos_hint= {"center_x": .5, "center_y": .4},size_hint=(1,None))
        self.button_inserir_gasto.bind(on_press=self.inserir_gasto)
        self.window.add_widget(self.button_inserir_gasto)
        self.window.add_widget(MDLabel())
        self.window.add_widget(MDLabel())
        self.i = 0

    def goCamera(self,instance):
        #self.manager.screens[8].camera.play = True
        self.manager.current = "camera_screen"

    def erasee(self,instance):
        self.nome_empresa.text = ""
        self.cnpj.text = ""
        self.valor.text = ""
        self.obs.text = ""
    def inserir_gasto(self,instance): #
        self.i = self.i + 1
        if self.button_date.text!="Selecionar Data" and self.button_hora.text!="Selecionar Hora" and self.tp_gasto!=None and len(self.nome_empresa.text)>0 and self.nome_empresa.text!=None and len(self.valor.text)>0 and self.valor.text!=None:
            print("inserir")
            nome_pessoa = self.spinner_pessoa.text
            tipo_gasto = self.tp_gasto
            dt = self.button_date.text
            hr = self.button_hora.text
            #dt, hr = data_str.split()
            print(dt, hr)
            dia, mes, ano = dt.split("/")
            if(len(dia)==1):
                dia = "0"+dia
            if(len(mes)==1):
                mes = "0"+mes
            hora, minuto,seg = hr.split(":")
            if(len(hora)==1):
                hora = "0"+hora
            if(len(minuto)==1):
                minuto = "0"+minuto

            data_string = dia+"/"+mes+"/"+ano[2:]+" "+hora+":"+minuto+":00"

            date_time_obj = datetime.datetime.strptime(data_string, '%d/%m/%y %H:%M:%S')
            print(date_time_obj)
            cnpj = self.cnpj.text
            if(len(self.nome_empresa.text)>0):
                nome_empresa = self.nome_empresa.text
            else:
                nome_empresa = ""
            if(len(self.valor.text)>0):
                valor = float(self.valor.text)
            else:
                valor = ""

            obs = self.obs.text
            sql = f"""INSERT INTO gastos_pessoais(id,pessoa_id,tipo_gasto,data,cnpj_empresa,nome_empresa,valor,obs) 
                            VALUES ((SELECT max(id)+1 from gastos_pessoais),(SELECT id from pessoas where nome = '{nome_pessoa}'),
                                (select valor from tipos_gastos where nome = '{tipo_gasto}'),'{date_time_obj}','{cnpj}','{nome_empresa}',{valor},'{obs}');"""


            print(sql)

            self.manager.screens[2].sqlite_database.insert(sql)
            self.dialog = MDDialog(
                text="Gasto inserido com sucesso!", buttons=[MDRaisedButton(text="OK", on_press=self.ok), ], )  #
            self.dialog.open()
            #self.ads.request_interstitial()
            #self.i = 0
            #time.sleep(3)
            #self.dialog.dismiss()
            if(platform=='android'):
                vibrator.vibrate(1)

            # self.ads = KivMob(TestIds.APP)
            # self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
            # # Add any callback functionality to this class.
            # self.ads.set_rewarded_ad_listener(RewardedListenerInterface())
            # self.ads.show_rewarded_ad()
        else:
            dlg = MDDialog(
                text='Problema ao inserir o gasto!\nPreencha os senguintes campos:\n-Usuário\n-Tipo\n-Data\n-Hora\n-Empresa\n-Valor',
                buttons=[MDRaisedButton(text="OK", on_press=lambda x: dlg.dismiss())], )  #
            dlg.open()



    def ok(self,instance):
        self.dialog.dismiss()
        if(self.i>2):
            GastosPessoais.ads.show_interstitial()
            GastosPessoais.ads.request_interstitial()
            self.i = 0
    # def on_pre_enter(self, *args):
    #     if(self.i>1):
    #         GastosPessoais.ads.request_interstitial()

    def ret_chip_gasolina(self,instance):
        self.tp_gasto = "Gasolina"
        print(self.tp_gasto)
    def ret_chip_alimentacao(self,instance):
        self.tp_gasto = "Alimentação"
        print(self.tp_gasto)
    def ret_chip_saida(self,instance):
        self.tp_gasto = "Saída"
        print(self.tp_gasto)
    def ret_chip_educacao(self,instance):
        self.tp_gasto = "Educação/Aprendizado"
        print(self.tp_gasto)
    def ret_chip_investimento(self,instance):
        self.tp_gasto = "Investimento"
        print(self.tp_gasto)
    def ret_chip_contas(self,instance):
        self.tp_gasto = "Contas"
        print(self.tp_gasto)
    def ret_chip_cartao(self,instance):
        self.tp_gasto = "Cartão"
        print(self.tp_gasto)
    def ret_chip_outro(self,instance):
        self.tp_gasto = "Outro"
        print(self.tp_gasto)
    def goToHome(self,*args):
        self.manager.current = "home_screen"

    #def on_resume(self):

    def getTime(self,*args):
        print("ok")
        self.time_dialog = MDTimePicker()
        self.time_dialog.set_time(self.last_time)
        self.time_dialog.bind(time=self.time_)
        self.time_dialog.open(pos_hint= {'center_x': .5, 'center_y': .5})

    def time_(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''
        print(time)
        self.last_time = time
        self.button_hora.text = str(time)
        return time
    def getDate(self,*args):
        date_dialog = MDDatePicker(year=self.last_year, month=self.last_month, day=self.last_day)
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.button_date.text = str(value).split("-")[2]+"/"+str(value).split("-")[1]+"/"+str(value).split("-")[0]
        self.last_year = int(str(value).split("-")[0])
        self.last_month = int(str(value).split("-")[1])
        self.last_day = int(str(value).split("-")[2])
        print(instance, value, date_range)

    def on_cancel_date(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''


class EmailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)

        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goToHome)
        self.window.add_widget(self.button_voltar)

        #image e-mail
        self.window.add_widget(Image(source="email.png"))

        # login
        self.user = MDTextField(multiline=False, hint_text='Usuário gmail')
        self.window.add_widget(self.user)

        # Password
        self.password = MDTextField(multiline=False, password=True, hint_text = "Senha gmail")
        self.window.add_widget(self.password)

        # button enviar
        self.button_email = MDRectangleFlatButton(text="Enviar e-mail",pos_hint= {"center_x": .5, "center_y": .3},size_hint=(1,None))
        self.button_email.bind(on_press=self.SMTP_enviar)
        self.window.add_widget(self.button_email)

        self.window.add_widget(MDLabel())
        #self.window.add_widget(MDLabel())

    def goToHome(self, *args):
        self.manager.current = "home_screen"

    # def on_pre_enter(self, *args):
    #     GastosPessoais.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)

    def SMTP_enviar(self,instance):
        t = datetime.datetime.now()
        data = t.strftime('%d/%m/%Y')
        subject = f"Backup DB Gastos Pessoais v1.1- {data}"
        html = f"""\
        <html>
          <head></head>
          <body>
            <p>
                Backup do banco de dados de gastos pessoais SQLite beta.
                <br>
                Att,<br>
                Gastos Pessoais v1.1 - by MMS
            </p>
          </body>
        </html>"""
        sender_email = self.user.text
        receiver_email = sender_email
        password = base64.b64encode(self.password.text.encode("utf-8"))

        print(sender_email)
        print(password)

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email[0]
        message["Subject"] = subject
        # Add body to email
        message.attach(MIMEText(html, "html"))
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(self.app_path, 'database1.db')
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= database.db",
        )
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, str(base64.b64decode(password), "utf-8"))
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
        GastosPessoais.ads.show_rewarded_ad()

class RelatorioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)

        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goToHome)
        self.window.add_widget(self.button_voltar)
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))

        self.plot_grid = MDGridLayout()
        self.plot_grid.cols = 1
        #self.plotar_graficos()

        self.window.add_widget(self.plot_grid)
        self.window.add_widget(MDLabel(text="",halign="center",size_hint=(1, .1)))

        self.rewarded_count = 0

    def plotar_graficos(self):

        #grafico de donut
        fig, (ax1, ax2, ax3) = plt.subplots(3,gridspec_kw={'height_ratios': [2, 1,1]})#,'width_ratios': [0.2]
        fig.tight_layout(pad=2.0)

        #data
        sql = """SELECT tg.nome, sum(gp.valor)
                FROM gastos_pessoais gp,
                tipos_gastos tg
                WHERE gp.tipo_gasto = tg.id 
                AND cast(substr(data,6,2) as real) = (select cast(max(substr(data,6,2)) as real) from gastos_pessoais)
                AND gp.pessoa_id = (select id from pessoas where nome = '{}')
                GROUP BY tg.nome
                ORDER BY tg.nome
                """.format(self.manager.screens[2].relatorio_pessoa)
        names = []
        size = []
        data = self.sqlite_database.select(sql)
        for row in data:
            print(row[0])
            print(row[1])
            names.append(row[0])
            size.append(row[1])
        # create data
        total = sum(size)
        names_values = []
        for i,nm in enumerate(size):
            val = round((nm/total) * 100,1)
            names_values.append(names[i] + ": R$" + str(round(nm,2)) + " ({}%)".format(str(val)))
        print(total)
        print(names_values)
        # Create a circle at the center of the plot
        my_circle = plt.Circle((0, 0), 0.7, color='white')

        # Give color names
        ax1.pie(size, labels=names_values, colors=['orange', 'gray', 'blue', 'skyblue'],
                wedgeprops={'linewidth': 3, 'edgecolor': 'white'})
        p = plt.gcf()
        ax1.add_patch(my_circle)
        ax1.title.set_text('GASTO DO MES CATEGORIZADO')

        #linha
        sql_atual = """SELECT cast(substr(data,9,2) as integer) dia,sum(valor) valor
                        FROM gastos_pessoais 
                        WHERE cast(substr(data,6,2) as real) = (select cast(max(substr(data,6,2)) as real) from gastos_pessoais)
                        AND cast(substr(data,0,5) as integer) = (select max(cast(substr(data,0,5) as integer)) from gastos_pessoais)
                        AND pessoa_id = (select id from pessoas where nome = '{}')
                        GROUP BY substr(data,9,2)
                        ORDER BY substr(data,9,2) asc""".format(self.manager.screens[2].relatorio_pessoa)

        sql_anterior = """SELECT cast(substr(data,9,2) as integer) dia,sum(valor) valor
                            FROM gastos_pessoais
                            WHERE cast(substr(data,6,2) as real) = (select cast(max(substr(data,6,2)) as real)-1 from gastos_pessoais)
                            AND cast(substr(data,0,5) as integer) = (select max(cast(substr(data,0,5) as integer)) from gastos_pessoais)
                            AND pessoa_id = (select id from pessoas where nome = '{}')
                            GROUP BY substr(data,9,2)
                            ORDER BY substr(data,9,2) asc""".format(self.manager.screens[2].relatorio_pessoa)

        data_atual = self.sqlite_database.select(sql_atual)
        data_anterior = self.sqlite_database.select(sql_anterior)

        x1 = list(range(1,32,1))
        y1 = [0]*31

        x2 = list(range(1,32,1))
        y2 = [0]*31

        for row in data_atual:
            y1[int(row['dia'])-1] = float(row['valor'])
        for row in data_anterior:
            y2[int(row['dia'])-1] = float(row['valor'])

        print(y1)
        print(y2)

        ax2.plot(x1, y1,marker='o')
        ax2.plot(x2,y2,marker='o')
        ax2.title.set_text('GASTO MENSAL')
        ax2.legend(['Mês atual','Mês anterior'], loc="upper right")

        #barras
        meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        valores = [0.0]*12

        sql = """SELECT substr(data,6,2) mes, sum(valor) valor
                FROM gastos_pessoais
                WHERE pessoa_id = (select id from pessoas where nome = '{}')
                GROUP BY substr(data,6,2)""".format(self.manager.screens[2].relatorio_pessoa)
        data = self.sqlite_database.select(sql)
        for row in data:
            valores[int(row['mes'])-1] = round(row['valor'],2)
        print(valores)
        ax3.bar(meses,valores)
        for i, v in enumerate(valores):
            if(v>0):
                ax3.text(i-0.40 ,v,str(v), color='black')
        ax3.title.set_text('GASTO ANUAL')
        ax3.set_ylim([0, max(valores)+ 150])
        graph2 = FigureCanvasKivyAgg(plt.gcf())

        self.plot_grid.add_widget(graph2)


    def goToHome(self,*args):
        self.manager.current = "home_screen"
    #def displayAD(self,instance):
    def on_pre_enter(self, *args):
        self.rewarded_count = self.rewarded_count + 1
        if(self.rewarded_count==2):
            #GastosPessoais.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
            GastosPessoais.ads.load_rewarded_ad('ca-app-pub-4966595271619074/2769624912')
    def on_pre_leave(self, *args):
        if(self.rewarded_count==2):
            GastosPessoais.ads.show_rewarded_ad()
            self.rewarded_count = 0
class AddAcountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)

        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goToHome)
        self.window.add_widget(self.button_voltar)

        self.window.add_widget(MDLabel())
        # image e-mail
        self.window.add_widget(Image(source="user.png"))

        # login
        self.user = MDTextField(multiline=False, hint_text='Nome da Conta')
        self.window.add_widget(self.user)

        # login
        self.idade = MDTextField(multiline=False, hint_text='Idade',input_filter='int')
        #self.window.add_widget(self.idade)
        # button enviar
        self.button_add = MDRectangleFlatButton(text="Adicionar", pos_hint={"center_x": .5, "center_y": .3},
                                                  size_hint=(1, None))
        self.button_add.bind(on_press=self.add_user)
        self.window.add_widget(self.button_add)

        self.window.add_widget(MDLabel())
        # self.window.add_widget(MDLabel())
    def goToHome(self,instance):
        self.manager.current = "home_screen"
    def add_user(self,instance):
        print("add_user")
        sql = """INSERT INTO pessoas(id,nome) 
                 VALUES((SELECT max(id)+1 FROM pessoas),'{}')""".format(self.user.text)

        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))

        self.sqlite_database.insert(sql)

        sql = """SELECT *
                 FROM pessoas
                      """
        data = self.sqlite_database.select(sql)
        pessoas = ()
        for row in data:
            pessoas = pessoas + (row['nome'],)
        self.manager.screens[7].spinner_pessoa.values = pessoas
        self.manager.screens[3].spinner_pessoa.values = pessoas

        self.dialog = MDDialog(
            text="Conta adicionada com sucesso!", buttons=[MDRaisedButton(text="OK", on_press=self.ok), ], )  #
        self.dialog.open()

    def ok(self, instance):
        self.dialog.dismiss()
        #GastosPessoais.ads.show_interstitial()

class EditAcountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)

        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goToHome)
        self.window.add_widget(self.button_voltar)

        self.window.add_widget(MDLabel())
        # image e-mail
        self.window.add_widget(Image(source="edit_user.png"))

        self.window.add_widget(MDLabel())

        sql = """SELECT *
                         FROM pessoas
                              """
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_database = SQLite_DB(os.path.join(self.app_path, 'database1.db'))
        data = self.sqlite_database.select(sql)
        pessoas = ()
        for row in data:
            pessoas = pessoas + (row['nome'],)

        self.spinner_pessoa = Spinner(
            text='Conta',
            values=pessoas,
            background_color=(0.500, 0.5, 0.5, 0.5),
            # size_hint=(None, None),
             size=(600, 20),
            pos_hint={'center_x': .5, 'center_y': .2}
        )
        self.window.add_widget(self.spinner_pessoa)
        # novo usuario
        self.user = MDTextField(multiline=False, hint_text='Novo nome da Conta')
        self.window.add_widget(self.user)

        # button editar
        self.button_edit = MDRectangleFlatButton(text="Trocar Conta", pos_hint={"center_x": .5, "center_y": .3},
                                                  size_hint=(1, None))
        self.button_edit.bind(on_press=self.edit_user)
        self.window.add_widget(self.button_edit)

        self.window.add_widget(MDLabel())
        # self.window.add_widget(MDLabel())
    def goToHome(self,instance):
        self.manager.current = "home_screen"
    def edit_user(self,instance):
        print("edit_user")
        sql = """UPDATE pessoas
                SET nome = '{}'
                WHERE nome = '{}'""".format(self.user.text, self.spinner_pessoa.text)
        self.sqlite_database.update(sql)

        sql = """SELECT *
                 FROM pessoas"""

        data = self.sqlite_database.select(sql)
        pessoas = ()
        for row in data:
            pessoas = pessoas + (row['nome'],)
        self.spinner_pessoa.values = pessoas
        self.manager.screens[3].spinner_pessoa.values = pessoas
        self.spinner_pessoa.text = self.user.text

        self.dialog = MDDialog(
            text="Conta alterada com sucesso!", buttons=[MDRaisedButton(text="OK", on_press=self.ok), ], )  #
        self.dialog.open()

    def ok(self, instance):
        self.dialog.dismiss()
        # GastosPessoais.ads.show_interstitial()

class AndroidCamera(Camera):
    camera_resolution = (1920, 1080)
    counter = 0
    def __init__(self,screen, **kwargs):
        super().__init__(**kwargs)
        self.screen_camera = screen



    def _camera_loaded(self, *largs):
        self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
        self.texture_size = list(self.texture.size)

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return None
        frame = self.frame_from_buf()

        self.frame_to_screen(frame)
        super(AndroidCamera, self).on_tex(*l)

    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)
        return np.rot90(frame_bgr, 3)

    def frame_to_screen(self, frame):
        w, h = self.resolution
        h_,w_ = self.camera_resolution
        x0 = int((w_-1000)/2)
        y0 = int((h_-1000)/2)
        x1 = x0 + 1000
        y1 = y0 + 1000
        self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(self.frame_rgb, "Enquadre o QR Code", (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(self.frame_rgb, (x0, y0), (x1, y1), (255, 0, 0), 2)
        self.counter += 1
        flipped = np.flip(self.frame_rgb, 0)
        buf = flipped.tostring()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


    def parse_qrcode(self):
        # self.spin = MDSpinner(size_hint = (None, None), size= (dp(46), dp(46)),pos_hint= {'center_x': .5, 'center_y': .5},active= True)

        h_, w_ = self.camera_resolution
        x0 = int(((w_ - 1000) / 2)-10)
        y0 = int(((h_ - 1000) / 2)-10)
        w=1000+10
        h=1000+10
        gray_img = cv2.cvtColor(self.frame_rgb, 0)
        cropped_img = gray_img[y0:y0+h, x0:x0+w]
        #barcode = decode(cropped_img)
        barcode = decode(gray_img)
        for obj in barcode:
            if(obj.type=='QRCODE'):
                points = obj.polygon
                (x, y, w, h) = obj.rect
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(self.frame_rgb, [pts], True, (0, 255, 0), 3)
                decodedText = obj.data.decode("utf-8")
                print(decodedText)
                barcodeType = obj.type
                # string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)

                # cv2.putText(self.frame_rgb, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                # print("Barcode: " + barcodeData + " | Type: " + barcodeType)

                if (len(decodedText)> 0):
                    #try:
                    self.nfce = self.parse_nfce(decodedText)
                    print(self.nfce)
                    self.dialog = MDDialog(
                        text=f'QR Code lido com sucesso!\n\nEmpresa: {self.nfce["empresa"]}\nCNPJ: {self.nfce["cnpj"]}\nData: {self.nfce["data"]}\nHora: {self.nfce["hora"]}\nValor: {self.nfce["valor"]}',
                        buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)],)  #
                    self.dialog.open()
                    self.status = 1
                        # self.spin.active = False
                    #except:
                        # self.dialog = MDDialog(
                        #     text='Problema na extração de informações, QR Code Inválido!',
                        #     buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)], )  #
                        # self.dialog.open()
                        # self.status = 0

                    # print(mystr)
                else:
                    self.dialog = MDDialog(
                        text='QR Code Inválido/Nulo!',
                        buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)], )  #
                    self.dialog.open()
                    self.status = 0
                    # self.spin.active = False
            break
    def dialog_ok(self,instance):

        self.dialog.dismiss()
        if(self.status==1):
            self.screen_camera.manager.screens[3].nome_empresa.text = self.nfce['empresa']
            self.screen_camera.manager.screens[3].cnpj.text = self.nfce['cnpj'].replace(".","").replace("/","").replace("-","")
            self.screen_camera.manager.screens[3].button_date.text = self.nfce['data']
            self.screen_camera.manager.screens[3].button_hora.text = self.nfce['hora']
            self.screen_camera.manager.screens[3].valor.text = str(self.nfce['valor'])

            self.screen_camera.manager.current = "gasto_screen"
        print("ok")

    # def parse_qrcode(self):
    #     h_, w_ = self.camera_resolution
    #     x0 = int(((w_ - 1000) / 2)-10)
    #     y0 = int(((h_ - 1000) / 2)-10)
    #     w=1000+10
    #     h=1000+10
    #     cropped_img = self.frame_rgb[y0:y0+h, x0:x0+w]
    #     self.qrCodeDetector = cv2.QRCodeDetector()
    #     decodedText, points, _ = self.qrCodeDetector.detectAndDecode(cropped_img)
    #     qr_data = decodedText.split(',')
    #     qr_size = qr_data[0]
    #     print(decodedText)
    #     self.status = 0
    #     if (len(decodedText)>0):
    #         try:
    #             self.nfce = self.parse_nfce(decodedText)
    #             print(self.nfce)
    #             self.dialog = MDDialog(
    #                 text=f'QR Code lido com sucesso!\n\nEmpresa: {self.nfce["empresa"]}\nCNPJ: {self.nfce["cnpj"]}\nData: {self.nfce["data"]}\nHora: {self.nfce["hora"]}\nValor: {self.nfce["valor"]}',
    #                 buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)],)  #
    #             self.dialog.open()
    #             self.status = 1
    #         except:
    #             self.dialog = MDDialog(
    #                 text='Problema na extração de informações, QR Code Inválido!',
    #                 buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)], )  #
    #             self.dialog.open()
    #             self.status = 0
    #         # print(mystr)
    #     else:
    #         self.dialog = MDDialog(
    #             text='QR Code Inválido/Nulo!',
    #             buttons=[MDRaisedButton(text="OK", on_press=self.dialog_ok)], )  #
    #         self.dialog.open()
    #         self.status = 0
    # def dialog_ok(self,instance):
    #     self.dialog.dismiss()
    #     if(self.status==1):
    #         self.manager.current = "gasto_screen"
    #     print("ok")

    def parse_nfce(self,url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()

        # print(mystr)

        cnpj_i = mystr.find("CNPJ:")
        cnpj_f = mystr[cnpj_i:].find("</div>")
        cnpj = mystr[cnpj_i + cnpj_f - 18:cnpj_i + cnpj_f]

        empresa_text = mystr[:cnpj_i].split("<div")[-2]
        empresa_i = empresa_text.find('">')
        empresa_f = empresa_text.find('</div>')
        empresa = empresa_text[empresa_i + 2:empresa_i + empresa_f].split("</div")[0]

        valor_text = mystr[mystr.find("Valor a pagar R$:"):]
        valor_i = valor_text.find(",")
        valor_ii = valor_text.rfind('>', 0, valor_i)
        valor_f = valor_text[valor_i:].find("<")
        print(valor_text[valor_ii:valor_i + valor_f].replace(",", ".").replace(">", "").replace(">", ""))
        valor = float(valor_text[valor_ii:valor_i + valor_f].replace(",", ".").replace(">", "").replace(">", ""))

        data_hora_i = mystr.find("Emissão:")
        data_hora_text = mystr[data_hora_i:].replace(" ", "")
        data_hora_f = data_hora_text.find("-ViaConsumidor")
        data_hora = data_hora_text[data_hora_f - 18:data_hora_f]

        data = data_hora[:10]
        hora = data_hora[10:]

        return {"empresa": empresa,
                "cnpj": cnpj,
                "data": data,
                "hora": hora,
                "valor": valor
                }
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #
    def on_pre_enter(self, *args):
        # self.spin = MDSpinner(size_hint=(None, None), size=(dp(46), dp(46)), pos_hint={'center_x': .5, 'center_y': .5},
        #                       active=True)
        # self.float_layout_spin = MDFloatLayout()
        # self.float_layout_spin.add_widget(self.spin)
        # self.add_widget(self.float_layout_spin)
        self.camera = AndroidCamera(self,index=0, allow_stretch=True, play=True, resolution=(1920, 1080))

        #self.camera.play = True

        self.window = MDGridLayout()
        self.window.cols = 1
        self.add_widget(self.window)
        self.button_voltar = MDRectangleFlatButton(text="Voltar")
        self.button_voltar.bind(on_press=self.goGastos)
        self.window.add_widget(self.button_voltar)

        self.window.add_widget(self.camera)

        self.float_layout = MDFloatLayout()
        self.button_picture = MDFloatingActionButton(icon="camera-iris",
                                                     pos_hint={"center_x": .5, "center_y": 0.15},
                                                     # elevation= 50,
                                                     user_font_size=40)
        self.button_picture.bind(on_press=self.take_picture)
        self.float_layout.add_widget(self.button_picture)
        self.add_widget(self.float_layout)

    def on_pre_leave(self, *args):
        self.camera.play=False
        #self.window.remove_widget(self.camera)
        #self.camera = None
        # for child in self.window.children:
        #     #print(child)
        #     self.window.remove_widget(child)
        self.window.clear_widgets()

        self.clear_widgets()
        print(self.children)
    def goGastos(self,instance):
        self.manager.current = "gasto_screen"

    def take_picture(self,instance):
        print("picture taken")
        self.dcim = '/storage/emulated/0/DCIM/Camera'
        #self.camera.export_to_png(os.path.join(self.dcim,'qrcode.jpg'))
        self.camera.parse_qrcode()



class GastosPessoais(MDApp):
    #ads = KivMob(TestIds.APP)
    ads = KivMob('ca-app-pub-4966595271619074~2060154841')
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        sm = ScreenManager()
        sm.add_widget(InitialScreen(name="inicial_screen"))
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(GastoScreen(name="gasto_screen"))
        sm.add_widget(EmailScreen(name="email_screen"))
        sm.add_widget(RelatorioScreen(name="relatorio_screen"))
        sm.add_widget(AddAcountScreen(name="add_acount_screen"))
        sm.add_widget(EditAcountScreen(name="edit_acount_screen"))
        sm.add_widget(CameraScreen(name="camera_screen"))

        # self.ads = KivMob(TestIds.APP)
        # self.ads.new_interstitial(TestIds.INTERSTITIAL)
        # self.ads.request_interstitial()
        # self.ads.show_interstitial()


        self.ads.new_banner('ca-app-pub-4966595271619074/8924397354', top_pos=False)
        #self.ads.new_banner(TestIds.BANNER, top_pos=False)
        self.ads.request_banner()


        #self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.new_interstitial('ca-app-pub-4966595271619074/8716539444')
        self.ads.request_interstitial()
        #self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
        self.ads.load_rewarded_ad('ca-app-pub-4966595271619074/2769624912')
        self.ads.set_rewarded_ad_listener(RewardedListenerInterface())

        return sm

    def on_resume(self):
        self.ads.request_interstitial()
        self.ads.load_rewarded_ad('ca-app-pub-4966595271619074/2769624912')

    def presser(self):
        print("ok")
        self.ads.show_interstitial()

if __name__ == "__main__":
    a = GastosPessoais().run()
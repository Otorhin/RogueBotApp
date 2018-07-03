# -*- coding: utf-8 -*-
import RogueBot
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker

RogueBotString = """
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDSpinner kivymd.spinner.MDSpinner

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "RogueBot"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Играть"
            on_release: app.root.ids.scr_mngr.current = 'RogueBotMain'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Настройки"
            on_release: app.root.ids.scr_mngr.current = 'settings'
    BoxLayout:
        id : BoxLayoutinNL
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'RogueBot'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'settings'
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(48)
                        spacing: 20
                        MDLabel:
                            font_style: 'Headline'
                            text : 'Ваш токен : ' 
                        MDTextField:
                            hint_text: "Введите ваш токен"
                            required: True
                            id : RogueBotUserToken
                            helper_text_mode: "on_error"
                        MDRaisedButton:
                            size_hint: None, None
                            size: 3 * dp(48), dp(48)
                            center_x: self.parent.center_x
                            text: 'Сменить тему приложения'
                            on_release: MDThemePicker().open()
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y' : 0.1}
                        MDLabel:
                            text: "Текущая тема: " + app.theme_cls.theme_style + ", " + app.theme_cls.primary_palette
                            theme_text_color: 'Primary'
                            pos_hint: {'center_x': 0.5}
                            halign: 'center'
                MDRaisedButton:
                    text: "Сохранить настройки"
                    elevation_normal: 2
                    opposite_colors: True
                    pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                    on_release : app.RogueBotStart()
            Screen:
                name: 'RogueBotMain'
                BoxLayout :
                    padding : dp(20)
                    orientation: 'vertical'
                    MDLabel:
                        text: app.RB_text
                        font_style : 'Subhead'
                        theme_text_color : 'Primary'
                        id : RogueBotMainScreen
                        size_hint_y: None
                        height: dp(450)
        
                    Widget:
    
                    MDRaisedButton:
                        text: 'Доступные действия'
                        opposite_colors: True
                        size_hint: None, None
                        size: dp(75), dp(45)
                        pos_hint: {'center_x': .5}
                        on_release:
                            app.show_example_bottom_sheet()
            Screen :
                name : 'LoadingRB'
                MDSpinner:
                    id: spinner
                    size_hint: None, None
                    size: dp(46), dp(46)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    active: True
"""

otrh_kost = None

class RogueBotApp(App):
    theme_cls = ThemeManager()
    title = "RogueBot"
    appname = "RogueBot"

    RB_text = 'Вы не авторизированы.'
    RB_button = []
    RB_token = ''

    def RB_update():
        global otrh_kost
        self = otrh_kost
        new_update = RogueBot.get_message(RogueBotApp.RB_token)
        if new_update:
            RogueBotApp.RB_text, RogueBotApp.RB_button = new_update
            self.root.ids.RogueBotMainScreen.text = RogueBotApp.RB_text

    def RogueBotStart(self):
        global otrh_kost
        otrh_kost = self
        if RogueBot.validate(self.root.ids.RogueBotUserToken.text):
            RogueBotApp.RB_token = self.root.ids.RogueBotUserToken.text
            RogueBotApp.RB_update()
            self.root.ids.scr_mngr.current = 'RogueBotMain'
        else :
            self.root.ids.scr_mngr.current = 'settings'
            self.show_error_token()

    def show_error_token(self):
        global otrh_kost
        self = otrh_kost
        if self.root.ids.RogueBotUserToken.text == '' :
            text = 'Вы не указали токен'
        else :
            text = 'Вы указали неправильный токен'
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=text,
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Неправильный токен",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.dialog.add_action_button("Вернуться",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def build(self):
        main_widget = Builder.load_string(RogueBotString)

        self.bottom_navigation_remove_mobile(main_widget)

        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

    def RB_Open_Settings(self):
        global otrh_kost
        self = otrh_kost
        self.root.ids.scr_mngr.current = 'settings'


    def show_example_bottom_sheet(self):
        global otrh_kost
        otrh_kost = self
        bs = MDListBottomSheet()
        i = 1
        if RogueBotApp.RB_text == 'Вы не авторизированы.':
            bs.add_item('Авторизоваться', RogueBotApp.RB_Open_Settings)
            bs.open()
            return
        for all in RogueBotApp.RB_button:
            bs.add_item(all, eval('OTRH_RogueBot.otrh_' + str(i)))
            i += 1
        bs.open()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_start(self):
        pass

class OTRH_RogueBot():

    def otrh_1(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[0])
        RogueBotApp.RB_update()

    def otrh_2(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[1])
        RogueBotApp.RB_update()

    def otrh_3(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[2])
        RogueBotApp.RB_update()

    def otrh_4(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[3])
        RogueBotApp.RB_update()

    def otrh_5(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[4])
        RogueBotApp.RB_update()

    def otrh_6(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[5])
        RogueBotApp.RB_update()

    def otrh_7(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[6])
        RogueBotApp.RB_update()

    def otrh_8(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[7])
        RogueBotApp.RB_update()

    def otrh_9(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[8])
        RogueBotApp.RB_update()

    def otrh_10(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[9])
        RogueBotApp.RB_update()

    def otrh_11(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[10])
        RogueBotApp.RB_update()

    def otrh_12(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[11])
        RogueBotApp.RB_update()

    def otrh_13(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[12])
        RogueBotApp.RB_update()

    def otrh_14(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[13])
        RogueBotApp.RB_update()

    def otrh_15(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[14])
        RogueBotApp.RB_update()

    def otrh_16(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[15])
        RogueBotApp.RB_update()

    def otrh_17(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[16])
        RogueBotApp.RB_update()

    def otrh_18(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[17])
        RogueBotApp.RB_update()

    def otrh_19(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[18])
        RogueBotApp.RB_update()

    def otrh_20(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[19])
        RogueBotApp.RB_update()

    def otrh_21(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[20])
        RogueBotApp.RB_update()

    def otrh_22(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[21])
        RogueBotApp.RB_update()

    def otrh_23(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[22])
        RogueBotApp.RB_update()

    def otrh_24(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[23])
        RogueBotApp.RB_update()

    def otrh_25(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[24])
        RogueBotApp.RB_update()

    def otrh_26(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[25])
        RogueBotApp.RB_update()

    def otrh_27(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[26])
        RogueBotApp.RB_update()

    def otrh_28(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[27])
        RogueBotApp.RB_update()

    def otrh_29(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[28])
        RogueBotApp.RB_update()

    def otrh_30(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[29])
        RogueBotApp.RB_update()

    def otrh_31(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[30])
        RogueBotApp.RB_update()

    def otrh_32(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_33(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_34(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_35(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_36(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_37(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_38(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_39(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_40(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_41(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_42(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_43(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_44(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_45(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_46(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_47(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_48(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_49(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()

    def otrh_50(self):
        RogueBot.send_message(RogueBotApp.RB_token, RogueBotApp.RB_button[31])
        RogueBotApp.RB_update()


if __name__ in ('__main__', '__android__'):
    RogueBotApp().run()
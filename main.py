"""
AMR Status Dashboard - Android Version
Created by: Brian Rowe
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.clock import Clock
import requests
import json
from datetime import datetime
from threading import Thread

# API Configuration
API_BASE_URL = "http://10.111.60.163/api/v2.0.0"
AUTH_HEADER = "Basic UmVwb3J0RW5naW5lOmUzYWE2NjY2MzdjYzZjZjA5ZTc2M2YzNTdkYTg3ODdlMDE2MmViYjg5ODdiYjA4OWE0NDJmMmQ3MzFhYjk4OWY="

MISSIONS = [
    {"id": "02a7fd35-db97-569c-2fd4-528173949c28", "name": "PC1 to F1-3", 
     "desc": "PC1 F62 to WIP F1-3 (Assy West Plant)"},
    {"id": "16a718a0-8d74-0609-2b29-8693badd5cfc", "name": "PC1 to F2-1",
     "desc": "PC1 F62 to WIP F2-1 (Assy Mid Plant)"},
    {"id": "2a7fd35-db97-569c-2fd4-528173949c28", "name": "PC1 to F2-2",
     "desc": "PC1 F62 to WIP F2-2 (Assy East Plant)"}
]

class AMRDashboardApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='AMR Status Dashboard\nPC1-C3, C4, C6',
            size_hint_y=0.15,
            bold=True,
            font_size='20sp'
        )
        layout.add_widget(header)
        
        # Status log
        self.log_text = TextInput(
            readonly=True,
            size_hint_y=0.15,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(0, 1, 0, 1)
        )
        layout.add_widget(self.log_text)
        self.log("Dashboard initialized")
        
        # Tabs
        tabs = TabbedPanel(do_default_tab=False)
        
        # Quick missions
        quick_tab = TabbedPanelItem(text='Quick Missions')
        quick_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        for mission in MISSIONS:
            btn = Button(
                text=f"{mission['name']}\n{mission['desc']}",
                size_hint_y=None,
                height=80,
                background_color=(0.2, 0.7, 0.4, 1)
            )
            btn.bind(on_press=lambda x, m=mission: self.launch_mission(m))
            quick_content.add_widget(btn)
        
        self.response_text = TextInput(readonly=True, size_hint_y=0.3)
        quick_content.add_widget(self.response_text)
        
        quick_tab.add_widget(quick_content)
        tabs.add_widget(quick_tab)
        
        # Mission status
        status_tab = TabbedPanelItem(text='Mission Status')
        status_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        refresh_btn = Button(
            text='Refresh Missions',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        refresh_btn.bind(on_press=self.refresh_missions)
        status_content.add_widget(refresh_btn)
        
        self.missions_text = TextInput(readonly=True)
        status_content.add_widget(self.missions_text)
        
        status_tab.add_widget(status_content)
        tabs.add_widget(status_tab)
        
        layout.add_widget(tabs)
        
        # Footer
        footer = Label(
            text='Created By: Brian Rowe',
            size_hint_y=0.05
        )
        layout.add_widget(footer)
        
        return layout
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.text += f"[{timestamp}] {msg}\n"
    
    def launch_mission(self, mission):
        self.log(f"Launching: {mission['name']}")
        self.response_text.text = "Sending request..."
        
        def api_call():
            try:
                headers = {"Authorization": AUTH_HEADER, "Content-Type": "application/json"}
                data = {"mission_id": mission['id'], "priority": 0, "description": mission['desc']}
                response = requests.post(f"{API_BASE_URL}/mission_scheduler", headers=headers, json=data, timeout=10)
                result = response.json()
                Clock.schedule_once(lambda dt: self.handle_launch(True, result, mission['name']), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.handle_launch(False, str(e), mission['name']), 0)
        
        Thread(target=api_call, daemon=True).start()
    
    def handle_launch(self, success, result, name):
        if success:
            self.response_text.text = f"Success!\n{json.dumps(result, indent=2)}"
            self.log(f"Launched: {name}")
        else:
            self.response_text.text = f"Error: {result}"
            self.log(f"Failed: {result}")
    
    def refresh_missions(self, instance):
        self.log("Refreshing missions...")
        self.missions_text.text = "Loading..."
        
        def api_call():
            try:
                headers = {"Authorization": AUTH_HEADER}
                response = requests.get(f"{API_BASE_URL}/mission_scheduler", headers=headers, timeout=10)
                result = response.json()
                Clock.schedule_once(lambda dt: self.handle_missions(True, result), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.handle_missions(False, str(e)), 0)
        
        Thread(target=api_call, daemon=True).start()
    
    def handle_missions(self, success, result):
        if success:
            self.missions_text.text = json.dumps(result, indent=2)
            self.log("Missions loaded")
        else:
            self.missions_text.text = f"Error: {result}"

if __name__ == '__main__':
    AMRDashboardApp().run()

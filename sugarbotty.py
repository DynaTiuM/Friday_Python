import json
import os
import datetime
import pytz

class SugarBotty:
    
    MONEY = 4.05 * 7
    money_file = "money.json"
    holiday = ["2023-11-01"]
    messages_file = "sugarbotty_new_day.json"

    def __init__(self) -> None:
        if not os.path.exists(self.money_file):
            with open(self.money_file, 'w', encoding='utf-8') as f:
                initial_data = {"money": 0.0}
                json.dump(initial_data, f)
    
    def load_messages(self):
        with open(self.messages_file, "r", encoding='utf-8') as f:
            data = json.load(f)
            self.messages = data["messages"]
            self.current_message_index = data["current_index"]
    
    def add_daily_value(self):
        if self.is_work_day():
                with open(self.money_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data["money"] += 4.05 * 7
                self.total_money = data["money"]
                
                with open(self.money_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f)
    
    def get_daily_message(self) -> str:
        if self.is_work_day():
            if not hasattr(self, "messages"):
                self.load_messages()
                if self.current_message_index < len(self.messages):
                    self.set_current_message_index(self.current_message_index + 1)
                    return self.messages[self.current_message_index]["message"]

    def is_work_day(self) -> bool:
        france_timezone = pytz.timezone('Europe/Paris')
        current_date = datetime.datetime.now(france_timezone)
        
        current_date_str = current_date.strftime("%Y-%m-%d")
        if current_date.weekday() < 5:
            if current_date_str not in self.holiday:
                return True
        return False

    def set_current_message_index(self, index) -> None :
        with open(self.messages_file, "r", encoding='utf-8') as f:
            data = json.load(f)
            max_index = len(data["messages"]) - 1
            data["current_index"] = index % (max_index + 1)

        with open(self.messages_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    
    def announce_salary(self) -> str:
        return f"💰 **Annonce Quotidienne** 💰\n\n Votre cagnotte a augmenté de {round(self.MONEY, 2)}€ aujourd'hui grâce à votre travail acharné.\n\n **Monnaie cumulée** : {round(self.total_money, 2)}€"

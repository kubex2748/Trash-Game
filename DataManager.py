import json
import hashlib
import os
import shutil
from datetime import datetime


class Save_Manager:
    def __init__(self, filename):
        self.filename = filename
        self.backup_filename = "data_backup.json"
        self.data = self._load_data()

    # ======== 🔐 Pomocnicze ========
    def _hash_password(self, password: str) -> str:
        if not password == '':
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            return password

    def _create_backup(self):
        """Tworzy kopię zapasową pliku przed zapisem."""
        if os.path.exists(self.filename):
            shutil.copy(self.filename, self.backup_filename)
            print("[SaveManager] Utworzono kopię zapasową.")

    def _restore_from_backup(self):
        """Przywraca dane z kopii zapasowej, jeśli główny plik jest uszkodzony."""
        if os.path.exists(self.backup_filename):
            print("[SaveManager] Przywracam dane z kopii zapasowej...")
            shutil.copy(self.backup_filename, self.filename)
            with open(self.filename, "r") as f:
                return json.load(f)
        print("[SaveManager] Brak kopii zapasowej — tworzę nowy plik.")
        return {"players": {}}

    def _load_data(self):
        """Wczytuje dane z pliku lub tworzy nowy słownik."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("[SaveManager] Uszkodzony plik save.json!")
                    return self._restore_from_backup()
        return {"players": {}}

    def _save_data(self):
        """Zapisuje dane do pliku (z kopią zapasową)."""
        self._create_backup()
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)
        print("[SaveManager] Dane zapisane pomyślnie.")

    # ======== Gracze ========
    def add_player(self, nick: str, password: str):
        """Dodaje nowego gracza, jeśli jeszcze nie istnieje."""
        if nick in self.data["players"]:
            print(f"[SaveManager] Gracz '{nick}' już istnieje.")
            return False
        self.data["players"][nick] = {
            "password": self._hash_password(password),
            "score": 0,
            "level": 1,
            "killed_boss": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None
        }
        self._save_data()
        print(f"[SaveManager] Utworzono gracza: {nick}")
        return True

    def login(self, nick: str, password: str):
        """Sprawdza dane logowania gracza."""
        player = self.data["players"].get(nick)
        if not player:
            print("[SaveManager] Nie znaleziono gracza.")
            return False
        if player["password"] == self._hash_password(password):
            player["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_data()
            print(f"[SaveManager] Zalogowano jako {nick}.")
            return True
        else:
            print("[SaveManager] Błędne hasło.")
            return False

    def update_score(self, nick: str, score: int):
        """Aktualizuje wynik gracza."""
        if nick not in self.data["players"]:
            print("[SaveManager] Nie znaleziono gracza.")
            return False
        self.data["players"][nick]["score"] = score
        self._save_data()
        print(f"[SaveManager] Zaktualizowano wynik {nick} na {score}.")
        return True

    def update_level(self, nick: str, level: int):
        """Aktualizuje poziom gracza."""
        if nick not in self.data["players"]:
            print("[SaveManager] Nie znaleziono gracza.")
            return False
        self.data["players"][nick]["level"] = level
        self._save_data()
        print(f"[SaveManager] Zaktualizowano poziom {nick} na {level}.")
        return True

    def get_value(self, nick: str, key: str):
        """Zwraca wartość z danych gracza (np. score, level, password)."""
        players = self.data.get("players", {})
        player = players.get(nick)
        if player is not None and key in player:
            return player[key]
        else:
            print(f"⚠️ Nie znaleziono klucza '{key}' lub gracza '{nick}'")
            return None

    def get_player(self, nick: str):
        """Zwraca dane gracza jako dict lub None."""
        return self.data["players"].get(nick)

    def list_players(self):
        """Zwraca listę wszystkich nicków."""
        return list(self.data["players"].keys())

    def remove_player(self, nick: str):
        """Usuwa gracza o podanym nicku z danych i zapisuje zmiany."""
        if nick in self.data["players"]:
            del self.data["players"][nick]
            self._save_data()
            print(f"Gracz '{nick}' został usunięty.")
        else:
            print(f"Gracz '{nick}' nie istnieje.")

    def reset_stats(self, nick: str):
        """Resetuje statystyki gracza do wartości początkowych."""
        player = self.data["players"].get(nick)

        if not player:
            print(f"⚠️ Gracz '{nick}' nie istnieje — nie mogę zresetować statystyk.")
            return

        # tu ustawiasz co chcesz wyzerować:
        player["score"] = 0
        player["level"] = 1
        player["killed_boss"] = 0

        # (opcjonalnie) możesz dodać nową datę "reset_at"
        from datetime import datetime
        player["reset_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # zapisz zmiany
        self._save_data()

        print(f"✅ Statystyki gracza '{nick}' zostały zresetowane.")

    def reset_all_stats(self):
        """Resetuje statystyki wszystkich graczy."""
        for nick in self.data["players"]:
            self.reset_stats(nick)
        print("✅ Statystyki wszystkich graczy zostały zresetowane.")


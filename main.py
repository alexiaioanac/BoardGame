import tkinter as tk
import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.tile_index = 0
        self.radius = 12
        # Offset ca să nu se suprapună perfect pionii pe aceeași căsuță
        self.offset_x = random.randint(-15, 15)
        self.offset_y = random.randint(-15, 15)

class BoardGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BoardGame")
        
        # 1. Interfața principală
        self.info_label = tk.Label(root, text="Board Game", font=("Arial", 14, "bold"))
        self.info_label.pack(pady=10)
        
        # Canvas-ul este "planșa" pe care vom desena căsuțele și pionii
        self.canvas = tk.Canvas(root, width=700, height=450, bg="#ffc7e9")
        self.canvas.pack()
        
        self.roll_btn = tk.Button(root, text="Roll the dice", font=("Arial", 14), command=self.roll_dice)
        self.roll_btn.pack(pady=15)
        
        # 2. Datele jocului
        self.tiles = []
        self.setup_board()
        
        self.players = [
            Player("First player", "pink"),
            Player("Second player", "purple")
        ]
        self.current_turn = 0
        
        # 3. Desenarea inițială
        self.draw_board()
        self.draw_players()

    def setup_board(self):
        self.tiles = []
        n = 5 
        m = 7
        
        # Definim limitele matricei
        top, bottom = 0, n - 1
        left, right = 0, m - 1
        
        # Salvăm coordonatele logice (rând, coloană) în ordinea traseului
        path = []
        
        while top <= bottom and left <= right:
            # 1. Deplasare spre dreapta
            for i in range(left, right + 1):
                path.append((top, i))
            top += 1
            
            # 2. Deplasare în jos
            for i in range(top, bottom + 1):
                path.append((i, right))
            right -= 1
            
            # 3. Deplasare spre stânga
            if top <= bottom:
                for i in range(right, left - 1, -1):
                    path.append((bottom, i))
                bottom -= 1
                
            # 4. Deplasare în sus
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    path.append((i, left))
                left += 1

        tile_size = 60
        padding = 5 
        margin_x, margin_y = 150, 40 

        # Folosim o listă în loc de dicționar pentru a itera mult mai ușor
        provocari = [
            "Bea apa",
            "Pleaca acasa",
            "Adevar sau provocare",
            "Fa 5 flotari",
            "Da-mi 50 de lei",
            "Latra"
            "Întoarce-te 2 căsuțe",
            "Fă un pas de street dance",
            "Spune 3 limbaje de programare în 3 secunde. Dacă nu, pedeapsă",
            "Mimează un profesor de la facultate",
            "Alege pe cineva care să facă 5 genuflexiuni",
            "Regula degetului mare: ultimul cu degetul pe masă execută o pedeapsă",
            "Noroc! Dă cu zarul încă o dată",
            "Stai într-un picior până îți vine rândul",
            "Imită sunetul de eroare de la Windows",
            "Fă o rimă cu numele jucătorului din dreapta",
            "Schimbă locul pe tablă cu jucătorul de pe ultimul loc",
            "Cântă refrenul melodiei preferate",
            "Adevăr: Care e ultima ta căutare pe telefon?",
            "Nu ai voie să folosești litera 'A' timp de un minut",
            "Fă o mișcare de popping (robot) de 10 secunde",
            "Vorbește cu accent ardelenesc până la tura următoare",
            "Lasă jucătorul din stânga să dea un mesaj de pe telefonul tău",
            "Toate fetele execută o pedeapsă",
            "Toți băieții execută o pedeapsă",
            "Povestește cea mai penibilă întâmplare de anul ăsta",
            "Mimează un animal la alegerea adversarului",
            "Stai nemișcat ca o statuie până la următoarea tură",
            "Fă-i un compliment jucătorului din stânga",
            "Adevăr: Ce notă crezi că iei la licență?",
            "Ești imun! Scapi de următoarea pedeapsă",
            "Stai cu ochii închiși până îți vine rândul",
            "Ghinion, du-te înapoi 4 căsuțe!"
        ]
        
        # Generăm căsuțele
        for index, (row, col) in enumerate(path):
            pixel_x = margin_x + col * (tile_size + padding)
            pixel_y = margin_y + row * (tile_size + padding)
            
            # Folosim modulo (%) ca să repetăm provocările când lista se termină
            # Alternativ, pentru provocări complet randomizate, poți folosi: random.choice(provocari)
            provocare_curenta = provocari[index % len(provocari)]
            
            self.tiles.append({
                "x": pixel_x,
                "y": pixel_y,
                "text": f"Provocare: {provocare_curenta}" if index < len(path) - 1 else "FINISH în centru!"
            })

        
        

    def get_tile_center(self, index):
        # Calculează centrul unei căsuțe pentru a pune pionul acolo
        tile = self.tiles[index]
        return tile["x"] + 30, tile["y"] + 30

    def draw_board(self):
        # Desenează căsuțele o singură dată
        for i, tile in enumerate(self.tiles):
            # Culoare specială pentru Start și Finish
            bg_color = "#fa148f" if i == 0 else "#fc228f" if i == len(self.tiles)-1 else "#fc6fac"
            
            self.canvas.create_rectangle(
                tile["x"], tile["y"], tile["x"] + 60, tile["y"] + 60, 
                fill=bg_color, outline="black"
            )
            # Numărul căsuței în colț
            self.canvas.create_text(tile["x"] + 15, tile["y"] + 15, text=str(i))

    def draw_players(self):
        # Ștergem pionii vechi de pe ecran înainte să îi desenăm în noile poziții
        self.canvas.delete("pioni")
        
        for p in self.players:
            cx, cy = self.get_tile_center(p.tile_index)
            # Adăugăm offset-ul ca să stea dispersați în căsuță
            px, py = cx + p.offset_x, cy + p.offset_y
            
            # Desenăm cercul pionului și îi punem eticheta "pioni" ca să îl putem șterge tura viitoare
            self.canvas.create_oval(
                px - p.radius, py - p.radius, px + p.radius, py + p.radius, 
                fill=p.color, outline="black", tags="pioni"
            )

    def roll_dice(self):
        # Logica declanșată de buton
        p = self.players[self.current_turn]
        dice = random.randint(1, 6)
        
        # Mutăm jucătorul
        p.tile_index += dice
        if p.tile_index >= len(self.tiles) - 1:
            p.tile_index = len(self.tiles) - 1
            provocare = "AI CÂȘTIGAT!"
        else:
            provocare = self.tiles[p.tile_index]["text"]
            
        # Actualizăm textul de pe ecran
        self.info_label.config(text=f"{p.name} a dat {dice}.\n{provocare}")
        
        # Redesenăm pionii în noile poziții
        self.draw_players()
        
        # Schimbăm tura
        self.current_turn = (self.current_turn + 1) % len(self.players)

# Punctul de intrare în aplicație
if __name__ == "__main__":
    root = tk.Tk()
    app = BoardGameApp(root)
    root.mainloop()
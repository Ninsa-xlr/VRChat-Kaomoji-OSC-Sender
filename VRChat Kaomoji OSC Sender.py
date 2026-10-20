import tkinter as tk
from tkinter import ttk, messagebox
import traceback

try:
    from pythonosc import udp_client
    OSC_AVAILABLE = True
except ImportError:
    OSC_AVAILABLE = False

KAOMOJI_DATA = {
    "Cute / Classic": [
        "(,,>﹏<,,)", "(,,> ᴗ <,,)", "(,,>ω<,,)", "(,,>///<,,)", "(,,•﹏•,,)",
        "(｡>﹏<｡)", "(｡•́‿•̀｡)", "(｡･ω･｡)", "(｡♥‿♥｡)", "(｡•̀ᴗ-)✧",
        "(๑>ᴗ<๑)", "(๑˃ᴗ˂)ﻭ", "(๑•̀ㅂ•́)و✧", "(๑´ڡ`๑)", "(๑´ㅂ`๑)",
        "(๑´ლ`๑)", "(๑>◡<๑)", "(๑˘︶˘๑)", "(๑˃̵ᴗ˂̵)", "(≧◡≦)",
        "(≧▽≦)", "(≧ω≦)", "(｡˃ ᵕ ˂ )ﾉﾞ", "(づ｡◕‿‿◕｡)づ", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
        "(✿◠‿◠)", "(◕‿◕✿)", "(◕ᴗ◕✿)", "(◕‿◕)", "(｡･∀･)ﾉﾞ",
        "( ´ ▽ ` )ﾉ", "(＾▽＾)", "(＾ω＾)", "(⌒▽⌒)☆", "٩(｡•́‿•̀｡)۶",
        "(ﾉ´ヮ`)ﾉ*: ･ﾟ"
    ],
    "Happy / Excited": [
        "ヾ(＾∇＾)", "ヾ(＠⌒ー⌒＠)ノ", "ヾ(≧▽≦*)o", "ヽ(o＾▽＾o)ノ", "ヽ(>∀<☆)ノ",
        "٩(◕‿◕｡)۶", "٩(๑❛ᴗ❛๑)۶", "٩(ˊᗜˋ*)و", "٩(｡•̀ᴗ-)و ̑̑", "＼(＾▽＾)／",
        "＼(≧▽≦)／", "＼(￣▽￣)／", "ヽ(*・ω・)ﾉ", "ヽ(＾Д＾)ﾉ", "ヽ(♡‿♡)ノ",
        "(ﾉ´ з `)ノ", "(ﾉ≧∀≦)ﾉ", "(☆▽☆)", "(★ω★)/", "(˶ᵔ ᵕ ᵔ˶)",
        "(˶˃ ᵕ ˂˶)", "(ˊᗜˋ*)", "(ﾉ>ω<)ﾉ", "(ง ื▿ ื)ว", "(ง •̀_•́)ง",
        "(☞ﾟヮﾟ)☞", "☜(ﾟヮﾟ☜)", "♪(๑ᴖ◡ᴖ๑)♪"
    ],
    "Shy / Blushing": [
        "(⁄ ⁄•⁄ω⁄•⁄ ⁄)", "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)", "(*/ω＼*)", "(〃▽〃)", "(〃ω〃)",
        "(〃￣ω￣〃ゞ", "(//ω//)", "(//▽//)", "(//ᴗ//)", "(⁄˘⁄ ⁄ ω⁄ ⁄ ˘⁄)",
        "(๑////๑)", "(๑´•.̫ • `๑)", "(〃ﾉωﾉ)", "(つω`｡)", "(๑•́ ₃ •̀๑)",
        "(//́Д/̀/)", "(⁄ ⁄>⁄ᗜ⁄<⁄ ⁄)", "(ᵔ////ᵔ)", "(♡ >ω< ♡)"
    ],
    "Pouting / Pleading": [
        "(｡•́︿•̀｡)", "(｡•́ - •̀｡)", "(｡╯︵╰｡)", "( ˘︹˘ )", "(｡•́︿•̀｡)♡",
        "(｡•́︿•̀｡)👉👈", "( •́દ•̩̥̀ )", "(╥﹏╥)", "(つ﹏<。)", "(っ˘╭╮˘̩)っ",
        "(ᗒᗣᗕ)՞", "(ᵕ̣̣̣̣̣̣﹏ᵕ̣̣̣̣̣̣)", "( •́ ̯•̀ )", "(づT_T)づ", "(ó﹏ò｡)",
        "(ಥ﹏ಥ)", "(ノ_<。)", "(っ- ‸ - ς)", "(╥_╥)", "(；ω；)"
    ],
    "Sad / Crying": [
        "(T_T)", "(;_;)", "(ಥ_ಥ)", "(；へ；)", "(ノ_<。)",
        "(っ˘╭╮˘̩)っ", "(இ﹏இ`｡)", "(つ﹏⊂)", "(╯︵╰,)", "(っ◞‸◟ c)",
        "(ಥДಥ)", "( ; ω ; )", "(ノД`)・゜・。", "(இдஇ; )", "(｡•́︿•̀｡)｡ﾟ",
        "(Ｔ▽Ｔ)", "(つд⊂)", "(｡ﾉω＼｡)", "(╥﹏╥)"
    ],
    "Love / Hearts": [
        "(♡˙︶˙♡)", "(♡ >ω< ♡)", "(♡°▽°♡)", "(♡μ_μ)", "(♥ω♥*)",
        "(｡♥‿♥｡)", "(ღ˘⌣˘ღ)", "(灬♥ω♥灬)", "( ˘ ³˘)♥", "(っ˘з(˘⌣˘ )",
        "(づ￣ ³￣)づ", "(♡ˊ͈ ꒳ ˋ͈)", "(♡°ω°♡)", "(๑♡⌓♡๑)", "(๑♡3♡๑)",
        "(｡・//ε//・｡)", "(๑˘ ³˘๑)♥", "(♡´艸`)", "(♡´▽`♡)", "(づ￣ ³￣)づ♡",
        "(♡˘͈ ᵕ ˘͈♡)"
    ],
    "Hugs / Comfort": [
        "(づ｡◕‿‿◕｡)づ", "(つ≧▽≦)つ", "(づ￣ ³￣)づ", "(っ´▽｀)っ", "(つ✧ω✧)つ",
        "(づ ◕‿◕ )づ", "(っ´ω`)ﾉ(╥ω╥)", "(つ . •́ _ʖ •̀ .)つ", "(づ◡﹏◡)づ", "(っ´▽｀)っ♡",
        "(つ≧▽≦)つ♡", "(つ´∀｀)つ", "(つ´ω`)つ", "(っ・ω・）っ", "(づ｡◕‿‿◕｡)づ♡",
        "(っ*´∀｀*)っ", "(つω`｡)っ", "(づ๑•ᴗ•๑)づ♡", "(つ≧▽≦)つ ぎゅっ"
    ],
    "Angry / Annoyed": [
        "(＃`Д´)", "( ` ω ´ )", "(ง'̀-'́)ง", "(╬ Ò﹏Ó)", "(ノಠ益ಠ)ノ彡┻━┻",
        "(╯°□°）╯︵ ┻━┻", "(ಠ益ಠ)", "(¬_¬)", "(눈_눈)", "(≖_≖ )",
        "(＃＞＜)", "(>_<)", "(｡•̀︿•́｡)", "(╬ಠ益ಠ)", "(ಠ⌣ಠ)",
        "(¬､¬)", "( •̀ω•́ )σ", "(ง •̀_•́)ง", "(＃￣0￣)", "(⇀‸↼‶)",
        "(≧ヘ≦ )", "(ಠ_ಠ)", "(¬_¬\")", "(＃｀д´)ﾉ"
    ],
    "Surprised": [
        "(⊙_⊙)", "(°ロ°) !", "(゜ロ゜)", "(⊙_⊙;)", "(๑°ㅁ°๑)‼",
        "(☉｡☉)!", "(°△°|||)", "(〇_o)/", "(⊙.☉)7", "Σ(°△°|||)︴",
        "Σ(っ°Д°;)っ", "(・o・)", "(°д°)", "(；￣Д￣）", "(๑°o°๑)",
        "(ʘᗩʘ')", "(ﾟДﾟ;)", "(」°ロ°)」", "(⊙﹏⊙)", "(◉_◉)",
        "(๑•ૅㅁ•๑)", "(°□°；)", "(；゜０゜)"
    ],
    "Confused": [
        "(・・)?", "(￣ω￣;)", "(・_・ヾ", "(゜-゜)", "(・・。)ゞ",
        "(￣～￣;)", "(ーー;)", "(•ิ_•ิ)?", "(⊙_☉)", "(◎_◎;)",
        "(・・ ) ?", "(¬､¬)", "(・・;)", "(・へ・)", "( ˘•ω•˘ )",
        "(ᵔ.ᵔ)?", "(°ヘ°)", "(＠_＠)", "(・・；)", "(•﹏•;)",
        "(￣～￣；)", "(⊙_⊙)?", "(눈‸눈)", "(。ヘ°)", "(￣ ￣|||)"
    ],
    "Sleepy / Tired": [
        "(－ω－) zzZ", "(￣o￣) zzZZzzZZ", "(＿ ＿*) Z z z", "(－_－) zzZ", "(∪｡∪)｡｡｡zzz",
        "(－.－)...zzz", "(￣ρ￣)..zzZZ", "(｡-ω-)ﾉ☆･ﾟ::ﾟ", "(｡ρω-｡)", "(つω`｡)",
        "(￣o￣) . z Z", "(。-ω-)zzz", "(ᴗ˳ᴗ)", "( ˘ω˘ )ｽﾔｧ", "(¦3[▓▓]",
        "(っ- ‸ - ς)", "(／０￣)", "(¬д¬。)"
    ],
    "Laughing / Silly": [
        "(≧▽≦)", "(＾▽＾)", "(๑˃́ꇴ˂̀๑)", "(≧∇≦)/", "(ﾉ∀≦｡)ﾉ",
        "(๑˃ᴗ˂)ﻭ", "(≧ω≦)", "(￣▽￣)ノ", "(¬‿¬)", "(ಡωಡ)",
        "(ಡ艸ಡ)", "(≧艸≦)", "(๑>؂<๑)", "(ノ∀｀)", "(≧ヮ≦)",
        "(≧∇≦)", "( ＾∀＾)", "(ᗒᗨᗕ)", "(≖ᴗ≖✿)", "(☞ﾟヮﾟ)☞",
        "(ﾉ≧∀≦)ﾉ", "(≧∇≦)ﾉ", "(＾Д＾)", "(ノ＞▽＜。)ノ"
    ],
    "Smug / Mischievous": [
        "(¬‿¬)", "(￣ー￣)", "(ಡ‿ಡ)", "(ಡωಡ)", "( ͡° ͜ʖ ͡°)",
        "(¬‿¬ )", "(￣▽￣)", "(¬‿¬)✧", "( ͡~ ͜ʖ ͡°)", "(ಡ艸ಡ)",
        "(≖‿≖)", "(｡•̀ᴗ-)✧", "(￢‿￢ )", "(￣ω￣)", "(ಡᴗಡ)",
        "(ᵔ ͜ʖ ᵔ)", "(˵¬ᴗ¬˵)", "(≖ᴗ≖✿)"
    ],
    "Waving / Greetings": [
        "(｡･ω･)ﾉﾞ", "(￣▽￣)ノ", "( ´ ▽ ` )ﾉ", "ヾ(＾∇＾)", "(｡•̀ᴗ-)✧",
        "(ﾉ´ з `)ノ", "(・∀・)ノ", "(＾-＾)ノ", "(≧▽≦)/", "( ^_^)/~~~",
        "(・ω・)ノ", "(￣ω￣)ノ", "ヾ(・ω・*)ノ", "(=ﾟωﾟ)ﾉ", "(｡•̀ᴗ-)ﾉ",
        "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(｡･ω･｡)ﾉ♡"
    ],
    "Thanks / Please": [
        "(人´∀`)", "(人 •͈ᴗ•͈)", "(人ω<`;) ｺﾞﾒﾝﾈ", "(シ_ _)シ", "(m｡_｡)m",
        "(＞人＜;)", "(シ. .)シ", "(｡-人-｡)", "(人 •͈ᴗ•͈)✧", "(人´ω`*)♡",
        "(m´･ω･`)m", "(＞﹏＜) please", "(｡•́︿•̀｡) sorry"
    ],
    "Animals / Cats": [
        "(=^･ω･^=)", "(=^･ｪ･^=)", "(=ＴェＴ=)", "(=｀ω´=)", "(=^-ω-^=)",
        "(=^‥^=)", "(=①ω①=)", "(=ↀωↀ=)", "(=ｘェｘ=)", "(=；ェ；=)",
        "(=；ω；=)", "(ФωФ)", "(Ф∀Ф)", "(ΦωΦ)", "(ฅ^•ﻌ•^ฅ)",
        "(ฅ'ω'ฅ)", "(ฅ•ω•ฅ)", "(ฅ´ω`ฅ)", "(U・ᴥ・U)", "ʕ•ᴥ•ʔ",
        "ʕ ꈍᴥꈍʔ", "ʕง•ᴥ•ʔง", "ʕ´•ᴥ•`ʔ", "(ᵔᴥᵔ)", "(•ө•)♡", "(•ㅅ•)"
    ],
    "Determined": [
        "(ง •̀_•́)ง", "(๑•̀ㅂ•́)و✧", "(ง'̀-'́)ง", "٩(๑•̀ω•́๑)۶", "(๑•̀ㅂ•́)و",
        "( •̀ᴗ•́ )و ̑̑", "(งಠ_ಠ)ง", "(๑•̀ㅁ•́๑)✧", "( •̀ω•́ )و", "(๑•̀ᗝ•́)૭",
        "(ง •̀_•́)ง‼", "( •̀ᴗ•́ )و", "(ง •̀_•́)ง🔥", "٩(ˊᗜˋ*)و", "(๑•̀ㅁ•́๑)૭✧",
        "(ง •̀ω•́)ง"
    ],
    "Embarrassed": [
        "(・・。)ゞ", "(￣▽￣*)ゞ", "(⌒_⌒;)", "(〃￣ω￣〃ゞ", "(＠_＠;)",
        "(・・;)", "(；￣Д￣）", "(￣ω￣;)", "(•́ω•̀ ٥)", "(ᵕ—ᴗ—)",
        "(•́ ᴗ •̀)", "(；・∀・)", "(￣□￣」)", "(•﹏•;)"
    ],
    "Cool / Confident": [
        "(⌐■_■)", "( •_•)>⌐■-■", "(⌐▨_▨)", "(￣ー￣)ゞ", "( •̀ᴗ•́ )و",
        "(｡•̀ᴗ-)✧", "(ง ื▿ ื)ว", "(•̀ᴗ•́)و ̑̑", "(๑•̀ㅂ•́)و✧", "(￣^￣)ゞ",
        "(｀・ω・´)", "( •̀ω•́ )✧", "(⌐■_■)ノ♪"
    ],
    "Gestures / Actions": [
        "(☞ﾟヮﾟ)☞", "☜(ﾟヮﾟ☜)", "(っ•̀ω•́)っ", "(づ｡◕‿‿◕｡)づ", "(σ≧▽≦)σ",
        "(☞ ͡° ͜ʖ ͡°)☞", "(〜￣▽￣)〜", "┬─┬ノ( º _ ºノ)", "(ノಥ,_｣ಥ)ノ彡┻━┻", "(╯°□°）╯︵ ┻━┻",
        "(._.)ヾ( )", "(づ￣ ³￣)づ", "(っ´▽｀)っ", "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ", "(っ'-')╮=͟͟͞͞♡",
        "(ﾉ≧∀≦)ﾉ ‥…━━━★"
    ],
    "Simple Text Faces": [
        ":)", "^_^", "^-^", "^.^", ":D", "xD", "XD", ":3",
        ";-)", ";)", ":P", ":p", ":(", ":'(", "T_T", ";-;",
        "._.", "-_-", "o_O", "O_o", ">_<", ">w<", "<3", "</3",
        ":')", ":]", ":v", ":/", "(¬_¬)", "(._.)", "(o_o)", "(o.O)",
        "(O.O)", "(0_0)", "(>_<)", "(^o^)", "(^.^)","(*_*)", "(@_@)", "(u_u)",
        "(=_=)", "(T.T)", "(Q_Q)", "(>w<)", "(UwU)", "(OwO)"
    ],
    "Extra Cute": [
        "(,,>﹏<,,)♡", "(｡>﹏<｡)♡", "(๑>ᴗ<๑)♡", "(⁄ ⁄•⁄ω⁄•⁄ ⁄)♡", "(づ｡◕‿‿◕｡)づ♡",
        "(｡♥‿♥｡)ノ", "(っ˘з(˘⌣˘ )♡", "(ฅ´ω`ฅ)♡", "(˶ᵔ ᵕ ᵔ˶)♡", "(๑˃̵ᴗ˂̵)و ♡",
        "(｡･ω･｡)ﾉ♡", "(｡•̀ᴗ-)✧♡", "(,,> ᴗ <,,)♡", "(,,•́ . •̀,,)♡", "(,,>ω<,,)♡",
        "(つ≧▽≦)つ♡", "(｡•́︿•̀｡)♡", "(っ´▽｀)っ♡", "(♡˘͈ ᵕ ˘͈♡)", "(づ˶•༝•˶)づ♡"
    ]
}

BG_DARK = "#181524"
PANEL_BG = "#221d33"
TEXT_LIGHT = "#e2def0"
ACCENT_LILA = "#a277ff"
BTN_BG = "#2f2847"

class VRChatKaomojiSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRChat Kaomoji OSC")
        self.root.geometry("800x600")
        self.root.minsize(650, 500)
        self.root.configure(bg=BG_DARK)

        self.setup_styles()

        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.IntVar(value=9000)
        self.client = None
        self.update_osc_client()

        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure(".", background=BG_DARK, foreground=TEXT_LIGHT)
        style.configure("TFrame", background=BG_DARK)
        style.configure("TLabelframe", background=BG_DARK, foreground=ACCENT_LILA)
        style.configure("TLabelframe.Label", background=BG_DARK, foreground=ACCENT_LILA, font=("Segoe UI", 10, "bold"))
        
        style.configure("TButton", background=BTN_BG, foreground=TEXT_LIGHT, borderwidth=0, focusthickness=0, font=("Segoe UI", 10))
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        style.configure("Status.TLabel", background=PANEL_BG, foreground=ACCENT_LILA, font=("Segoe UI", 10, "italic"))
        style.configure("TEntry", fieldbackground=PANEL_BG, foreground=TEXT_LIGHT)
        style.configure("TCombobox", fieldbackground=PANEL_BG, background=PANEL_BG, foreground=TEXT_LIGHT)

    def update_osc_client(self):
        if not OSC_AVAILABLE:
            return
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get())
            self.client = udp_client.SimpleUDPClient(ip, port)
        except Exception as e:
            messagebox.showerror("OSC Error", f"Ungültige IP oder Port: {e}")

    def send_kaomoji(self, text):
        if not OSC_AVAILABLE:
            messagebox.showerror("Bibliothek fehlt", "Das Paket 'python-osc' ist nicht installiert.\nFühre aus: pip install python-osc")
            return
        if not self.client:
            self.update_osc_client()
        try:
            self.client.send_message("/chatbox/input", [text, True])
            
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
            except Exception:
                pass
            
            self.status_var.set(f"Gesendet & Kopiert: {text}")
        except Exception as e:
            self.status_var.set(f"Fehler beim Senden: {e}")

    def create_widgets(self):
        top_container = ttk.Frame(self.root)
        top_container.pack(fill="x", padx=15, pady=15)

       
        conn_frame = ttk.LabelFrame(top_container, text="OSC Verbindung", padding=10)
        conn_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(conn_frame, text="IP:").pack(side="left", padx=(0, 5))
        ttk.Entry(conn_frame, textvariable=self.ip_var, width=12).pack(side="left", padx=(0, 8))

        ttk.Label(conn_frame, text="Port:").pack(side="left", padx=(0, 5))
        ttk.Entry(conn_frame, textvariable=self.port_var, width=5).pack(side="left", padx=(0, 8))

        ttk.Button(conn_frame, text="Anwenden", command=self.update_osc_client).pack(side="left")

     
        search_frame = ttk.LabelFrame(top_container, text="Live-Suche", padding=10)
        search_frame.pack(side="right", fill="both", expand=True)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill="x", expand=True)

      
        catalog_container = ttk.LabelFrame(self.root, text="Kaomoji Katalog Menü", padding=12)
        catalog_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        
        menu_row = ttk.Frame(catalog_container)
        menu_row.pack(fill="x", padx=5, pady=(0, 10))

        ttk.Label(menu_row, text="Katalog auswählen: ", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        
        self.catalog_var = tk.StringVar(value=list(KAOMOJI_DATA.keys())[0])
        self.catalog_menu = ttk.Combobox(
            menu_row, 
            textvariable=self.catalog_var, 
            values=list(KAOMOJI_DATA.keys()), 
            state="readonly", 
            width=28
        )
        self.catalog_menu.pack(side="left")
        self.catalog_menu.bind("<<ComboboxSelected>>", self.on_catalog_selected)

        
        content_frame = ttk.Frame(catalog_container)
        content_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(content_frame, highlightthickness=0, bg=BG_DARK)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding=5)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.populate_catalog_buttons(self.catalog_var.get())

      
        status_frame = tk.Frame(self.root, bg=PANEL_BG, padx=10, height=35)
        status_frame.pack(fill="x", side="bottom", padx=15, pady=(0, 15))
        status_frame.pack_propagate(False)

        status_text = "Bereit! Klicke auf ein Kaomoji, um es an VRChat zu senden & zu kopieren." if OSC_AVAILABLE else "WARNUNG: 'python-osc' fehlt! Führe aus: pip install python-osc"
        self.status_var = tk.StringVar(value=status_text)
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel")
        status_label.pack(side="left", fill="both", expand=True, pady=5)

    def on_catalog_selected(self, event):
        if self.search_var.get():
            self.search_var.set("")
        selected_cat = self.catalog_var.get()
        self.populate_catalog_buttons(selected_cat)

    def populate_catalog_buttons(self, category_name):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        kaomojis = KAOMOJI_DATA.get(category_name, [])
        row, col = 0, 0
        for k in kaomojis:
            btn = ttk.Button(
                self.scrollable_frame, 
                text=k, 
                width=24, 
                command=lambda val=k: self.send_kaomoji(val)
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            col += 1
            if col > 3:
                col = 0
                row += 1

    def filter_search(self, *args):
        query = self.search_var.get().strip().lower()
        if not query:
            self.populate_catalog_buttons(self.catalog_var.get())
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        matches = []
        for cat, kaomojis in KAOMOJI_DATA.items():
            for k in kaomojis:
                if query in k.lower() or query in cat.lower():
                    matches.append((k, cat))

        if not matches:
            lbl = ttk.Label(self.scrollable_frame, text="Keine passenden Kaomojis gefunden.", font=("Segoe UI", 11))
            lbl.grid(row=0, column=0, padx=10, pady=10)
            return

        row, col = 0, 0
        for k, cat in matches:
            btn = ttk.Button(
                self.scrollable_frame, 
                text=f"{k}  ({cat})", 
                width=30, 
                command=lambda val=k: self.send_kaomoji(val)
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            col += 1
            if col > 2:
                col = 0
                row += 1

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VRChatKaomojiSenderApp(root)
        root.mainloop()
    except Exception as e:
        err_details = traceback.format_exc()
        try:
            err_root = tk.Tk()
            err_root.withdraw()
            messagebox.showerror("Startup-Fehler", f"Die Anwendung konnte nicht gestartet werden:\n\n{err_details}")
        except Exception:
            print(err_details)
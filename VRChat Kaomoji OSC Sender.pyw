import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
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

TEXT_LIGHT = "#e2def0"

class VRChatKaomojiSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kaomoji for VRChat")
        self.root.geometry("960x700")
        self.root.minsize(720, 540)

        self.hue_var = tk.IntVar(value=260)
        self.set_menu_palette(self.hue_var.get())
        self.root.configure(bg=self.bg_color)
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

        self.style = style
        self.apply_menu_palette()

    def set_menu_palette(self, hue):
        hue_fraction = (int(hue) % 360) / 360.0

        def color(saturation, value):
            channels = colorsys.hsv_to_rgb(hue_fraction, saturation, value)
            return "#{:02x}{:02x}{:02x}".format(*(int(channel * 255) for channel in channels))

        self.bg_color = color(0.22, 0.10)
        self.panel_color = color(0.34, 0.16)
        self.button_color = color(0.40, 0.24)
        self.accent_color = color(0.56, 1.0)
        self.muted_color = color(0.16, 0.72)

    def apply_menu_palette(self):
        style = self.style
        style.configure(".", background=self.bg_color, foreground=TEXT_LIGHT)
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabelframe", background=self.bg_color, foreground=self.accent_color, bordercolor=self.button_color)
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.accent_color, font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=self.bg_color, foreground=TEXT_LIGHT, font=("Segoe UI", 10))
        style.configure("Subtitle.TLabel", background=self.bg_color, foreground=self.muted_color, font=("Segoe UI", 10))
        style.configure("TButton", background=self.button_color, foreground=TEXT_LIGHT, borderwidth=0, focusthickness=0, padding=(10, 7), font=("Segoe UI", 10))
        style.map("TButton", background=[("active", self.accent_color), ("pressed", self.accent_color)], foreground=[("active", self.bg_color)])
        style.configure("TEntry", fieldbackground=self.panel_color, foreground=TEXT_LIGHT, insertcolor=TEXT_LIGHT, padding=7)
        style.configure("TCombobox", fieldbackground=self.panel_color, background=self.panel_color, foreground=TEXT_LIGHT, padding=5)
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.button_color, foreground=TEXT_LIGHT, padding=(18, 9))
        style.map("TNotebook.Tab", background=[("selected", self.panel_color), ("active", self.accent_color)], foreground=[("selected", self.accent_color), ("active", self.bg_color)])
        style.configure("Status.TLabel", background=self.panel_color, foreground=self.accent_color, font=("Segoe UI", 10))
        style.configure("Vertical.TScrollbar", background=self.button_color, troughcolor=self.bg_color, arrowcolor=TEXT_LIGHT)

    def update_menu_hue(self, hue):
        hue = max(0, min(359, int(hue)))
        self.hue_var.set(hue)
        self.set_menu_palette(hue)
        self.apply_menu_palette()
        self.root.configure(bg=self.bg_color)

        if hasattr(self, "title_label"):
            self.canvas.configure(bg=self.bg_color)
            self.hue_slider.configure(bg=self.bg_color)
            self.status_frame.configure(bg=self.panel_color)
            self.title_label.configure(foreground=self.accent_color)
            self.hue_value_label.configure(text="{}°".format(hue))
            self.hue_swatch.configure(bg=self.accent_color)
            self.update_hue_marker()

    def draw_hue_slider(self, event=None):
        width = max(self.hue_slider.winfo_width(), 2)
        height = self.hue_slider.winfo_height()
        self.hue_slider.delete("all")

        for x in range(width):
            hue = x / float(width - 1)
            red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = "#{:02x}{:02x}{:02x}".format(int(red * 255), int(green * 255), int(blue * 255))
            self.hue_slider.create_line(x, 2, x, height - 2, fill=color, tags="spectrum")

        self.hue_slider.create_line(0, 0, 0, height, fill="#17131f", width=4, tags="marker_outline")
        self.hue_slider.create_line(0, 0, 0, height, fill="#ffffff", width=2, tags="marker")
        self.update_hue_marker()

    def update_hue_marker(self):
        if not hasattr(self, "hue_slider") or not self.hue_slider.find_withtag("marker"):
            return
        width = max(self.hue_slider.winfo_width(), 2)
        height = self.hue_slider.winfo_height()
        marker_x = round(self.hue_var.get() / 359.0 * (width - 1))
        for tag in ("marker_outline", "marker"):
            self.hue_slider.coords(tag, marker_x, 0, marker_x, height)

    def on_hue_slider_changed(self, event):
        width = max(self.hue_slider.winfo_width(), 2)
        x = max(0, min(width - 1, event.x))
        hue = round(x / float(width - 1) * 359)
        self.update_menu_hue(hue)

    def update_osc_client(self):
        if not OSC_AVAILABLE:
            return
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get())
            if not ip or not 1 <= port <= 65535:
                raise ValueError("Enter an IP address and a port from 1 to 65535.")
            self.client = udp_client.SimpleUDPClient(ip, port)
            if hasattr(self, "status_var"):
                self.status_var.set(f"OSC destination set to {ip}:{port}")
        except Exception as error:
            self.client = None
            messagebox.showerror("OSC Setup Error", f"Invalid IP address or port: {error}")

    def send_kaomoji(self, text):
        if not OSC_AVAILABLE:
            messagebox.showerror("Missing Library", "The 'python-osc' package is not installed.\nInstall it with: pip install python-osc")
            return
        if not self.client:
            self.update_osc_client()
        if not self.client:
            return
        try:
            self.client.send_message("/chatbox/input", [text, True])
            self.status_var.set(f"Sent to VRChat: {text}")
        except Exception as error:
            self.status_var.set(f"Send failed: {error}")

    def create_widgets(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=22, pady=(20, 14))
        self.title_label = ttk.Label(header, text="Kaomoji for VRChat", font=("Segoe UI", 20, "bold"), foreground=self.accent_color)
        self.title_label.pack(anchor="w")
        ttk.Label(header, text="Choose a face to send it straight to your VRChat chatbox.", style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=22, pady=(0, 12))
        self.library_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.library_tab, text="Kaomoji")
        self.notebook.add(self.settings_tab, text="Settings")

        search_frame = ttk.LabelFrame(self.library_tab, text="Search kaomojis", padding=12)
        search_frame.pack(fill="x", padx=14, pady=(14, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill="x", expand=True, ipady=2)

        catalog_container = ttk.LabelFrame(self.library_tab, text="Kaomoji Library", padding=14)
        catalog_container.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        menu_row = ttk.Frame(catalog_container)
        menu_row.pack(fill="x", padx=2, pady=(0, 12))

        ttk.Label(menu_row, text="Category", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 10))

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

        self.canvas = tk.Canvas(content_frame, highlightthickness=0, bg=self.bg_color)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding=5)
        for column in range(4):
            self.scrollable_frame.columnconfigure(column, weight=1)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfigure(self.canvas_window, width=event.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.populate_catalog_buttons(self.catalog_var.get())

        settings_content = ttk.Frame(self.settings_tab, padding=20)
        settings_content.pack(fill="x", anchor="n")
        ttk.Label(settings_content, text="Customize the menu and VRChat connection.", style="Subtitle.TLabel").pack(anchor="w", pady=(0, 14))

        appearance_frame = ttk.LabelFrame(settings_content, text="Menu Colors", padding=16)
        appearance_frame.pack(fill="x", pady=(0, 14))
        ttk.Label(appearance_frame, text="Choose a hue to recolor the entire interface.").pack(anchor="w", pady=(0, 10))

        self.hue_slider = tk.Canvas(appearance_frame, height=22, bg=self.bg_color, highlightthickness=0, cursor="hand2")
        self.hue_slider.pack(fill="x", expand=True, pady=(0, 8))
        self.hue_slider.bind("<Configure>", self.draw_hue_slider)
        self.hue_slider.bind("<Button-1>", self.on_hue_slider_changed)
        self.hue_slider.bind("<B1-Motion>", self.on_hue_slider_changed)

        hue_info = ttk.Frame(appearance_frame)
        hue_info.pack(fill="x")
        self.hue_swatch = tk.Frame(hue_info, width=16, height=16, bg=self.accent_color)
        self.hue_swatch.pack(side="left", padx=(2, 8))
        self.hue_swatch.pack_propagate(False)
        ttk.Label(hue_info, text="Current menu color").pack(side="left")
        self.hue_value_label = ttk.Label(hue_info, text="260°", style="Subtitle.TLabel")
        self.hue_value_label.pack(side="right")

        conn_frame = ttk.LabelFrame(settings_content, text="OSC Destination", padding=16)
        conn_frame.pack(fill="x")
        ttk.Label(conn_frame, text="IP address").grid(row=0, column=0, sticky="w", padx=(0, 12))
        ttk.Label(conn_frame, text="Port").grid(row=0, column=1, sticky="w", padx=(0, 12))
        ttk.Entry(conn_frame, textvariable=self.ip_var, width=24).grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(4, 0))
        ttk.Entry(conn_frame, textvariable=self.port_var, width=10).grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=(4, 0))
        ttk.Button(conn_frame, text="Apply", command=self.update_osc_client).grid(row=1, column=2, sticky="w", pady=(4, 0))
        conn_frame.columnconfigure(0, weight=1)
        conn_frame.columnconfigure(1, weight=1)

        self.status_frame = tk.Frame(self.root, bg=self.panel_color, padx=12, height=40)
        self.status_frame.pack(fill="x", side="bottom", padx=22, pady=(0, 18))
        self.status_frame.pack_propagate(False)

        status_text = "Ready — click any kaomoji to send it to VRChat." if OSC_AVAILABLE else "Warning: 'python-osc' is missing. Install it with: pip install python-osc"
        self.status_var = tk.StringVar(value=status_text)
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var, style="Status.TLabel")
        status_label.pack(side="left", fill="both", expand=True, pady=7)
        self.update_menu_hue(self.hue_var.get())

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
            lbl = ttk.Label(self.scrollable_frame, text="No matching kaomojis found.", font=("Segoe UI", 11))
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
            messagebox.showerror("Startup Error", f"The application could not start:\n\n{err_details}")
        except Exception:
            print(err_details)

"""
Catálogo Completo dos 15 Verbos Mais Usados em Espanhol + 3 Modelos Regulares
Gerador de Tiras Térmicas (Phomemo M02 - 384px)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

WIDTH = 384

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(size: int, bold: bool = False):
    try:
        font_path = FONT_BOLD if bold else FONT_REG
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

VERBS_DATA = {
    # 1. SER
    "ser": {
        "verb": "SER",
        "pt": "SER",
        "icon": "star",
        "present": [
            ("yo soy", "eu sou"),
            ("tú eres", "você é"),
            ("él / ella es", "ele / ela é"),
            ("nosotros somos", "nós somos"),
            ("vosotros sois", "vocês são [vós sois]"),
            ("ellos son", "eles são")
        ],
        "past": [
            ("yo fui", "eu fui"),
            ("tú fuiste", "você foi"),
            ("él / ella fue", "ele / ela foi"),
            ("nosotros fuimos", "nós fomos"),
            ("vosotros fuisteis", "vocês foram [vós fostes]"),
            ("ellos fueron", "eles foram")
        ],
        "future": [
            ("yo seré", "eu serei"),
            ("tú serás", "você será"),
            ("él / ella será", "ele / ela será"),
            ("nosotros seremos", "nós seremos"),
            ("vosotros seréis", "vocês serão [vós sereis]"),
            ("ellos serán", "eles serão")
        ],
        "examples": [
            ("PRES", "Yo soy brasileño.", "Eu sou brasileiro."),
            ("PAS",  "Ayer fue un gran día.", "Ontem foi um grande dia."),
            ("FUT",  "Mañana será mejor.", "Amanhã será melhor.")
        ]
    },
    # 2. ESTAR
    "estar": {
        "verb": "ESTAR",
        "pt": "ESTAR",
        "icon": "pin",
        "present": [
            ("yo estoy", "eu estou"),
            ("tú estás", "você está"),
            ("él / ella está", "ele / ela está"),
            ("nosotros estamos", "nós estamos"),
            ("vosotros estáis", "vocês estão [vós estais]"),
            ("ellos están", "eles estão")
        ],
        "past": [
            ("yo estuve", "eu estive"),
            ("tú estuviste", "você esteve"),
            ("él / ella estuvo", "ele / ela esteve"),
            ("nosotros estuvimos", "nós estivemos"),
            ("vosotros estuvisteis", "vocês estiveram"),
            ("ellos estuvieron", "eles estiveram")
        ],
        "future": [
            ("yo estaré", "eu estarei"),
            ("tú estarás", "você estará"),
            ("él / ella estará", "ele / ela estará"),
            ("nosotros estaremos", "nós estaremos"),
            ("vosotros estaréis", "vocês estarão"),
            ("ellos estarán", "eles estarão")
        ],
        "examples": [
            ("PRES", "Hoy estoy muy contento.", "Hoje estou muito contente."),
            ("PAS",  "Estuve ocupado ayer.", "Estive ocupado ontem."),
            ("FUT",  "Estaré allí a las ocho.", "Estarei lá às oito.")
        ]
    },
    # 3. TENER
    "tener": {
        "verb": "TENER",
        "pt": "TER",
        "icon": "box",
        "present": [
            ("yo tengo", "eu tenho"),
            ("tú tienes", "você tem"),
            ("él / ella tiene", "ele / ela tem"),
            ("nosotros tenemos", "nós temos"),
            ("vosotros tenéis", "vocês têm [vós tendes]"),
            ("ellos tienen", "eles têm")
        ],
        "past": [
            ("yo tuve", "eu tive"),
            ("tú tuviste", "você teve"),
            ("él / ella tuvo", "ele / ela teve"),
            ("nosotros tuvimos", "nós tivemos"),
            ("vosotros tuvisteis", "vocês tiveram"),
            ("ellos tuvieron", "eles tiveram")
        ],
        "future": [
            ("yo tendré", "eu terei"),
            ("tú tendrás", "você terá"),
            ("él / ella tendrá", "ele / ela terá"),
            ("nosotros tendremos", "nós teremos"),
            ("vosotros tendréis", "vocês terão"),
            ("ellos tendrán", "eles terão")
        ],
        "examples": [
            ("PRES", "Tengo muchas ganas de ir.", "Tenho muita vontade de ir."),
            ("PAS",  "Tuve suerte ayer.", "Tive sorte ontem."),
            ("FUT",  "Tendré tiempo el fin de semana.", "Terei tempo no fim de semana.")
        ]
    },
    # 4. HACER
    "hacer": {
        "verb": "HACER",
        "pt": "FAZER",
        "icon": "gear",
        "present": [
            ("yo hago", "eu faço"),
            ("tú haces", "você faz"),
            ("él / ella hace", "ele / ela faz"),
            ("nosotros hacemos", "nós fazemos"),
            ("vosotros hacéis", "vocês fazem"),
            ("ellos hacen", "eles fazem")
        ],
        "past": [
            ("yo hice", "eu fiz"),
            ("tú hiciste", "você fez"),
            ("él / ella hizo", "ele / ela fez"),
            ("nosotros hicimos", "nós fizemos"),
            ("vosotros hicisteis", "vocês fizeram"),
            ("ellos hicieron", "eles fizeram")
        ],
        "future": [
            ("yo haré", "eu farei"),
            ("tú harás", "você fará"),
            ("él / ella hará", "ele / ela fará"),
            ("nosotros haremos", "nós faremos"),
            ("vosotros haréis", "vocês farão"),
            ("ellos harán", "eles farão")
        ],
        "examples": [
            ("PRES", "Hago ejercicio todos los días.", "Faço exercício todo dia."),
            ("PAS",  "Hice todo lo que pude.", "Fiz tudo o que pude."),
            ("FUT",  "Mañana lo haré temprano.", "Amanhã farei cedo.")
        ]
    },
    # 5. IR
    "ir": {
        "verb": "IR",
        "pt": "IR",
        "icon": "arrow",
        "present": [
            ("yo voy", "eu vou"),
            ("tú vas", "você vai"),
            ("él / ella va", "ele / ela vai"),
            ("nosotros vamos", "nós vamos"),
            ("vosotros vais", "vocês vão [vós ides]"),
            ("ellos van", "eles vão")
        ],
        "past": [
            ("yo fui", "eu fui"),
            ("tú fuiste", "você foi"),
            ("él / ella fue", "ele / ela foi"),
            ("nosotros fuimos", "nós fomos"),
            ("vosotros fuisteis", "vocês foram"),
            ("ellos fueron", "eles foram")
        ],
        "future": [
            ("yo iré", "eu irei"),
            ("tú irás", "você irá"),
            ("él / ella irá", "ele / ela irá"),
            ("nosotros iremos", "nós iremos"),
            ("vosotros iréis", "vocês irão"),
            ("ellos irán", "eles irão")
        ],
        "examples": [
            ("PRES", "Voy al supermercado ahora.", "Vou ao supermercado agora."),
            ("PAS",  "Ayer fui al cine con amigos.", "Ontem fui ao cinema com amigos."),
            ("FUT",  "El mes próximo iré a Madrid.", "No próximo mês irei a Madri.")
        ]
    },
    # 6. PODER
    "poder": {
        "verb": "PODER",
        "pt": "PODER / CONSEGUIR",
        "icon": "check",
        "present": [
            ("yo puedo", "eu posso"),
            ("tú puedes", "você pode"),
            ("él / ella puede", "ele / ela pode"),
            ("nosotros podemos", "nós podemos"),
            ("vosotros podéis", "vocês podem"),
            ("ellos pueden", "eles podem")
        ],
        "past": [
            ("yo pude", "eu pude"),
            ("tú pudiste", "você pôde"),
            ("él / ella pudo", "ele / ela pôde"),
            ("nosotros pudimos", "nós pudemos"),
            ("vosotros pudisteis", "vocês puderam"),
            ("ellos pudieron", "eles puderam")
        ],
        "future": [
            ("yo podré", "eu poderei"),
            ("tú podrás", "você poderá"),
            ("él / ella podrá", "ele / ela poderá"),
            ("nosotros podremos", "nós poderemos"),
            ("vosotros podréis", "vocês poderão"),
            ("ellos podrán", "eles poderão")
        ],
        "examples": [
            ("PRES", "¿Puedes ayudarme un momento?", "Pode me ajudar um momento?"),
            ("PAS",  "No pude llegar a tiempo.", "Não pude chegar a tempo."),
            ("FUT",  "Pronto podré viajar.", "Em breve poderei viajar.")
        ]
    },
    # 7. DECIR
    "decir": {
        "verb": "DECIR",
        "pt": "DIZER",
        "icon": "speech",
        "present": [
            ("yo digo", "eu digo"),
            ("tú dices", "você diz"),
            ("él / ella dice", "ele / ela diz"),
            ("nosotros decimos", "nós dizemos"),
            ("vosotros decís", "vocês dizem"),
            ("ellos dicen", "eles dizem")
        ],
        "past": [
            ("yo dije", "eu disse"),
            ("tú dijiste", "você disse"),
            ("él / ella dijo", "ele / ela disse"),
            ("nosotros dijimos", "nós dissemos"),
            ("vosotros dijisteis", "vocês disseram"),
            ("ellos dijeron", "eles disseram")
        ],
        "future": [
            ("yo diré", "eu direi"),
            ("tú dirás", "você dirá"),
            ("él / ella dirá", "ele / ela dirá"),
            ("nosotros diremos", "nós diremos"),
            ("vosotros diréis", "vocês dirão"),
            ("ellos dirán", "eles dirão")
        ],
        "examples": [
            ("PRES", "Siempre digo la verdad.", "Sempre digo a verdade."),
            ("PAS",  "Te dije que vendría.", "Te disse que viria."),
            ("FUT",  "Mañana te diré la respuesta.", "Amanhã te direi a resposta.")
        ]
    },
    # 8. SABER
    "saber": {
        "verb": "SABER",
        "pt": "SABER",
        "icon": "brain",
        "present": [
            ("yo sé", "eu sei"),
            ("tú sabes", "você sabe"),
            ("él / ella sabe", "ele / ela sabe"),
            ("nosotros sabemos", "nós sabemos"),
            ("vosotros sabéis", "vocês sabem"),
            ("ellos saben", "eles sabem")
        ],
        "past": [
            ("yo supe", "eu soube"),
            ("tú supiste", "você soube"),
            ("él / ella supo", "ele / ela soube"),
            ("nosotros supimos", "nós soubemos"),
            ("vosotros supisteis", "vocês souberam"),
            ("ellos supieron", "eles souberam")
        ],
        "future": [
            ("yo sabré", "eu saberei"),
            ("tú sabrás", "você saberá"),
            ("él / ella sabrá", "ele / ela saberá"),
            ("nosotros sabremos", "nós saberemos"),
            ("vosotros sabréis", "vocês saberão"),
            ("ellos sabrán", "eles saberão")
        ],
        "examples": [
            ("PRES", "No sé qué hacer ahora.", "Não sei o que fazer agora."),
            ("PAS",  "Lo supe anoche.", "Soube disso ontem à noite."),
            ("FUT",  "Muy pronto lo sabremos.", "Muito em breve saberemos.")
        ]
    },
    # 9. QUERER
    "querer": {
        "verb": "QUERER",
        "pt": "QUERER / AMAR",
        "icon": "heart",
        "present": [
            ("yo quiero", "eu quero"),
            ("tú quieres", "você quer"),
            ("él / ella quiere", "ele / ela quer"),
            ("nosotros queremos", "nós queremos"),
            ("vosotros queréis", "vocês querem"),
            ("ellos quieren", "eles querem")
        ],
        "past": [
            ("yo quise", "eu quis"),
            ("tú quisiste", "você quis"),
            ("él / ella quiso", "ele / ela quis"),
            ("nosotros quisimos", "nós quisemos"),
            ("vosotros quisisteis", "vocês quiseram"),
            ("ellos quisieron", "eles quiseram")
        ],
        "future": [
            ("yo querré", "eu quererei"),
            ("tú querrás", "você quererá"),
            ("él / ella querrá", "ele / ela quererá"),
            ("nosotros querremos", "nós quereremos"),
            ("vosotros querréis", "vocês quererão"),
            ("ellos querrán", "eles quererão")
        ],
        "examples": [
            ("PRES", "Quiero aprender español.", "Quero aprender espanhol."),
            ("PAS",  "Quise llamarte pero no pude.", "Quis te ligar mas não pude."),
            ("FUT",  "Siempre te querré.", "Sempre te amarei/quererei.")
        ]
    },
    # 10. DAR
    "dar": {
        "verb": "DAR",
        "pt": "DAR",
        "icon": "gift",
        "present": [
            ("yo doy", "eu dou"),
            ("tú das", "você dá"),
            ("él / ella da", "ele / ela dá"),
            ("nosotros damos", "nós damos"),
            ("vosotros dais", "vocês dão [vós dais]"),
            ("ellos dan", "eles dão")
        ],
        "past": [
            ("yo di", "eu dei"),
            ("tú diste", "você deu"),
            ("él / ella dio", "ele / ela deu"),
            ("nosotros dimos", "nós demos"),
            ("vosotros disteis", "vocês deram"),
            ("ellos dieron", "eles deram")
        ],
        "future": [
            ("yo daré", "eu darei"),
            ("tú darás", "você dará"),
            ("él / ella dará", "ele / ela dará"),
            ("nosotros daremos", "nós daremos"),
            ("vosotros daréis", "vocês darão"),
            ("ellos darán", "eles darão")
        ],
        "examples": [
            ("PRES", "Te doy las gracias por todo.", "Te dou os agradecimentos por tudo."),
            ("PAS",  "Le di el regalo a mamá.", "Dei o presente para a mãe."),
            ("FUT",  "Te daré noticias mañana.", "Te darei notícias amanhã.")
        ]
    },
    # 11. VER
    "ver": {
        "verb": "VER",
        "pt": "VER",
        "icon": "eye",
        "present": [
            ("yo veo", "eu vejo"),
            ("tú ves", "você vê"),
            ("él / ella ve", "ele / ela vê"),
            ("nosotros vemos", "nós vemos"),
            ("vosotros veis", "vocês veem [vós vedes]"),
            ("ellos ven", "eles veem")
        ],
        "past": [
            ("yo vi", "eu vi"),
            ("tú viste", "você viu"),
            ("él / ella vio", "ele / ela viu"),
            ("nosotros vimos", "nós vimos"),
            ("vosotros visteis", "vocês viram"),
            ("ellos vieron", "eles viram")
        ],
        "future": [
            ("yo veré", "eu verei"),
            ("tú verás", "você verá"),
            ("él / ella verá", "ele / ela verá"),
            ("nosotros veremos", "nós veremos"),
            ("vosotros veréis", "vocês verão"),
            ("ellos verán", "eles verão")
        ],
        "examples": [
            ("PRES", "No veo nada aquí.", "Não vejo nada aqui."),
            ("PAS",  "Ayer vi una película genial.", "Ontem vi um filme genial."),
            ("FUT",  "Nos veremos la próxima semana.", "Nos veremos na próxima semana.")
        ]
    },
    # 12. PONER
    "poner": {
        "verb": "PONER",
        "pt": "PÔR / COLOCAR",
        "icon": "box",
        "present": [
            ("yo pongo", "eu ponho / coloco"),
            ("tú pones", "você põe"),
            ("él / ella pone", "ele / ela põe"),
            ("nosotros ponemos", "nós pomos"),
            ("vosotros ponéis", "vocês põem"),
            ("ellos ponen", "eles põem")
        ],
        "past": [
            ("yo puse", "eu pus"),
            ("tú pusiste", "você pôs"),
            ("él / ella puso", "ele / ela pôs"),
            ("nosotros pusimos", "nós pusemos"),
            ("vosotros pusisteis", "vocês puseram"),
            ("ellos pusieron", "eles puseram")
        ],
        "future": [
            ("yo pondré", "eu porei"),
            ("tú pondrás", "você porá"),
            ("él / ella pondrá", "ele / ela porá"),
            ("nosotros pondremos", "nós poremos"),
            ("vosotros pondréis", "vocês porão"),
            ("ellos pondrán", "eles porão")
        ],
        "examples": [
            ("PRES", "Pongo la mesa para cenar.", "Ponho a mesa para jantar."),
            ("PAS",  "Puse las llaves en la mesa.", "Pus as chaves na mesa."),
            ("FUT",  "Pondré más atención luego.", "Porei mais atenção depois.")
        ]
    },
    # 13. LLEGAR
    "llegar": {
        "verb": "LLEGAR",
        "pt": "CHEGAR",
        "icon": "arrow",
        "present": [
            ("yo llego", "eu chego"),
            ("tú llegas", "você chega"),
            ("él / ella llega", "ele / ela chega"),
            ("nosotros llegamos", "nós chegamos"),
            ("vosotros llegáis", "vocês chegam"),
            ("ellos llegan", "eles chegam")
        ],
        "past": [
            ("yo llegué", "eu cheguei"),
            ("tú llegaste", "você chegou"),
            ("él / ella llegó", "ele / ela chegou"),
            ("nosotros llegamos", "nós chegamos"),
            ("vosotros llegasteis", "vocês chegaram"),
            ("ellos llegaron", "eles chegaram")
        ],
        "future": [
            ("yo llegaré", "eu chegarei"),
            ("tú llegarás", "você chegará"),
            ("él / ella llegará", "ele / ela chegará"),
            ("nosotros llegaremos", "nós chegaremos"),
            ("vosotros llegaréis", "vocês chegarão"),
            ("ellos llegarán", "eles chegarão")
        ],
        "examples": [
            ("PRES", "Siempre llego puntual.", "Sempre chego pontual."),
            ("PAS",  "Ayer llegué muy tarde.", "Ontem cheguei muito tarde."),
            ("FUT",  "Llegaré a tiempo mañana.", "Chegarei a tempo amanhã.")
        ]
    },
    # 14. PASAR
    "pasar": {
        "verb": "PASAR",
        "pt": "PASSAR / ACONTECER",
        "icon": "clock",
        "present": [
            ("yo paso", "eu passo"),
            ("tú pasas", "você passa"),
            ("él / ella pasa", "ele / ela passa"),
            ("nosotros pasamos", "nós passamos"),
            ("vosotros pasáis", "vocês passam"),
            ("ellos pasan", "eles passam")
        ],
        "past": [
            ("yo pasé", "eu passei"),
            ("tú pasaste", "você passou"),
            ("él / ella pasó", "ele / ela passou"),
            ("nosotros pasamos", "nós passamos"),
            ("vosotros pasasteis", "vocês passaram"),
            ("ellos pasaron", "eles passaram")
        ],
        "future": [
            ("yo pasaré", "eu passarei"),
            ("tú pasarás", "você passará"),
            ("él / ella pasará", "ele / ela passará"),
            ("nosotros pasaremos", "nós passaremos"),
            ("vosotros pasaréis", "vocês passarão"),
            ("ellos pasarán", "eles passarão")
        ],
        "examples": [
            ("PRES", "¿Qué pasa aquí?", "O que acontece aqui?"),
            ("PAS",  "Lo pasé muy bien contigo.", "Passei muito bem com você."),
            ("FUT",  "El tiempo pasará rápido.", "O tempo passará rápido.")
        ]
    },
    # 15. HABER
    "haber": {
        "verb": "HABER",
        "pt": "HAVER / TER (AUXILIAR)",
        "icon": "star",
        "present": [
            ("yo he", "eu hei / tenho"),
            ("tú has", "você há / tem"),
            ("él / ella ha / hay", "ele há / há (existe)"),
            ("nosotros hemos", "nós havemos / temos"),
            ("vosotros habéis", "vocês haveis"),
            ("ellos han", "eles hão / têm")
        ],
        "past": [
            ("yo hube", "eu houve"),
            ("tú hubiste", "você houveste"),
            ("él / ella hubo", "houve (aconteceu)"),
            ("nosotros hubimos", "nós houvemos"),
            ("vosotros hubisteis", "vocês houvestes"),
            ("ellos hubieron", "eles houveram")
        ],
        "future": [
            ("yo habré", "eu haverei"),
            ("tú habrás", "você haverá"),
            ("él / ella habrá", "haverá (existirá)"),
            ("nosotros habremos", "nós haveremos"),
            ("vosotros habréis", "vocês havereis"),
            ("ellos habrán", "eles haverão")
        ],
        "examples": [
            ("PRES", "Hoy hay mucha gente aquí.", "Hoje há muita gente aqui."),
            ("PAS",  "Ayer hubo una gran fiesta.", "Ontem houve uma grande festa."),
            ("FUT",  "Mañana habrá buenas noticias.", "Amanhã haverá boas notícias.")
        ]
    },
    # MODELO REGULAR 1 (-AR): HABLAR
    "hablar": {
        "verb": "HABLAR",
        "pt": "FALAR",
        "icon": "speech",
        "present": [
            ("yo hablo", "eu falo"),
            ("tú hablas", "você fala"),
            ("él / ella habla", "ele / ela fala"),
            ("nosotros hablamos", "nós falamos"),
            ("vosotros habláis", "vocês falam [vós]"),
            ("ellos hablan", "eles falam")
        ],
        "past": [
            ("yo hablé", "eu falei"),
            ("tú hablaste", "você falou"),
            ("él / ella habló", "ele / ela falou"),
            ("nosotros hablamos", "nós falamos"),
            ("vosotros hablasteis", "vocês falaram [vós]"),
            ("ellos hablaron", "eles falaram")
        ],
        "future": [
            ("yo hablaré", "eu falarei"),
            ("tú hablarás", "você falará"),
            ("él / ella hablará", "ele / ela falará"),
            ("nosotros hablaremos", "nós falaremos"),
            ("vosotros hablaréis", "vocês falarão [vós]"),
            ("ellos hablarán", "eles falarão")
        ],
        "examples": [
            ("PRES", "Hablo español todos los días.", "Falo espanhol todos os dias."),
            ("PAS",  "Ayer hablé con María.", "Ontem falei com a Maria."),
            ("FUT",  "Mañana hablaré con el jefe.", "Amanhã falarei com o chefe.")
        ]
    },
    # MODELO REGULAR 2 (-ER): COMER
    "comer": {
        "verb": "COMER",
        "pt": "COMER",
        "icon": "food",
        "present": [
            ("yo como", "eu como"),
            ("tú comes", "você come"),
            ("él / ella come", "ele / ela come"),
            ("nosotros comemos", "nós comemos"),
            ("vosotros coméis", "vocês comem [vós]"),
            ("ellos comen", "eles comem")
        ],
        "past": [
            ("yo comí", "eu comi"),
            ("tú comiste", "você comeu"),
            ("él / ella comió", "ele / ela comeu"),
            ("nosotros comimos", "nós comemos"),
            ("vosotros comisteis", "vocês comeram [vós]"),
            ("ellos comieron", "eles comeram")
        ],
        "future": [
            ("yo comeré", "eu comerei"),
            ("tú comerás", "você comerá"),
            ("él / ella comerá", "ele / ela comerá"),
            ("nosotros comeremos", "nós comeremos"),
            ("vosotros comeréis", "vocês comerão [vós]"),
            ("ellos comerán", "eles comerão")
        ],
        "examples": [
            ("PRES", "Como frutas por la mañana.", "Como frutas pela manhã."),
            ("PAS",  "Ayer comí una paella increíble.", "Ontem comi uma paella incrível."),
            ("FUT",  "Mañana comeremos juntos.", "Amanhã comeremos juntos.")
        ]
    },
    # MODELO REGULAR 3 (-IR): VIVIR
    "vivir": {
        "verb": "VIVIR",
        "pt": "VIVER / MORAR",
        "icon": "house",
        "present": [
            ("yo vivo", "eu moro"),
            ("tú vives", "você mora"),
            ("él / ella vive", "ele / ela mora"),
            ("nosotros vivimos", "nós moramos"),
            ("vosotros vivís", "vocês moram [vós]"),
            ("ellos viven", "eles moram")
        ],
        "past": [
            ("yo viví", "eu morei"),
            ("tú viviste", "você morou"),
            ("él / ella vivió", "ele / ela morou"),
            ("nosotros vivimos", "nós moramos"),
            ("vosotros vivisteis", "vocês moraram [vós]"),
            ("ellos vivieron", "eles moraram")
        ],
        "future": [
            ("yo viviré", "eu morarei"),
            ("tú vivirás", "você morará"),
            ("él / ella vivirá", "ele / ela morará"),
            ("nosotros viviremos", "nós moraremos"),
            ("vosotros viviréis", "vocês morarão [vós]"),
            ("ellos vivirán", "eles morarão")
        ],
        "examples": [
            ("PRES", "Ahora vivo en São Paulo.", "Agora moro em São Paulo."),
            ("PAS",  "Viví dos años en Madrid.", "Morei dois anos em Madri."),
            ("FUT",  "El próximo año viviré afuera.", "No próximo ano morarei fora.")
        ]
    }
}

def draw_generic_icon(draw: ImageDraw.ImageDraw, icon_type: str, x: int, y: int):
    cx, cy = x + 18, y + 12
    if icon_type == "speech":
        draw.rounded_rectangle([(x, y), (x + 32, y + 20)], radius=5, outline=(0, 0, 0), width=2, fill=(255, 255, 255))
        draw.polygon([(x + 6, y + 19), (x + 11, y + 26), (x + 16, y + 19)], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.line([(x + 7, y + 19), (x + 15, y + 19)], fill=(255, 255, 255), width=2)
        draw.line([(x + 6, y + 7), (x + 26, y + 7)], fill=(0, 0, 0), width=2)
        draw.line([(x + 6, y + 13), (x + 20, y + 13)], fill=(0, 0, 0), width=2)
    elif icon_type == "food":
        draw.ellipse([(cx - 12, cy - 12), (cx + 12, cy + 12)], outline=(0, 0, 0), width=2)
        draw.line([(cx - 18, cy - 10), (cx - 18, cy + 10)], fill=(0, 0, 0), width=2)
        draw.line([(cx + 18, cy - 10), (cx + 18, cy + 10)], fill=(0, 0, 0), width=2)
    elif icon_type == "house":
        draw.polygon([(cx, cy - 12), (cx - 16, cy), (cx + 16, cy)], fill=(0, 0, 0))
        draw.rectangle([(cx - 12, cy), (cx + 12, cy + 12)], outline=(0, 0, 0), width=2)
        draw.rectangle([(cx - 4, cy + 4), (cx + 4, cy + 12)], fill=(0, 0, 0))
    elif icon_type == "arrow":
        draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(0, 0, 0), width=3)
        draw.polygon([(cx + 6, cy - 8), (cx + 16, cy), (cx + 6, cy + 8)], fill=(0, 0, 0))
    elif icon_type == "clock":
        draw.ellipse([(cx - 12, cy - 12), (cx + 12, cy + 12)], outline=(0, 0, 0), width=2)
        draw.line([(cx, cy), (cx, cy - 7)], fill=(0, 0, 0), width=2)
        draw.line([(cx, cy), (cx + 6, cy)], fill=(0, 0, 0), width=2)
    elif icon_type == "star":
        draw.polygon([
            (cx, cy - 12), (cx + 3, cy - 3), (cx + 12, cy), (cx + 3, cy + 3),
            (cx, cy + 12), (cx - 3, cy + 3), (cx - 12, cy), (cx - 3, cy - 3)
        ], fill=(0, 0, 0))
    elif icon_type == "heart":
        draw.ellipse([(cx - 9, cy - 8), (cx - 1, cy)], fill=(0, 0, 0))
        draw.ellipse([(cx + 1, cy - 8), (cx + 9, cy)], fill=(0, 0, 0))
        draw.polygon([(cx - 9, cy - 4), (cx + 9, cy - 4), (cx, cy + 9)], fill=(0, 0, 0))
    elif icon_type == "pin":
        draw.ellipse([(cx - 7, cy - 11), (cx + 7, cy + 3)], fill=(0, 0, 0))
        draw.polygon([(cx - 6, cy - 2), (cx + 6, cy - 2), (cx, cy + 11)], fill=(0, 0, 0))
        draw.ellipse([(cx - 3, cy - 7), (cx + 3, cy - 1)], fill=(255, 255, 255))
    elif icon_type == "gear":
        draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], outline=(0, 0, 0), width=3)
        draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(0, 0, 0), width=3)
        draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(0, 0, 0), width=3)
        draw.ellipse([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=(255, 255, 255))
    elif icon_type == "eye":
        draw.ellipse([(cx - 14, cy - 8), (cx + 14, cy + 8)], outline=(0, 0, 0), width=2)
        draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=(0, 0, 0))
    elif icon_type == "box":
        draw.rectangle([(cx - 11, cy - 9), (cx + 11, cy + 9)], outline=(0, 0, 0), width=2)
        draw.line([(cx - 11, cy - 3), (cx + 11, cy - 3)], fill=(0, 0, 0), width=1)
        draw.line([(cx, cy - 3), (cx, cy + 9)], fill=(0, 0, 0), width=1)
    else:
        draw.line([(cx - 10, cy), (cx - 3, cy + 7)], fill=(0, 0, 0), width=3)
        draw.line([(cx - 3, cy + 7), (cx + 11, cy - 7)], fill=(0, 0, 0), width=3)

def generate_verb_strip(verb_key: str) -> Image.Image:
    data = VERBS_DATA[verb_key.lower()]
    canvas_h = 1600
    img = Image.new('RGB', (WIDTH, canvas_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = 6
    draw.text((WIDTH // 2, y), "- - - - - - - - - - - - - - - - - - - - - - - -", fill=(0, 0, 0), anchor="mm", font=get_font(11))
    y += 12

    card_start_y = y
    
    # Barra de Título Superior Integrada
    draw.rectangle([(6, y), (WIDTH - 6, y + 54)], fill=(0, 0, 0))
    draw.text((18, y + 27), data["verb"], fill=(255, 255, 255), anchor="lm", font=get_font(32, bold=True))
    draw.text((WIDTH - 18, y + 27), f"({data['pt']})", fill=(255, 255, 255), anchor="rm", font=get_font(17, bold=True))
    y += 58

    # Subtítulo + Ícone
    draw.rectangle([(6, y), (WIDTH - 6, y + 32)], fill=(240, 240, 240))
    draw.text((18, y + 16), "6 PESSOAS : 3 TEMPOS", fill=(0, 0, 0), anchor="lm", font=get_font(12, bold=True))
    draw_generic_icon(draw, data.get("icon", "check"), WIDTH - 52, y + 4)
    y += 36

    # Blocos de Conjugação
    def render_tense_block(cur_y: int, title_es: str, title_pt: str, conjugations: list) -> int:
        draw.rectangle([(6, cur_y), (WIDTH - 6, cur_y + 24)], fill=(0, 0, 0))
        draw.text((16, cur_y + 12), title_es, fill=(255, 255, 255), anchor="lm", font=get_font(13, bold=True))
        draw.text((WIDTH - 16, cur_y + 12), f"[{title_pt}]", fill=(255, 255, 255), anchor="rm", font=get_font(12, bold=True))
        cur_y += 26

        for idx, (es, pt) in enumerate(conjugations):
            if idx % 2 == 1:
                draw.rectangle([(6, cur_y - 1), (WIDTH - 6, cur_y + 24)], fill=(240, 240, 240))
            
            draw.text((16, cur_y + 11), es, fill=(0, 0, 0), anchor="lm", font=get_font(16, bold=True))
            draw.text((WIDTH - 16, cur_y + 11), f"-> {pt}", fill=(0, 0, 0), anchor="rm", font=get_font(14))
            cur_y += 24
            
        return cur_y + 4

    y = render_tense_block(y, "1. PRESENTE", "Presente", data["present"])
    y = render_tense_block(y, "2. PASSADO", "Pret. Indefinido", data["past"])
    y = render_tense_block(y, "3. FUTURO", "Futuro Simples", data["future"])

    # Seção com 3 Frases de Demonstração
    draw.rectangle([(6, y), (WIDTH - 6, y + 24)], fill=(0, 0, 0))
    draw.text((16, y + 12), "FRASES DE DEMONSTRAÇÃO", fill=(255, 255, 255), anchor="lm", font=get_font(12, bold=True))
    y += 26

    for idx, (tense, es_phrase, pt_phrase) in enumerate(data["examples"]):
        bg_col = (255, 255, 255) if idx % 2 == 0 else (244, 244, 244)
        box_h = 44
        draw.rectangle([(6, y), (WIDTH - 6, y + box_h)], fill=bg_col)
        
        draw.rounded_rectangle([(14, y + 6), (56, y + 24)], radius=4, fill=(0, 0, 0))
        draw.text((35, y + 15), tense, fill=(255, 255, 255), anchor="mm", font=get_font(10, bold=True))
        
        draw.text((64, y + 15), es_phrase, fill=(0, 0, 0), anchor="lm", font=get_font(13, bold=True))
        draw.text((64, y + 33), f"-> {pt_phrase}", fill=(0, 0, 0), anchor="lm", font=get_font(12))
        
        y += box_h
        if idx < len(data["examples"]) - 1:
            draw.line([(14, y), (WIDTH - 14, y)], fill=(210, 210, 210), width=1)

    y += 4
    draw.rectangle([(6, card_start_y), (WIDTH - 6, y)], outline=(0, 0, 0), width=3)
    y += 10

    draw.text((WIDTH // 2, y), "- - - - - - - - - - - - - - - - - - - - - - - -", fill=(0, 0, 0), anchor="mm", font=get_font(11))
    y += 10

    return img.crop((0, 0, WIDTH, y))

def main():
    out_dir = Path(r"C:\Users\felip\Documents\git\phomemo-m02\tiras")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Gerando catálogo de {len(VERBS_DATA)} verbos...")
    for key in VERBS_DATA:
        img = generate_verb_strip(key)
        path = out_dir / f"tira_{key}.png"
        img.save(path)
        print(f" -> {key.upper()} ({img.width}x{img.height}px)")
    print("Todas as tiras foram geradas com sucesso!")

if __name__ == "__main__":
    main()

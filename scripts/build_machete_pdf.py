from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "machete-tercer-parcial.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
PAGE_W, PAGE_H = A4
MX, MT, MB = 13 * mm, 10 * mm, 10 * mm
INK, WINE, BLUE = colors.HexColor("#172033"), colors.HexColor("#7A2138"), colors.HexColor("#234C6B")
MUTED, RULE = colors.HexColor("#5C6570"), colors.HexColor("#B8C0C9")


def st(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=10, leading=13,
                textColor=INK, spaceAfter=3.2, allowWidows=0, allowOrphans=0)
    base.update(kw)
    return ParagraphStyle(**base)


TITLE = st("title", fontName="Helvetica-Bold", fontSize=15.5, leading=17,
           textColor=WINE, alignment=TA_CENTER, spaceAfter=5)
QUESTION = st("question", fontName="Helvetica-Bold", fontSize=12, leading=14,
              textColor=BLUE, spaceBefore=4, spaceAfter=2.5)
BODY = st("body")
THESIS = st("thesis", fontName="Helvetica-Bold", fontSize=10.2, leading=12.8,
            textColor=WINE, leftIndent=7, borderColor=WINE, borderWidth=0,
            borderLeftWidth=1.5, borderPadding=(1, 0, 1, 6), spaceBefore=2, spaceAfter=4)
MINI = st("mini", fontSize=8.8, leading=10.5, spaceAfter=1.2, leftIndent=8, firstLineIndent=-7)


def p(text, style=BODY):
    return Paragraph(text, style)


def q(text):
    return p(text, QUESTION)


def thesis(text):
    return p(text, THESIS)


def item(term, definition):
    return p(f"<b>{term}:</b> {definition}", MINI)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(.35)
    canvas.line(MX, PAGE_H - 7.2 * mm, PAGE_W - MX, PAGE_H - 7.2 * mm)
    canvas.setFont("Helvetica-Bold", 6.8)
    canvas.setFillColor(WINE)
    canvas.drawString(MX, PAGE_H - 5.4 * mm, "PSICOANÁLISIS FREUD - TERCER PARCIAL")
    canvas.setFont("Helvetica", 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MX, PAGE_H - 5.4 * mm, "Repaso orientado a consignas")
    canvas.drawRightString(PAGE_W - MX, 5.2 * mm, f"{doc.page} / 4")
    canvas.restoreState()


frame = Frame(MX, MB, PAGE_W - 2 * MX, PAGE_H - MT - MB,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc = BaseDocTemplate(str(OUT), pagesize=A4, title="Machete de repaso - tercer parcial",
                      author="Psicoanálisis Freud - Cátedra Laznik")
doc.addPageTemplates(PageTemplate(id="clean", frames=[frame], onPage=header_footer))
story = []


def page(title):
    story.append(p(title, TITLE))


page("MÁS ALLÁ: TRAUMA, SUEÑO Y REPETICIÓN")
q1 = "¿Por qué Freud postula un más allá del principio del placer?"
story += [q(q1), thesis("Tesis: ciertos fenómenos repiten displacer que no puede explicarse como placer para otro sistema. Freud no elimina el principio del placer: descubre una tarea más originaria, ligar la excitación para que aquel pueda operar."),
    p("Hasta 1920, el aparato parecía regulado por la disminución de tensión. El displacer corriente no refutaba esa tesis: el principio de realidad posterga la satisfacción y la represión vuelve displacentero para el yo lo que satisface a una moción inconsciente. Pero los <b>sueños traumáticos</b>, el <b>fort-da</b> y la <b>compulsión de repetición en transferencia</b> muestran una insistencia que no siempre puede reconducirse a una ganancia de placer previa."),
    p("El nuevo trauma se define económicamente: la sorpresa y la falta de preparación angustiada permiten que una magnitud excesiva atraviese la protección antiestímulo. Entran cantidades no ligadas y el yo queda en desvalimiento. El principio del placer queda transitoriamente abolido; primero hay que dominar y ligar esa excitación."),
    q("¿Cómo reformula esto la teoría del sueño?"),
    p("En la teoría clásica, el sueño realiza de manera desfigurada un <b>deseo reprimido</b>. Condensación, desplazamiento y figurabilidad permiten una satisfacción inconsciente compatible con seguir durmiendo: el sueño es guardián del dormir. En el sueño traumático, en cambio, retorna con terror una escena que nunca fue placentera para sistema alguno y el soñante despierta."),
    p("No conviene decir simplemente que esos sueños carecen de función o son totalmente ininterpretables. Su repetición intenta producir retroactivamente la preparación que faltó y <b>ligar</b> la excitación. La aparente excepción revela una operación previa al cumplimiento de deseo y al gobierno del principio del placer."),
    q("¿Qué muestran el fort-da y la transferencia?"),
    p("En el juego, el niño transforma en actividad la partida pasivamente sufrida. El retorno, <i>da</i>, ofrece placer directo; pero Freud subraya que se repite con mayor frecuencia el <i>fort</i>, la desaparición displacentera. El placer del juego completo no agota la insistencia del primer acto."),
    p("También hay que distinguir el <i>agieren</i> de 1914 -actuar lo reprimido que no se recuerda- de la compulsión de repetición de 1920, que incluye fracasos, vínculos y padecimientos nunca placenteros. Esta última prepara el segundo dualismo: <b>Eros</b> liga y reúne; la <b>pulsión de muerte</b> desliga y tiende a restaurar un estado anterior. El primer dualismo era autoconservación/sexuales; libido yoica/de objeto son destinos de la libido sexual, no ese dualismo."),
    q("¿Cómo se articula la pulsión de muerte con el masoquismo?"),
    p("La libido liga parte de la pulsión de muerte y desvía destrucción hacia afuera. Un resto permanece ligado en el interior: <b>masoquismo erógeno primario</b>. Sobre esa base se distinguen el masoquismo femenino -fantasías de posición pasiva, infantil y castigada- y el <b>masoquismo moral</b>, donde el padecimiento mismo satisface una necesidad de castigo. Esta última articulación permite comprender culpa inconsciente y reacción terapéutica negativa."), PageBreak()]

page("SEXUALIDAD, EDIPO Y CASTRACIÓN")
story += [q("¿Cómo se relacionan fase fálica, Edipo y castración?"), thesis("Tesis: la fase fálica organiza la diferencia bajo la oposición fálico/castrado. El complejo de castración interviene de modo asimétrico: en el varón conduce al sepultamiento del Edipo; en la niña posibilita su entrada."),
    p("Las organizaciones oral, sádico-anal y fálica no son escalones que desaparecen. Cada una ordena satisfacción y objeto: incorporación; retención-expulsión y actividad-pasividad; finalmente primado del falo. <b>Fijación</b> es la persistencia privilegiada de libido en una modalidad; <b>regresión</b>, el retorno a ella ante un conflicto. La latencia introduce represión y diques; la organización genital postpuberal coordina sin borrar lo anterior."),
    p("En la fase fálica rige la premisa universal del pene: la diferencia anatómica todavía se interpreta como fálico/castrado, no como masculino/femenino. El falo organiza tener, perder, dar y faltar; no debe reducirse al órgano ni conviene trasladar sin explicación fórmulas lacanianas a una respuesta sobre Freud."),
    q("¿En qué consiste la asimetría del Edipo?"),
    p("En el <b>varón</b>, la madre es objeto y el padre rival y modelo identificatorio. La amenaza de castración se vuelve eficaz al enlazarse con la percepción de la diferencia. Ante la alternativa entre conservar el pene y sostener las investiduras incestuosas, abandona los objetos edípicos: la castración <b>saca</b> del Edipo. Las investiduras se sustituyen por identificaciones que participan en la formación del superyó."),
    p("En la <b>niña</b>, el primer objeto también es la madre. La ligazón preedípica es larga, intensa y ambivalente. La diferencia se interpreta como perjuicio consumado: herida narcisista, envidia del pene y reproche a la madre. Por eso la castración <b>introduce</b> al Edipo: exige extrañarse de la madre, cambiar de objeto hacia el padre y, en la elaboración freudiana, desplazar pene por hijo. La salida es menos tajante y puede producirse por desilusión."),
    q("¿Cómo responder sobre «Pegan a un niño»?"),
    p("La fantasía se reconstruye en tres tiempos. 1) «El padre pega al niño odiado»: significa que ama al sujeto. 2) «Soy pegado por el padre»: fase inconsciente y construida, donde culpa y regresión sádico-anal convierten el castigo en sustituto de ser amado. 3) «Pegan a unos niños»: forma comunicada, con agente impersonal y satisfacción de apariencia sádica pero posición masoquista. En análisis se parte de la tercera, se reconstruye la primera y se construye la segunda. Es cicatriz del Edipo y fijación de satisfacción, no recuerdo material recuperado."), PageBreak()]

page("SEGUNDA TÓPICA Y RESISTENCIAS")
story += [q("¿Cómo se relacionan primera y segunda tópica?"), thesis("Tesis: no existe un mapeo uno a uno. Icc/Prcc/Cc describe la relación de los contenidos con la conciencia; ello/yo/superyó localiza instancias, conflictos y resistencias. La segunda tópica complementa, no reemplaza, a la primera."),
    p("El inconsciente <b>descriptivo</b> es lo actualmente no consciente; lo latente puede devenir consciente. El inconsciente <b>dinámico</b> es lo mantenido fuera de la conciencia por represión y que retorna deformado. La clínica obliga a agregar una dimensión <b>estructural</b>: lo inconsciente no se reduce a lo reprimido."),
    p("Lo reprimido pugna por retornar y, por eso, no puede ser la fuerza que se opone a su retorno. La resistencia parte del yo sin que el paciente lo sepa: hay yo inconsciente, y también superyó inconsciente. Fórmula central: <b>todo lo reprimido es inconsciente, pero no todo lo inconsciente es reprimido</b>. El ello es enteramente inconsciente, pero no todo lo inconsciente es ello."),
    q("¿Cómo caracteriza Freud al yo y sus vasallajes?"),
    p("El <b>ello</b> es sede pulsional, reservorio libidinal y contiene tanto lo reprimido como lo nunca reprimido. El <b>yo</b> es una parte del ello modificada por la realidad, corporal y parcialmente inconsciente; liga, sintetiza, prueba realidad, gobierna la motilidad y produce la señal de angustia. El <b>superyó</b>, heredero del Edipo y sedimento de identificaciones tempranas, encarna ideal y prohibición, pero también puede actuar como mandato cruel."),
    p("El yo aparece en su potencia porque organiza y defiende, y en su endeblez porque toma su energía del ello y debe servir a tres amos: mundo exterior, ello y superyó. De allí surgen, respectivamente, peligro realista, exigencia pulsional y amenaza de castigo o pérdida del amor del superyó."),
    q("¿Cuáles son las cinco resistencias?"),
    p("Tres son yoicas. La <b>resistencia de represión</b> sostiene mediante contrainvestidura lo apartado. La <b>resistencia de transferencia</b> actualiza el conflicto con el analista; la vertiente erótica u hostil puede interrumpir la asociación. La <b>ganancia secundaria</b> reúne ventajas que el yo obtiene con el síntoma ya formado; no debe confundirse con la satisfacción pulsional primaria en el síntoma."),
    p("La resistencia del <b>ello</b> es la compulsión de repetición: antiguas vías y fijaciones persisten incluso después de interpretar, por lo cual requieren reelaboración. La del <b>superyó</b> es la necesidad de castigo, ligada a culpa inconsciente y reacción terapéutica negativa. Interpretar representaciones conserva valor, sobre todo ante resistencias yoicas, pero no levanta automáticamente lo que procede del ello o del superyó."),
    q("Distinciones que suelen decidir la respuesta"),
    p("Ganancia primaria no es ganancia secundaria: la primera es satisfacción pulsional <i>en</i> el síntoma; la segunda son ventajas que el yo obtiene <i>con</i> el síntoma ya constituido. Culpa consciente tampoco equivale a necesidad inconsciente de castigo: el paciente puede sentirse enfermo, no culpable. Y transferencia no significa siempre resistencia: la vertiente tierna puede sostener el trabajo, mientras las formas erótica u hostil pueden obstaculizarlo."), PageBreak()]

page("ANGUSTIA + DEFINICIONES PARA RECORDAR")
story += [q("¿Qué cambia en la tercera teoría de la angustia?"), thesis("Tesis: Freud invierte la causalidad de la segunda teoría. Ya no es la represión la que produce angustia; el yo anticipa un peligro mediante angustia-señal y pone en marcha represión y defensa. A la vez conserva una angustia automática ante el desvalimiento efectivo."),
    p("Primera teoría: excitación sexual somática no elaborada se transforma en angustia, especialmente en las neurosis actuales. Segunda: la libido afectada por la represión se muda en angustia. Tercera: condición de peligro -> angustia-señal en el yo -> defensa/represión -> síntoma. La reformulación no borra todos los desarrollos anteriores, sino que redistribuye causas y funciones."),
    p("La <b>angustia automática</b> corresponde a una situación traumática efectiva: el yo queda pasivamente desbordado por cantidad no ligada. La <b>señal</b> es una reproducción atenuada y anticipatoria producida por el yo para evitar ese desborde. Las condiciones de peligro siguen la serie desvalimiento, pérdida de objeto, castración y pérdida del amor del superyó. En Hans: mociones edípicas -> peligro de castración -> señal -> represión -> desplazamiento al caballo -> fobia; así un peligro interno inevitable se vuelve externo y evitable, al precio de una inhibición."),
    p("<b>Puente trauma-angustia:</b> el trauma nombra desvalimiento y no ligadura; la angustia automática es su irrupción. Cuando una condición semejante puede anticiparse, el yo produce señal y moviliza defensa."),
    q("Lista mnemotécnica de definiciones"),
    item("Ligadura", "operación que domina cantidades y las integra en conexiones representacionales; condición para el principio del placer."),
    item("Trauma 1920", "sorpresa + falta de preparación + ruptura antiestímulo + exceso no ligado + desvalimiento."),
    item("Compulsión de repetición", "insistencia de experiencias y vías más allá de una satisfacción placentera previa."),
    item("Eros / muerte", "ligar, reunir y complejizar / desligar y tender a restaurar un estado anterior."),
    item("Fijación / regresión", "persistencia de libido en una modalidad / retorno a ella ante conflicto."),
    item("Fase fálica", "organización genital infantil bajo primado del falo y oposición fálico/castrado."),
    item("Castración", "amenaza que saca al varón del Edipo; perjuicio supuesto consumado que introduce a la niña."),
    item("ICC estructural", "sectores inconscientes no necesariamente reprimidos en ello, yo y superyó."),
    item("Superyó", "heredero del Edipo e identificaciones; ideal, ley y posible mandato cruel."),
    item("Vasallajes", "dependencia del yo respecto del mundo, el ello y el superyó."),
    item("Ganancia primaria/secundaria", "satisfacción pulsional en el síntoma / ventajas agregadas obtenidas con él."),
    item("Reacción terapéutica negativa", "empeoramiento ante la mejoría, ligado a necesidad inconsciente de castigo."),
    item("Angustia automática/señal", "desborde traumático efectivo / anticipación atenuada que moviliza defensa."),
    Spacer(1, 2), thesis("Antes de entregar: tesis -> texto/momento -> problema clínico -> mecanismo -> diferencia con formulación anterior -> consecuencia. Articular no es identificar: qué se conserva, qué cambia y qué permite explicar.")]

doc.build(story)
print(OUT)

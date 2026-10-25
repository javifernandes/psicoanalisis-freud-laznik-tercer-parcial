from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "machete-tercer-parcial.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
MARGIN_X = 10 * mm
MARGIN_TOP = 12 * mm
MARGIN_BOTTOM = 10 * mm
COL_W = PAGE_W - 2 * MARGIN_X

INK = colors.HexColor("#172033")
ACCENT = colors.HexColor("#7A2138")
ACCENT_2 = colors.HexColor("#234C6B")
PALE = colors.HexColor("#F0F3F6")
PALE_RED = colors.HexColor("#F6EAED")
LINE = colors.HexColor("#9BA6B2")


def style(name, **kwargs):
    base = dict(
        name=name,
        fontName="Helvetica",
        fontSize=8.4,
        leading=10,
        textColor=INK,
        spaceAfter=1.5,
        allowWidows=0,
        allowOrphans=0,
    )
    base.update(kwargs)
    return ParagraphStyle(**base)


BODY = style("body")
BULLET = style("bullet", leftIndent=7, firstLineIndent=-5, bulletIndent=0, spaceAfter=0.8)
H1 = style(
    "h1",
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=15.5,
    textColor=ACCENT,
    alignment=TA_CENTER,
    spaceAfter=5,
)
H2 = style(
    "h2",
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=11.4,
    textColor=colors.white,
    backColor=ACCENT_2,
    borderPadding=(2.5, 4, 2.5, 4),
    spaceBefore=3,
    spaceAfter=3,
)
H3 = style(
    "h3",
    fontName="Helvetica-Bold",
    fontSize=8.8,
    leading=10,
    textColor=ACCENT,
    spaceBefore=2.5,
    spaceAfter=1.3,
)
CALLOUT = style(
    "callout",
    fontName="Helvetica-Bold",
    fontSize=8.2,
    leading=9.7,
    backColor=PALE_RED,
    borderColor=ACCENT,
    borderWidth=0.6,
    borderPadding=4,
    spaceBefore=2,
    spaceAfter=3,
)
SMALL = style("small", fontSize=7.3, leading=8.5, spaceAfter=0.5)
FOOT = style("foot", fontSize=6.2, leading=7, textColor=colors.HexColor("#5C6570"), alignment=TA_CENTER)


def p(text, s=BODY):
    return Paragraph(text, s)


def bullet(text):
    return Paragraph(text, BULLET, bulletText="-")


def heading(text):
    return Paragraph(text, H2)


def sub(text):
    return Paragraph(text, H3)


def callout(text):
    return Paragraph(text, CALLOUT)


def tbl(rows, widths=None, header=True, font=7.1):
    cooked = []
    for ridx, row in enumerate(rows):
        row_style = ParagraphStyle(
            f"t{ridx}",
            parent=SMALL,
            fontName="Helvetica-Bold" if ridx == 0 and header else "Helvetica",
            textColor=colors.white if ridx == 0 and header else INK,
            fontSize=font,
            leading=font + 1.15,
        )
        cooked.append([Paragraph(str(cell), row_style) for cell in row])
    table = Table(cooked, colWidths=widths or [COL_W / len(rows[0])] * len(rows[0]), hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT_2))
    for idx in range(1 if header else 0, len(rows)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), PALE))
    table.setStyle(TableStyle(commands))
    return table


def keep(*items):
    return KeepTogether(list(items))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN_X, PAGE_H - 8.2 * mm, PAGE_W - MARGIN_X, PAGE_H - 8.2 * mm)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(ACCENT)
    canvas.drawString(MARGIN_X, PAGE_H - 6.4 * mm, "PSICOANÁLISIS FREUD - TERCER PARCIAL")
    canvas.setFont("Helvetica", 6.5)
    canvas.setFillColor(colors.HexColor("#5C6570"))
    canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 6.4 * mm, "Machete de repaso express")
    canvas.line(MARGIN_X, 7.6 * mm, PAGE_W - MARGIN_X, 7.6 * mm)
    canvas.drawString(MARGIN_X, 5.1 * mm, "Cátedra Laznik - usar como disparador, no como respuesta telegráfica")
    canvas.drawRightString(PAGE_W - MARGIN_X, 5.1 * mm, f"{doc.page} / 4")
    canvas.restoreState()


frames = [
    Frame(MARGIN_X, MARGIN_BOTTOM, COL_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0),
]

doc = BaseDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=MARGIN_X,
    rightMargin=MARGIN_X,
    topMargin=MARGIN_TOP,
    bottomMargin=MARGIN_BOTTOM,
    title="Machete de repaso express - tercer parcial",
    author="Guía de estudio Psicoanálisis Freud - Cátedra Laznik",
)
doc.addPageTemplates(PageTemplate(id="single-column", frames=frames, onPage=header_footer))

story = []


def page_title(kicker, title):
    story.append(p(kicker.upper(), style("kicker", fontName="Helvetica-Bold", fontSize=7.1, leading=8, textColor=ACCENT_2, alignment=TA_CENTER, spaceAfter=1)))
    story.append(p(title, H1))


# PAGE 1
page_title("Carilla 1", "MÁS ALLÁ: TRAUMA, SUEÑO Y REPETICIÓN")
story += [
    callout("Regla de respuesta: TESIS -> problema clínico -> mecanismo -> diferencia -> consecuencia."),
    heading("1. Principio del placer y límite"),
    bullet("No todo displacer está más allá: realidad posterga placer; represión produce satisfacción para una moción y displacer para el yo."),
    bullet("Tres referentes heterogéneos: sueño traumático, fort-da y repetición en transferencia."),
    bullet("Lo nuevo: insistencia que no se reconduce a placer para otro sistema."),
    heading("2. Trauma económico"),
    callout("Sorpresa -> falta de preparación -> ruptura antiestímulo -> cantidades no ligadas -> principio del placer abolido transitoriamente -> dominio y ligadura."),
    p("El trauma es el <b>desvalimiento del aparato</b> ante excitación que no puede ligar. La angustia preparatoria habría movilizado investiduras; el terror testimonia que faltó."),
    heading("3. Dos sueños"),
    tbl([
        ["Clásico", "Traumático"],
        ["Deseo reprimido", "Excitación no ligada"],
        ["Condensa, desplaza, figura", "Repite más literalmente"],
        ["Cumple deseo deformado", "No hay deseo reconocible como motor"],
        ["Guardián del dormir", "Terror y despertar"],
    ], widths=[COL_W * 0.5, COL_W * 0.5]),
    p("El sueño traumático intenta producir <b>retroactivamente preparación y ligadura</b>. No elimina la teoría del deseo: revela una tarea anterior al principio del placer."),
    heading("4. Fort-da"),
    bullet("Juego completo: fort + da; pasivo -> activo; el <b>da</b> da placer directo."),
    bullet("Problema: se repite más y también solo el <b>fort</b>, la partida displacentera."),
    bullet("No negar el placer del juego: explicar por qué no alcanza para la insistencia."),
    heading("5. Dos repeticiones"),
    tbl([
        ["Agieren", "Compulsión"],
        ["Actúa lo reprimido", "Insiste lo no ligado"],
        ["Placer mocional/displacer yo", "También fracaso sin placer previo"],
        ["Principio del placer", "Abre un más allá"],
    ], widths=[COL_W * 0.5, COL_W * 0.5]),
    heading("6. Dualismos"),
    bullet("1°: autoconservación (antes 'yoicas') / sexuales."),
    bullet("Narcisismo: libido yoica/de objeto = destinos de libido sexual, no dualismo."),
    bullet("2°: Eros liga y reúne / muerte desliga, repite, restaura estado anterior."),
    heading("7. Masoquismo"),
    bullet("Erógeno primario: resto interior de muerte ligado por libido."),
    bullet("Femenino: fantasías pasivas, infantiles, castigadas."),
    bullet("Moral: satisfacción en padecer -> castigo -> reacción terapéutica negativa."),
]
story.append(PageBreak())

# PAGE 2
page_title("Carilla 2", "SEXUALIDAD, EDIPO Y CASTRACIÓN")
story += [
    heading("1. Organizaciones sexuales"),
    tbl([
        ["Org.", "Operación", "Problema"],
        ["Oral", "incorporar", "dentro/fuera; identificación"],
        ["Sádico-anal", "retener/expulsar", "actividad/pasividad; ambivalencia"],
        ["Fálica", "primado del falo", "fálico/castrado; Edipo"],
        ["Latencia", "represión/diques", "no es fase equivalente"],
        ["Genital", "coordinación postpuberal", "no borra fases previas"],
    ], widths=[COL_W * .20, COL_W * .30, COL_W * .50], font=7.1),
    p("<b>Fijación</b>: libido retenida en una satisfacción. <b>Regresión</b>: retorno a organización, objeto o modo anterior ante conflicto."),
    heading("2. Fase fálica"),
    bullet("Organización genital infantil, no genitalidad adulta."),
    bullet("Premisa universal del pene: inicialmente se supone que todos poseen uno."),
    bullet("Diferencia interpretada como <b>fálico/castrado</b>, no aún masculino/femenino."),
    bullet("Falo organiza tener, perder, dar y faltar; no es mero dato anatómico."),
    heading("3. Asimetría edípica"),
    tbl([
        ["Varón", "Niña"],
        ["Madre objeto; padre rival/identificación", "Ligazón preedípica con madre"],
        ["Amenaza + diferencia = castración posible", "Interpreta perjuicio consumado"],
        ["Castración -> salida/sepultamiento", "Castración -> entrada al Edipo"],
        ["Objetos -> identificaciones -> superyó", "Reproche madre; madre -> padre"],
        ["Salida más definida", "Pene -> hijo; salida menos definida"],
    ], widths=[COL_W * .5, COL_W * .5], font=7.1),
    callout("Tesis: varón = amenaza de pérdida que saca del Edipo. Niña = castración interpretada como consumada que permite entrar."),
    heading("4. Preedípico femenino"),
    p("La madre es primer objeto para ambos. En la niña, la ligazón es larga, intensa y ambivalente. El ingreso al Edipo exige explicar extrañamiento de la madre, cambio de objeto madre -> padre y cambio de zona clítoris -> vagina."),
    heading("5. Pegan a un niño"),
    bullet("1. <b>El padre pega a un niño</b>: rival odiado; 'me ama a mí'."),
    bullet("2. <b>Soy pegado por el padre</b>: ICC, construida; culpa + regresión sádico-anal; castigo y sustituto de ser amado."),
    bullet("3. <b>Los niños son pegados</b>: comunicada; agente impersonal, varios niños, espectador; apariencia sádica, satisfacción masoquista."),
    callout("Análisis: parte de 3, reconstruye 1 y construye 2. Fantasía = cicatriz del Edipo y fijación, no recuerdo material."),
    heading("6. Errores frecuentes"),
    bullet("Anatomía produce directamente posición psíquica."),
    bullet("Fálica = genital adulta; castración afecta igual a ambos."),
    bullet("Niña entra directamente al Edipo con el padre."),
    bullet("Usar 'ser el falo de la madre' sin reconstrucción freudiana."),
]
story.append(PageBreak())

# PAGE 3
page_title("Carilla 3", "SEGUNDA TÓPICA Y RESISTENCIAS")
story += [
    heading("1. Dos tópicas"),
    bullet("1ª: relación de contenidos con conciencia - Icc / Prcc / Cc."),
    bullet("2ª: instancias del conflicto, defensa y satisfacción - ello / yo / superyó."),
    callout("No hay mapeo uno a uno. Todo ello es ICC; no todo ICC es ello: también hay yo y superyó ICC."),
    heading("2. Tercer inconsciente"),
    p("Problema: <b>lo reprimido busca retornar</b>, por eso no puede ser la fuerza que resiste. La resistencia parte del yo sin que el paciente lo sepa -> parte del yo es ICC."),
    tbl([
        ["Descriptivo", "Dinámico", "Estructural"],
        ["no Cc ahora; latente puede devenir", "reprimido por una fuerza; retorna deformado", "no necesariamente reprimido; atraviesa instancias"],
    ], widths=[COL_W/3]*3, font=7),
    callout("Todo lo reprimido es ICC; no todo ICC es reprimido. La segunda tópica complementa, no elimina, la primera."),
    heading("3. Instancias"),
    bullet("<b>Ello:</b> todo ICC; sede pulsional; libido; reprimido + nunca reprimido; procesos no ligados."),
    bullet("<b>Yo:</b> parte del ello modificada por realidad; corporal; síntesis, palabra, motilidad; parte ICC; almácigo de angustia."),
    bullet("<b>Superyó:</b> heredero del Edipo + identificaciones tempranas; ley/ideal y mandato cruel; afinidad con ello."),
    heading("4. Potencia, endeblez y vasallajes"),
    p("<b>Potencia:</b> liga, sintetiza, prueba realidad, gobierna motilidad, produce señal y defensa. <b>Endeblez:</b> toma energía del ello, no es soberano y media exigencias incompatibles."),
    tbl([
        ["Amo", "Exigencia", "Angustia"],
        ["Mundo", "realidad/peligro", "realista"],
        ["Ello", "pulsional", "neurótica"],
        ["Superyó", "ideal/castigo", "conciencia moral"],
    ], widths=[COL_W*.25, COL_W*.43, COL_W*.32], font=7),
    heading("5. Cinco resistencias"),
    tbl([
        ["Inst.", "Resistencia", "Clave"],
        ["Yo", "represión", "contrainvestidura mantiene apartado"],
        ["Yo", "transferencia", "conflicto actuado; erótica/hostil"],
        ["Yo", "ganancia secundaria", "ventajas agregadas al síntoma"],
        ["Ello", "compulsión", "vías insisten; reelaborar"],
        ["Superyó", "castigo", "culpa ICC; reacción negativa"],
    ], widths=[COL_W*.17, COL_W*.31, COL_W*.52], font=6.9),
    p("Interpretar ayuda especialmente con resistencias yoicas, pero no las levanta automáticamente. Ello y superyó no ceden sólo haciendo consciente una representación."),
    heading("6. No confundir"),
    bullet("Ganancia primaria = satisfacción pulsional <i>en</i> síntoma. Secundaria = ventajas <i>con</i> síntoma ya formado."),
    bullet("Culpa Cc != necesidad ICC de castigo: puede sentirse enfermo, no culpable."),
    bullet("Transferencia tierna puede ser motor; erótica/hostil, obstáculo."),
]
story.append(PageBreak())

# PAGE 4
page_title("Carilla 4", "ANGUSTIA Y ARTICULACIONES")
story += [
    heading("1. Tres teorías de angustia"),
    tbl([
        ["Versión", "Fórmula", "Clave"],
        ["1ª", "excitación sexual somática no elaborada -> angustia", "neurosis actuales; sin represión"],
        ["2ª", "libido afectada por represión -> angustia", "angustia producto"],
        ["3ª", "peligro -> señal -> defensa/represión -> síntoma", "angustia causa represión"],
    ], widths=[COL_W*.13, COL_W*.51, COL_W*.36], font=6.8),
    heading("2. Automática y señal"),
    tbl([
        ["Automática", "Señal"],
        ["situación traumática efectiva", "anticipa condición de peligro"],
        ["yo desbordado; desvalimiento", "pequeña reproducción por el yo"],
        ["cantidad no ligada; pasiva", "moviliza defensa"],
    ], widths=[COL_W*.5, COL_W*.5], font=7.1),
    p("Serie: desvalimiento económico -> pérdida del objeto -> castración -> pérdida del amor del superyó. Núcleo: separación + riesgo de desborde."),
    heading("3. Hans"),
    callout("Mociones edípicas -> peligro de castración -> angustia-señal -> represión -> caballo -> fobia. Convierte peligro interno inevitable en objeto externo evitable; precio: inhibición."),
    heading("4. Articulaciones de alta frecuencia"),
    bullet("<b>Sueños:</b> deseo/trabajo/guardián -> trauma no ligado/repetición/ligadura previa."),
    bullet("<b>Trauma:</b> afecto no abreaccionado -> VSPT, dos tiempos y realidad psíquica -> sorpresa, ruptura y no ligadura."),
    bullet("<b>Repetición:</b> agieren/retorno reprimido -> compulsión/no ligado -> resistencia del ello/reelaboración."),
    bullet("<b>Tópicas:</b> Icc-Prcc-Cc describe conciencia -> yo-ello-superyó localiza instancias y resistencias."),
    bullet("<b>Edipo-superyó:</b> sepultamiento -> objetos abandonados -> identificaciones -> superyó; crueldad excede ley."),
    bullet("<b>Masoquismo-resistencia:</b> resto de muerte ligado -> primario -> moral -> castigo -> superyó -> reacción negativa."),
    bullet("<b>Trauma-angustia:</b> desvalimiento/no ligadura -> automática; peligro anticipado -> señal -> defensa."),
    heading("5. Frases de cierre"),
    bullet("La reformulación no elimina lo anterior: muestra su límite y agrega una tarea más originaria."),
    bullet("Articular no es identificar: se conserva X, cambia Y y la consecuencia es Z."),
    bullet("La segunda tópica no sustituye a la primera: redistribuye lo ICC entre instancias."),
    bullet("La interpretación conserva valor, pero no basta ante ello y superyó."),
    heading("6. Errores frecuentes"),
    p("Todo displacer = más allá. Represión = ligadura. Sueño traumático totalmente ininterpretable. Pulsiones yoicas = libido yoica. Ello = antiguo Icc. Yo = Cc. Automática = señal. Satisfacción sintomática = ganancia secundaria. Interpretar levanta toda resistencia."),
    heading("7. Antes de entregar"),
    callout("¿Definí problema? ¿Ubiqué texto/momento? ¿Expliqué mecanismo? ¿Marqué diferencia? ¿Respondí todos los verbos? ¿Cerré retomando tesis?"),
]

doc.build(story)
print(OUT)

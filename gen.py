#!/usr/bin/env python3
# BringGo blog: yaziya ozel, dark-mode uyumlu SVG infografik ureteci.
import html, os, re

W=720; PADX=28; CX=28; CW=664
STYLE='''<style>
text{font-family:Arial,Helvetica,sans-serif}
.card{fill:#ffffff;stroke:#e4ebe7;stroke-width:1.5}
.row{fill:#f5f8f7}.pill{fill:#E1F5EE}.hi{fill:#1f9d5f}.mut{fill:#eef1f0}
.acc{fill:#12876A}.circ{fill:#12876A}.rd{fill:#fbe9e7}.am{fill:#fbf1dd}.tl{fill:#E1F5EE}.ln{stroke:#dbe6e1}
.tt{fill:#0F3D33;font-weight:bold}.ts{fill:#5b6b66}.tl2{fill:#22332f}
.tv{fill:#0F6E56;font-weight:bold}.tm{fill:#5b6b66;font-weight:bold}.tw{fill:#ffffff;font-weight:bold}
.tf{fill:#8a9691}.tb{fill:#12876A;font-weight:bold}.big{fill:#0F3D33;font-weight:bold}
.trd{fill:#a3392c;font-weight:bold}.tam{fill:#8a5a12;font-weight:bold}.ttl{fill:#0F6E56;font-weight:bold}
@media (prefers-color-scheme:dark){
.card{fill:#16211e;stroke:#2c3a35}
.row{fill:#1d2b27}.pill{fill:#123a2e}.hi{fill:#1f9d5f}.mut{fill:#28352f}
.acc{fill:#2fae7e}.circ{fill:#2fae7e}.rd{fill:#3a201c}.am{fill:#352a15}.tl{fill:#123a2e}
.tt{fill:#d7f2e6}.ts{fill:#8fa79d}.tl2{fill:#cfe0d9}
.tv{fill:#6fe0b0}.tm{fill:#9db3a9}.tw{fill:#ffffff}
.tf{fill:#6d8279}.tb{fill:#57d3a3}.big{fill:#d7f2e6}
.trd{fill:#f0a99e}.tam{fill:#e6c281}.ttl{fill:#6fe0b0}.ln{stroke:#31423c}}
</style>'''

def esc(s): return html.escape(str(s), quote=True)
def _capw(m):
    w=m.group(0); i=m.start()
    if i>0 and m.string[i-1] in "'’ʼ`": return w  # Turkce ek (Meksika'ya, ABD'den) buyutulmez
    if w.isupper() or any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w): return w
    f=w[0]; f='İ' if f=='i' else f.upper()
    return f+w[1:]
def titlecase(s): return re.sub(r"[A-Za-zÀ-ÿğıİşçöüĞŞÇÖÜ]+", _capw, s)

def wrap(title, sub, inner, ch):
    # dikey ritim: ust padding ~ alt padding. Icerik 88'de baslar; kaynak satiri icerikten sonra 44px bosluk.
    fy=88+ch+44        # kaynak satiri temel cizgisi
    H=fy+24            # alt padding
    p=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img">'%(W,H,W,H)]
    p.append('<title>%s</title>'%esc(title)); p.append(STYLE)
    p.append('<rect x="1" y="1" width="%d" height="%d" rx="18" class="card"/>'%(W-2,H-2))
    p.append('<rect x="28" y="28" width="4" height="28" rx="2" class="acc"/>')
    p.append('<text x="44" y="45" font-size="21" class="tt">%s</text>'%esc(title))
    p.append('<text x="44" y="67" font-size="13" class="ts">%s</text>'%esc(sub))
    p.append('<g transform="translate(0,88)">%s</g>'%inner)
    p.append('<text x="28" y="%d" font-size="11.5" class="tf">%s</text>'%(fy, esc(SRC)))
    p.append('<text x="%d" y="%d" text-anchor="end" font-size="12" class="tb">BringGo Ship</text>'%(W-28,fy))
    p.append('</svg>')
    return ''.join(p)

SRC="Kaynak: SAT · DOF · trade.gov · 2026"

# --- sablonlar: (inner_svg, content_height) dondurur ---
def costlist(rows):
    h=[]; y=0
    for label,val,kind in rows:
        cls='hi' if kind=='hi' else ('mut' if kind=='mut' else 'pill')
        tcls='tw' if kind=='hi' else ('tm' if kind=='mut' else 'tv')
        h.append('<rect x="28" y="%d" width="664" height="40" rx="10" class="%s"/>'%(y, 'row' if kind=='n' else 'row'))
        h.append('<text x="46" y="%d" font-size="15" class="tl2">%s</text>'%(y+25, esc(label)))
        h.append('<rect x="480" y="%d" width="200" height="24" rx="12" class="%s"/>'%(y+8, cls))
        h.append('<text x="580" y="%d" text-anchor="middle" font-size="13" class="%s">%s</text>'%(y+25, tcls, esc(val)))
        y+=48
    return ''.join(h), y-8

def carriers(rows):
    h=[]; y=0
    for name,strength,use in rows:
        h.append('<rect x="28" y="%d" width="664" height="46" rx="10" class="row"/>'%y)
        h.append('<text x="46" y="%d" font-size="15" class="tl2" font-weight="bold">%s</text>'%(y+20, esc(name)))
        h.append('<text x="46" y="%d" font-size="12" class="ts">%s</text>'%(y+38, esc(strength)))
        h.append('<rect x="470" y="%d" width="210" height="24" rx="12" class="pill"/>'%(y+11))
        h.append('<text x="575" y="%d" text-anchor="middle" font-size="12" class="tv">%s</text>'%(y+28, esc(use)))
        y+=54
    return ''.join(h), y-8

def statusrows(rows):
    # rows: (item, statustext, statuskind[pro/res/lbl], authority)
    h=[]; y=0
    for item,st,kind,auth in rows:
        sc={'pro':'rd','res':'am','lbl':'tl'}[kind]; tc={'pro':'trd','res':'tam','lbl':'ttl'}[kind]
        h.append('<rect x="28" y="%d" width="664" height="44" rx="10" class="row"/>'%y)
        h.append('<text x="46" y="%d" font-size="14.5" class="tl2">%s</text>'%(y+27, esc(item)))
        h.append('<rect x="392" y="%d" width="132" height="22" rx="11" class="%s"/>'%(y+11, sc))
        h.append('<text x="458" y="%d" text-anchor="middle" font-size="12" class="%s">%s</text>'%(y+27, tc, esc(st)))
        h.append('<text x="676" y="%d" text-anchor="end" font-size="12" class="ts">%s</text>'%(y+27, esc(auth)))
        y+=52
    return ''.join(h), y-8

def stepflow(steps):
    h=[]; y=18; n=len(steps); step=56
    # baglanti cizgisi
    h.append('<line x1="46" y1="%d" x2="46" y2="%d" stroke-width="2" class="ln"/>'%(18, 18+(n-1)*step))
    for i,(label,sub) in enumerate(steps):
        cy=y+i*step
        h.append('<circle cx="46" cy="%d" r="15" class="circ"/>'%cy)
        h.append('<text x="46" y="%d" text-anchor="middle" font-size="13" class="tw">%d</text>'%(cy+5, i+1))
        h.append('<text x="76" y="%d" font-size="15.5" class="tl2" font-weight="bold">%s</text>'%(cy-2, esc(label)))
        h.append('<text x="76" y="%d" font-size="12.5" class="ts">%s</text>'%(cy+16, esc(sub)))
    return ''.join(h), 18+(n-1)*step+18

def stats(figs, note=""):
    h=[]; nf=len(figs); colw=CW/nf
    for i,(val,lab) in enumerate(figs):
        cx=28+colw*i+colw/2
        h.append('<text x="%.0f" y="50" text-anchor="middle" font-size="26" class="big">%s</text>'%(cx, esc(val)))
        h.append('<text x="%.0f" y="76" text-anchor="middle" font-size="13" class="ts">%s</text>'%(cx, esc(lab)))
        if i>0:
            h.append('<line x1="%.0f" y1="24" x2="%.0f" y2="82" stroke-width="1" class="ln"/>'%(28+colw*i,28+colw*i))
    hh=104
    if note:
        h.append('<rect x="28" y="%d" width="664" height="34" rx="10" class="pill"/>'%hh)
        h.append('<text x="360" y="%d" text-anchor="middle" font-size="13" class="tv">%s</text>'%(hh+22, esc(note))); hh+=42
    return ''.join(h), hh

def compare2(colA, colB, rows, winB=True):
    h=[]; xa=398; xb=574; y=0
    h.append('<text x="%d" y="16" text-anchor="middle" font-size="14.5" class="tl2" font-weight="bold">%s</text>'%(xa, esc(colA)))
    h.append('<text x="%d" y="16" text-anchor="middle" font-size="14.5" class="tb" font-weight="bold">%s</text>'%(xb, esc(colB)))
    h.append('<line x1="28" y1="28" x2="692" y2="28" stroke-width="1" class="ln"/>')
    y=40
    for factor,a,b in rows:
        h.append('<rect x="28" y="%d" width="664" height="38" rx="9" class="row"/>'%y)
        h.append('<text x="46" y="%d" font-size="13.5" class="ts">%s</text>'%(y+24, esc(factor)))
        h.append('<text x="%d" y="%d" text-anchor="middle" font-size="13.5" class="tl2">%s</text>'%(xa, y+24, esc(a)))
        h.append('<text x="%d" y="%d" text-anchor="middle" font-size="13.5" class="tv" font-weight="bold">%s</text>'%(xb, y+24, esc(b)))
        y+=44
    return ''.join(h), y-6

def decision(cols):
    h=[]; n=len(cols); gap=14; cw=(CW-(n-1)*gap)/n
    for i,(label,desc) in enumerate(cols):
        x=28+i*(cw+gap)
        h.append('<rect x="%.0f" y="0" width="%.0f" height="118" rx="12" class="row"/>'%(x,cw))
        h.append('<circle cx="%.0f" cy="30" r="13" class="circ"/>'%(x+cw/2))
        h.append('<text x="%.0f" y="35" text-anchor="middle" font-size="14" class="tw">%d</text>'%(x+cw/2, i+1))
        h.append('<text x="%.0f" y="66" text-anchor="middle" font-size="14.5" class="tl2" font-weight="bold">%s</text>'%(x+cw/2, esc(label)))
        # desc wrap (2 satir)
        words=desc.split(' '); line1=[]; line2=[]; cur=line1
        for w in words:
            if cur is line1 and len(' '.join(line1+[w]))>22: cur=line2
            cur.append(w)
        h.append('<text x="%.0f" y="88" text-anchor="middle" font-size="12" class="ts">%s</text>'%(x+cw/2, esc(' '.join(line1))))
        if line2: h.append('<text x="%.0f" y="105" text-anchor="middle" font-size="12" class="ts">%s</text>'%(x+cw/2, esc(' '.join(line2))))
    return ''.join(h), 118

# ================= VERI (30 yazi) =================
D = {
"how-cross-border-shipping-mexico-works": ("How US to Mexico shipping works","US to Mexico · 5 steps","step",[("Leave US warehouse","Documents checked"),("US export","Formalities"),("Border transfer","Drayage"),("Customs clearance","Pedimento · light"),("Delivery","Monterrey 1-2 days")]),
"mexico-customs-clearance-process": ("Mexican customs clearance","5 steps at the border","step",[("Classify goods","HS codes"),("File pedimento","Pay duty + 16% IVA"),("Customs light","Green or red"),("Inspection if red","Adds 1-2 days"),("Release","To delivery")]),
"cost-to-ship-to-mexico": ("What it costs to ship to Mexico","Fiscal cost components · 2026","cost",[("Customs broker","3,500-15,000 MXN","n"),("Duty · US origin (USMCA)","0% · USMCA","hi"),("IVA (VAT)","16%","n"),("DTA · customs fee (USMCA)","~362 MXN","n"),("Prevalidation","~238 MXN","n"),("Freight (LTL / FTL)","Varies · quote","mut")]),
"how-to-sell-amazon-mexico-from-us": ("Selling on Amazon Mexico: NARF vs FBA","Two ways from the US","cmp",("NARF","FBA Mexico",[("Inventory","US","In Mexico"),("Who imports","Customer","You, bulk"),("RFC needed","No","Yes"),("Delivery","5-9 days","Local Prime"),("Per-unit fee","Higher","Lower"),("Best for","Testing","Steady volume")])),
"cuanto-cuesta-importar-eeuu-mexico": ("Cuánto cuesta importar a México","Componentes del costo fiscal · 2026","cost",[("Agente aduanal","3.500-15.000 MXN","n"),("Arancel · origen EE.UU. (T-MEC)","0% · T-MEC","hi"),("IVA","16%","n"),("DTA · derecho de trámite","~362 MXN","n"),("Prevalidación","~238 MXN","n"),("Flete (LTL / FTL)","Variable · cotización","mut")]),
"productos-prohibidos-importar-mexico": ("Qué no puedes importar a México","Prohibido · restringido · 2026","status",[("Vapeadores y cigarros electrónicos","Prohibido","pro","Reforma 2026"),("Ropa y calzado usados","Prohibido","pro","SAT · ANAM"),("Armas y municiones","Restringido","res","SEDENA"),("Alimentos y agropecuarios","Restringido","res","SENASICA"),("Medicamentos y cosméticos","Restringido","res","COFEPRIS"),("Mayoría de retail","Etiqueta NOM","lbl","NOM-050/051")]),
"nearshoring-mexico-beneficios": ("Nearshoring en México","Inversión extranjera directa · 2026","stat",[("~$41 B","IED en 2025"),("$23,6 B","Récord 1T 2026"),("~58%","es nearshoring")],"Origen EE.UU. entra con 0% de arancel bajo el T-MEC"),
"abd-meksika-sinir-otesi-lojistik": ("ABD-Meksika sınır ötesi lojistik","ABD'den Meksika'ya · 5 adım","step",[("ABD deposundan çıkış","Belgeler kontrol"),("ABD ihracatı","Formaliteler"),("Sınır transferi","Drayage"),("Gümrükleme","Pedimento · ışık"),("Teslimat","Monterrey 1-2 gün")]),
"amazon-meksika-satis-rehberi": ("NARF mı FBA Meksika mı?","ABD'den iki satış yolu","cmp",("NARF","FBA Meksika",[("Stok","ABD'de","Meksika'da"),("İthalatçı","Müşteri","Siz, toplu"),("RFC gerekir","Hayır","Evet"),("Teslimat","5-9 gün","Yerel Prime"),("Birim ücret","Yüksek","Düşük"),("En uygun","Test","Düzenli hacim")])),
"meksika-pazarina-giris-rehberi": ("Meksika pazarına giriş","Yol haritası · 4 adım","step",[("Kanal seç","Amazon / ML / B2B"),("Yasal kurulum","RFC + gümrük müşaviri"),("Lojistik","ABD'de konsolidasyon"),("Fiyatlama","IVA + rekabet")]),
"cross-border-returns-mexico-guide": ("Handling a return from Mexico","One of three paths","dec",[("Restock in Mexico","Resaleable back to local stock"),("Return to US","Held and shipped in a batch"),("Dispose locally","Damaged or low value items")]),
"border-warehouse-fulfillment-laredo-monterrey": ("Border warehousing","Laredo + Monterrey corridor","step",[("Laredo (US side)","Consolidate + prep"),("Cross border","One pedimento"),("Customs","Broker clears"),("Monterrey (MX side)","Fulfill orders"),("Deliver","Local + returns")]),
"dropshipping-mexico-from-us-guide": ("Dropshipping to Mexico: two models","Direct parcel vs border warehouse","cmp",("Direct parcel","Border warehouse",[("Customs","Per order","Once, bulk"),("Delivery","Days to a week","Fast local"),("Per-order cost","Ship + tax","Cheap local"),("Setup","Low","Bulk import"),("Returns","Hard","Local"),("Best for","Testing","Steady volume")])),
"nearshoring-mexico-full-guide": ("Nearshoring to Mexico","Investment & incentives · 2026","stat",[("~$41B","FDI in 2025"),("$23.6B","Record Q1 2026"),("41-91%","Plan Mexico deduction")],"US-origin goods enter the US at 0% under the USMCA"),
"vender-amazon-mexico-desde-eeuu": ("NARF o FBA México","Vender en Amazon México desde EE.UU.","cmp",("NARF","FBA México",[("Inventario","En EE.UU.","En México"),("Quién importa","El cliente","Tú, a granel"),("RFC","No","Sí"),("Entrega","5-9 días","Prime local"),("Tarifa unidad","Mayor","Menor"),("Ideal para","Probar","Volumen")])),
"que-es-fulfillment-mexico": ("Cómo funciona el fulfillment","5 pasos","step",[("Recepción","Inventario"),("Almacenamiento","Organizado"),("Pick & pack","Por pedido"),("Envío","Transportista"),("Devoluciones","Local")]),
"dropshipping-eeuu-mexico": ("Dropshipping a México: dos modelos","Envío directo vs almacén en frontera","cmp",("Envío directo","Almacén frontera",[("Aduana","Por pedido","Una vez, granel"),("Entrega","Días a semana","Rápida local"),("Costo/pedido","Envío + impuesto","Local barato"),("Arranque","Bajo","Importar granel"),("Devoluciones","Difícil","Local"),("Ideal para","Probar","Volumen")])),
"meksika-dropshipping-rehberi": ("Meksika'ya dropshipping: iki model","Doğrudan kargo vs sınır deposu","cmp",("Doğrudan kargo","Sınır deposu",[("Gümrük","Sipariş başına","Bir kez, toplu"),("Teslimat","Günler-hafta","Hızlı yerel"),("Sipariş maliyeti","Kargo + vergi","Ucuz yerel"),("Kurulum","Düşük","Toplu ithalat"),("İadeler","Zor","Yerel"),("En uygun","Test","Hacim")])),
"meksika-iade-yonetimi": ("Meksika'da iade edilen ürün","Üç yoldan biri","dec",[("Meksika'da yeniden stok","Satılabilirse yerel stoğa"),("ABD'ye dönüş","Partiyle birleştirilir"),("Yerel imha","Hasarlı veya düşük değer")]),
"meksika-son-mil-teslimat": ("Meksika son mil kargo firmaları","Karşılaştırma · 2026","carrier",[("Estafeta","40+ yıl, geniş ulusal kapsam","Genel e-ticaret"),("Paquetexpress","30+ yıl, 180+ nokta","Güvenli teslimat"),("DHL Express","Hız, uluslararası, takip","Ekspres"),("FedEx","89 istasyon, 3.000+ araç","Ülke geneli"),("99 Minutos","Aynı gün, 99 dk","Şehir içi hız"),("Correos de México","Ulusal posta","Ekonomik / kırsal")]),
"restricted-products-shipping-mexico": ("What you can't ship to Mexico","Prohibited · restricted · 2026","status",[("Vapes and e-cigarettes","Prohibited","pro","2026 reform"),("Used clothing (commercial)","Prohibited","pro","SAT · ANAM"),("Weapons and ammunition","Restricted","res","SEDENA"),("Food and agricultural goods","Restricted","res","SENASICA"),("Medicines and cosmetics","Restricted","res","COFEPRIS"),("Most retail products","NOM label","lbl","NOM-050/051")]),
"selling-online-to-mexico-guide": ("Selling online to Mexico","Market entry · 4 steps","step",[("Choose a channel","Amazon / ML / B2B"),("Legal setup","RFC + customs broker"),("Logistics","Consolidate in the US"),("Pricing","IVA + competition")]),
"last-mile-delivery-mexico-guide": ("Mexico last-mile carriers","Comparison · 2026","carrier",[("Estafeta","40+ years, wide coverage","General e-commerce"),("Paquetexpress","30+ years, 180+ points","Secure delivery"),("DHL Express","Speed, international","Express"),("FedEx","89 stations, 3,000+ vehicles","Nationwide"),("99 Minutos","Same day, under 99 min","City speed"),("Correos de Mexico","National post","Economy / rural")]),
"amazon-narf-vs-fba-mexico": ("Amazon NARF vs FBA Mexico","The decision framework","cmp",("NARF","FBA Mexico",[("Inventory","US warehouses","In Mexico"),("Who imports","Customer","You, bulk"),("RFC needed","No","Yes"),("Delivery","5-9 days","Local Prime"),("Per-unit fee","Higher","Lower"),("Taxes","At checkout","On bulk import")])),
"logistica-inversa-devoluciones-mexico": ("Una devolución desde México","Uno de tres caminos","dec",[("Reingresar en México","Vendible al stock local"),("Regresar a EE.UU.","En un lote consolidado"),("Desechar localmente","Dañado o de bajo valor")]),
"vender-en-estados-unidos-desde-mexico": ("Vender en EE.UU. desde México","Hoja de ruta · 4 pasos","step",[("Elige un canal","Amazon USA / B2B"),("Aduana CBP","T-MEC · origen mexicano"),("Logística","Almacén en EE.UU."),("Precio","Aranceles + canal")]),
"vender-mercado-libre-guia": ("Mercado Envíos vs Full","Logística en Mercado Libre","cmp",("Mercado Envíos","Envíos Full",[("Inventario","Tú lo guardas","En centros ML"),("Preparación","Tú","Mercado Libre"),("Entrega","Estándar","Más rápida"),("Posición","Normal","Favorecida"),("Stock local","No","Sí")])),
"nearshoring-meksika-turk-firmalari": ("Nearshoring ve Meksika","Yatırım ve teşvikler · 2026","stat",[("41 milyar $","2025 DYY"),("23,6 milyar $","2026 1Ç rekor"),("%41-91","Plan México")],"Meksika menşeli üretim, ABD'ye T-MEC ile %0 tarifeyle girer"),
"meksika-yasakli-urunler": ("Meksika'ya gönderilemeyenler","Yasaklı · kısıtlı · 2026","status",[("Vape ve elektronik sigara","Yasaklı","pro","2026 reformu"),("Kullanılmış giysi (ticari)","Yasaklı","pro","SAT · ANAM"),("Silah ve mühimmat","Kısıtlı","res","SEDENA"),("Gıda ve tarım ürünleri","Kısıtlı","res","SENASICA"),("İlaç ve kozmetik","Kısıtlı","res","COFEPRIS"),("Çoğu perakende ürün","NOM etiketi","lbl","NOM-050/051")]),
"meksika-gonderim-maliyeti": ("Meksika'ya gönderim maliyeti","Mali maliyet kalemleri · 2026","cost",[("Gümrük müşaviri","3.500-15.000 MXN","n"),("Gümrük vergisi · ABD menşe","%0 · USMCA","hi"),("IVA (KDV)","%16","n"),("DTA · işlem harcı (T-MEC)","~362 MXN","n"),("Prevalidación","~238 MXN","n"),("Navlun (LTL / FTL)","Değişken · teklif","mut")]),
}

OUT=os.path.dirname(os.path.abspath(__file__))
count=0
for slug,entry in D.items():
    title,sub,kind=titlecase(entry[0]),entry[1],entry[2]
    if kind=="cost": inner,ch=costlist(entry[3])
    elif kind=="carrier": inner,ch=carriers(entry[3])
    elif kind=="status": inner,ch=statusrows(entry[3])
    elif kind=="step": inner,ch=stepflow(entry[3])
    elif kind=="stat": inner,ch=stats(entry[3], entry[4] if len(entry)>4 else "")
    elif kind=="cmp": inner,ch=compare2(entry[3][0],entry[3][1],entry[3][2])
    elif kind=="dec": inner,ch=decision(entry[3])
    else: continue
    svg=wrap(title,sub,inner,ch)
    open(os.path.join(OUT,slug+".svg"),"w").write(svg)
    count+=1
print("uretildi:",count,"SVG")

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
TR_SLUGS={"abd-meksika-sinir-otesi-lojistik","amazon-meksika-satis-rehberi","meksika-pazarina-giris-rehberi","meksika-iade-yonetimi","meksika-son-mil-teslimat","meksika-dropshipping-rehberi","meksika-yasakli-urunler","nearshoring-meksika-turk-firmalari","meksika-gonderim-maliyeti","amazon-mx-fba-gonderi","mercado-libre-nedir-rehber","laredo-monterrey-depo-fulfillment","meksika-depo-ucretleri","amazon-meksika-q4-takvimi","meksika-sat-cfdi","hibrit-dropshipping","amazon-meksika-mi-amerika-mi","usmca-tmec-2026-gozden-gecirme","meksika-adres-sistemi","mercado-libre-mi-amazon-mi","meksikada-uretim-vs-ihracat","nom-004-tekstil","laredo-depo-hizmeti","abdden-meksikaya-kargo","amazon-meksika-fbm","palet-basina-maliyet-senaryo","meksika-gumruk-vergisi-ne-kadar","meksika-elektronik-deger-beyani"}
def titlecase(s, tr=False):
    def cap(m):
        w=m.group(0); i=m.start()
        if i>0 and m.string[i-1] in "'’ʼ`": return w  # Turkce ek (Meksika'ya) buyutulmez
        if w.isupper() or any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w): return w
        f=w[0]
        if f=='i': f='İ' if tr else 'I'   # TR: i->İ, ES/EN: i->I
        else: f=f.upper()
        return f+w[1:]
    return re.sub(r"[A-Za-zÀ-ÿğıİşçöüĞŞÇÖÜ]+", cap, s)

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
"meksika-son-mil-teslimat": ("Meksika son mil kargo firmaları","Karşılaştırma · 2026","carrier",[("Estafeta","40+ yıl, geniş ulusal kapsam","Genel e-ticaret"),("Paquetexpress","~40 yıl (1986), ulusal ağ","Güvenli teslimat"),("DHL Express","Hız, uluslararası, takip","Ekspres"),("FedEx","83 istasyon, 3.000+ araç","Ülke geneli"),("99 Minutos","Aynı gün, 99 dk","Şehir içi hız"),("Correos de México","Ulusal posta","Ekonomik / kırsal")]),
"restricted-products-shipping-mexico": ("What you can't ship to Mexico","Prohibited · restricted · 2026","status",[("Vapes and e-cigarettes","Prohibited","pro","2026 reform"),("Used clothing (commercial)","Prohibited","pro","SAT · ANAM"),("Weapons and ammunition","Restricted","res","SEDENA"),("Food and agricultural goods","Restricted","res","SENASICA"),("Medicines and cosmetics","Restricted","res","COFEPRIS"),("Most retail products","NOM label","lbl","NOM-050/051")]),
"selling-online-to-mexico-guide": ("Selling online to Mexico","Market entry · 4 steps","step",[("Choose a channel","Amazon / ML / B2B"),("Legal setup","RFC + customs broker"),("Logistics","Consolidate in the US"),("Pricing","IVA + competition")]),
"last-mile-delivery-mexico-guide": ("Mexico last-mile carriers","Comparison · 2026","carrier",[("Estafeta","40+ years, wide coverage","General e-commerce"),("Paquetexpress","~40 years (1986), national","Secure delivery"),("DHL Express","Speed, international","Express"),("FedEx","83 stations, 3,000+ vehicles","Nationwide"),("99 Minutos","Same day, under 99 min","City speed"),("Correos de Mexico","National post","Economy / rural")]),
"amazon-narf-vs-fba-mexico": ("Amazon NARF vs FBA Mexico","The decision framework","cmp",("NARF","FBA Mexico",[("Inventory","US warehouses","In Mexico"),("Who imports","Customer","You, bulk"),("RFC needed","No","Yes"),("Delivery","5-9 days","Local Prime"),("Per-unit fee","Higher","Lower"),("Taxes","At checkout","On bulk import")])),
"logistica-inversa-devoluciones-mexico": ("Una devolución desde México","Uno de tres caminos","dec",[("Reingresar en México","Vendible al stock local"),("Regresar a EE.UU.","En un lote consolidado"),("Desechar localmente","Dañado o de bajo valor")]),
"vender-en-estados-unidos-desde-mexico": ("Vender en EE.UU. desde México","Hoja de ruta · 4 pasos","step",[("Elige un canal","Amazon USA / B2B"),("Aduana CBP","T-MEC · origen mexicano"),("Logística","Almacén en EE.UU."),("Precio","Aranceles + canal")]),
"vender-mercado-libre-guia": ("Mercado Envíos vs Full","Logística en Mercado Libre","cmp",("Mercado Envíos","Envíos Full",[("Inventario","Tú lo guardas","En centros ML"),("Preparación","Tú","Mercado Libre"),("Entrega","Estándar","Más rápida"),("Posición","Normal","Favorecida"),("Stock local","No","Sí")])),
"nearshoring-meksika-turk-firmalari": ("Nearshoring ve Meksika","Yatırım ve teşvikler · 2026","stat",[("41 milyar $","2025 DYY"),("23,6 milyar $","2026 1Ç rekor"),("%41-91","Plan México")],"Meksika menşeli üretim, ABD'ye T-MEC ile %0 tarifeyle girer"),
"meksika-yasakli-urunler": ("Meksika'ya gönderilemeyenler","Yasaklı · kısıtlı · 2026","status",[("Vape ve elektronik sigara","Yasaklı","pro","2026 reformu"),("Kullanılmış giysi (ticari)","Yasaklı","pro","SAT · ANAM"),("Silah ve mühimmat","Kısıtlı","res","SEDENA"),("Gıda ve tarım ürünleri","Kısıtlı","res","SENASICA"),("İlaç ve kozmetik","Kısıtlı","res","COFEPRIS"),("Çoğu perakende ürün","NOM etiketi","lbl","NOM-050/051")]),
"meksika-gonderim-maliyeti": ("Meksika'ya gönderim maliyeti","Mali maliyet kalemleri · 2026","cost",[("Gümrük müşaviri","3.500-15.000 MXN","n"),("Gümrük vergisi · ABD menşe","%0 · USMCA","hi"),("IVA (KDV)","%16","n"),("DTA · işlem harcı (T-MEC)","~362 MXN","n"),("Prevalidación","~238 MXN","n"),("Navlun (LTL / FTL)","Değişken · teklif","mut")]),
"mexican-parcel-carriers-comparison": ("Mexican parcel carriers compared","Coverage and best fit · 2026","carrier",[("Estafeta","40+ years, ~95% territory","National ground"),("Paquetexpress","~40 years (1986), national","E-commerce ground"),("FedEx","83 stations, 3,000+ vehicles","Speed, hard addresses"),("DHL Express","International, real-time tracking","Fast express"),("99 Minutos","70+ cities, same-day","City core")]),
"paqueterias-mexico-comparativa": ("Paqueterías en México comparadas","Cobertura y uso ideal · 2026","carrier",[("Estafeta","40+ años, ~95% territorio","Terrestre nacional"),("Paquetexpress","~40 años (1986), red nacional","E-commerce terrestre"),("FedEx","83 estaciones, 3.000+ vehículos","Velocidad"),("DHL Express","Internacional, rastreo","Exprés rápida"),("99 Minutos","70+ ciudades, mismo día","Núcleo urbano")]),
"ship-pallet-texas-mexico-cost": ("Cost to ship a pallet to Mexico","Cost lines · 2026","cost",[("LTL freight (1 pallet)","~$350-800","n"),("FTL freight","Near/below $2 per mile","mut"),("Customs broker","A few thousand MXN","n"),("Duty · US origin (USMCA)","0% · USMCA","hi"),("IVA (VAT)","16%","n"),("Border transfer","Varies · quote","mut")]),
"mercado-libre-nedir-rehber": ("Mercado Libre satıcı maliyeti","Katmanlar · 2026","cost",[("Satış komisyonu","Kategoriye göre","n"),("Mercado Envíos Full","Depolama + gönderi","mut"),("İthalat IVA","%16","n"),("Gümrük · ABD menşe","%0 · USMCA","hi"),("Reklam (Mercado Ads)","İsteğe bağlı","mut")]),
"meksika-depo-ucretleri": ("Meksika depo ücret kalemleri","Fiyat temeli · 2026","cost",[("Depolama","Palet/m² · aylık","n"),("Elleçleme (giriş/çıkış)","Birim/sevkiyat","mut"),("Kabul ve sayım","TIR başına","n"),("Sipariş işleme","Sipariş/kalem","mut"),("Katma değer","Kitting, NOM etiket","mut")]),
"how-to-choose-customs-broker-mexico": ("Choosing a customs broker","Red flag vs good sign","cmp",("Red flag","Good sign",[("Fees","Opaque lump sum","Itemized"),("License","Cannot show","Active patente"),("References","None","On your lane"),("2026 rules","Vague","Explains clearly"),("Value","Suggests undervaluing","Correct declared")])),
"prep-center-amazon-fba": ("Prep center en frontera","Por separado vs en frontera","cmp",("Por separado","En frontera",[("Etiquetado","Distinto sitio","Mismo lugar"),("NOM","Aparte","Incluido"),("Aduana","Traspaso","Coordinada"),("Tiempo","Semanas","Días"),("Errores","Más","Menos")])),
"mercadolibre-vs-amazon-mexico": ("Mercado Libre vs Amazon Mexico","Where to sell first","cmp",("Amazon Mexico","Mercado Libre",[("Position","Strong second","Largest in MX"),("Buyers","Prime loyalty","Local, Mercado Pago"),("Fulfillment","FBA","Envíos Full"),("Best fit","Amazon sellers","Deep local reach"),("Needs MX stock","Yes","Yes")])),
"cuanto-vender-para-importar": ("Punto de equilibrio","Por paquete vs en volumen","cmp",("Por paquete","En volumen",[("Despacho","En cada pedido","Una vez por lote"),("Costo fijo por venta","Alto","Bajo, se reparte"),("Entrega","Días desde fuera","1-2 días local"),("Conviene","Casi nunca","Baja con el volumen")])),
"handle-returns-mexico-customers": ("Returns from Mexico","Ship back vs handle local","cmp",("Ship back to US","Handle in Mexico",[("Customer return","International","Domestic"),("Border cost","Northbound + duty","None, stays in MX"),("Restock","Re-import to resell","Local, no import"),("Value recovery","Slow, written off","Fast, resold")])),
"bonded-warehouse-laredo": ("Bonded warehouse vs FTZ","Laredo options · 2026","cmp",("Bonded warehouse","Foreign trade zone",[("Duty on arrival","Deferred","Not imported"),("Time limit","Up to 5 years","No time limit"),("Bond","Per entry","Not required"),("Re-export to MX","Deferral","No US duty"),("Value-added","Limited","Kitting, assembly")])),
"hibrit-dropshipping": ("Klasik vs hibrit dropshipping","Meksika · 2026","cmp",("Klasik","Hibrit",[("Gümrük/IVA","Her siparişte","Parti üzerinden"),("Teslimat","Bir hafta+","Yurt içi 1-3 gün"),("Sipariş maliyeti","Yüksek","Hızlı satanda düşük"),("Katalog","Geniş, risksiz","Stoklu + uzun kuyruk")])),
"amazon-meksika-mi-amerika-mi": ("Amazon ABD mi Meksika mı?","Türk satıcı için · 2026","cmp",("Amazon ABD","Amazon Meksika",[("Pazar","Çok büyük","~62 milyar $, büyüyor"),("Rekabet","Yüksek, doygun","Görece düşük"),("Reklam maliyeti","Yüksek","Görece düşük"),("Uyum","Olgun, tanıdık","IVA, NOM, CFDI"),("Lojistik","Laredo, NARF","Monterrey, FBA+Full")])),
"laredo-monterrey-depo-fulfillment": ("Laredo vs Monterrey depo","Hangi yaka neyi çözer · 2026","cmp",("Laredo (ABD)","Monterrey (MX)",[("Stok","Gümrük öncesi","Gümrüklenmiş"),("Kullanım","NARF, ABD siparişi","Yurt içi teslimat"),("Hız","Sınır + gümrük","Yurt içi 1-2 gün"),("Besleme","Prep","Full + FBA + müşteri"),("Avantaj","FTZ No. 94","IVA bir kez")])),
"amazon-mx-fba-gonderi": ("Amazon Meksika FBA gönderisi","6 adım · 2026","step",[("Gönderi planı","Seller Central"),("Prep + etiket","Amazon barkodu + NOM"),("Sınır deposu","Malı topla"),("Gümrük","Pedimento · IVA"),("Depoya teslim","Yurt içi sevkiyat"),("Q4 zamanlama","Geç Ekim")]),
"amazon-mexico-q4-cutoff-calendar": ("Amazon Mexico Q4 timeline","Plan backwards · 2026","step",[("Start shipping (US)","Early October"),("Cross + customs","Border buffer"),("Inventory live","By late October"),("El Buen Fin","November 13-17"),("Holiday peak","Through December")]),
"fechas-limite-fba-q4": ("Línea de tiempo Q4 FBA","Hacia atrás · 2026","step",[("Enviar desde EE.UU.","Inicios de octubre"),("Cruce + aduana","Margen de frontera"),("Inventario activo","Finales de octubre"),("El Buen Fin","13-17 de noviembre"),("Pico navideño","Diciembre")]),
"amazon-meksika-q4-takvimi": ("Amazon Meksika Q4 takvimi","Geriye doğru · 2026","step",[("ABD'den sevkiyat","Ekim başı"),("Geçiş + gümrük","Sınır tamponu"),("Stok aktif","Geç Ekim"),("El Buen Fin","13-17 Kasım"),("Yıl sonu piki","Aralık")]),
"how-to-ship-pallet-to-mexico": ("How to ship a pallet to Mexico","5 steps · 2026","step",[("Documents","Invoice, HS, origin"),("Freight to border","LTL or FTL"),("Customs","Pedimento · 16% IVA"),("Border handoff","Transfer to MX carrier"),("Delivery","1-2 days to Monterrey")]),
"requisitos-exportar-eeuu": ("Exportar a EE.UU. desde México","Requisitos clave · 2026","step",[("Factura + HTS","Clasificación correcta"),("Prueba de origen","T-MEC sin arancel"),("Importador de registro","Ante CBP"),("De minimis","Suspendido desde 2025"),("Agencias","FDA/USDA según producto")]),
"importar-para-vender-mercado-libre": ("Importar para Mercado Libre","Flujo en bloque · 2026","step",[("Importar en bloque","Con agente aduanal"),("Pagar IVA/arancel","Una vez, por lote"),("Etiquetado NOM","En español"),("Almacén en México","Stock listo"),("Alimentar Full","O envío doméstico")]),
"immex-benefits-us-shippers": ("IMMEX for US shippers","Program at a glance · 2026","stat",[("5,821","active programs"),("3.2M","workers"),("100%","VAT credit")],"IMMEX defers duty and IVA on temporary imports for export production"),
"hurricane-season-border-planning": ("2026 Atlantic hurricane season","NOAA outlook","stat",[("8-14","named storms"),("3-6","hurricanes"),("1-3","major")],"Below-normal season · June 1 to November 30 · plan buffers and staging"),
"nom-labeling-requirements-mexico": ("NOM labeling for Mexico","Which standard applies · 2026","status",[("General retail goods","NOM-050","lbl","Profeco"),("Food and beverages","NOM-051","res","COFEPRIS"),("Textiles and apparel","Category + NOM-050","res","Profeco"),("Electronics","Category NOM","res","Safety marks"),("All products","Importer of record","pro","SAT")]),
"meksika-sat-cfdi": ("Meksika SAT ve CFDI","Satıcının bilmesi gereken · 2026","status",[("CFDI 4.0","Zorunlu e-fatura","lbl","SAT · eşik yok"),("Carta Porte","Taşımada zorunlu","res","Federal taşıma"),("2026 reformu","Gerçeklik denetimi","pro","SAT"),("Uyumsuzluk","Ceza %5-10","pro","Fatura değeri")]),
"usmca-2026-review-shippers": ("USMCA 2026 review","Scenarios for shippers","dec",[("Status quo","Duty-free for qualifying goods, as today"),("Tighter rules","Stricter origin proof, most expected"),("Reversion","MFN tariffs return, six months notice")]),
"revision-tmec-2026-que-significa": ("Revisión del T-MEC 2026","Escenarios","dec",[("Continúa igual","Sin arancel para bienes calificados"),("Reglas más estrictas","Más prueba de origen, lo esperado"),("Reversión","Vuelven aranceles, con seis meses de aviso")]),
"usmca-tmec-2026-gozden-gecirme": ("USMCA 2026 ve Türk satıcı","Menşeine göre etki","dec",[("Türkiye menşeli","USMCA dışı, genel IGI tarifesi"),("ABD menşeli yönlendirme","Tercihli oran, ama sıkılaşabilir"),("Çin bağlantılı içerik","Kısıtlama hedefi, takip et")]),
# --- Gun 7-9 (grafik-deger yazilar) ---
"remote-fulfillment-narf-worth-it": ("Is NARF worth it for Mexico?","NARF vs local FBA · 2026","cmp",("NARF","Local FBA",[("Inventory","In the US","In Mexico"),("Who imports","Customer","You, bulk"),("RFC / IVA","None","Required"),("Delivery","About a week","Local Prime"),("Per-unit fee","Higher","Lower"),("Best for","Market test","Proven volume")])),
"cheapest-way-ship-freight-mexico": ("Cheapest way to ship to Mexico","What drives the cost · 2026","cost",[("Consolidate loads","Splits fixed cost","hi"),("Customs broker","Per pedimento","n"),("Duty · US origin (USMCA)","0% · USMCA","hi"),("IVA (VAT)","16%","n"),("Freight (LTL / FTL)","Varies · quote","mut"),("Small parcels","High per unit","mut")]),
"us-vs-mexican-customs-broker": ("US vs Mexican customs broker","Two sides of the border","cmp",("US broker","Mexican broker",[("Clears","US export","MX import"),("Files","EEI / AES","Pedimento"),("License","US customs broker","Patente aduanal"),("Required","On US side","Always for MX"),("Handles","Origin docs","Duty + 16% IVA")])),
"autocertificacion-origen-tmec": ("Autocertificación de origen T-MEC","Quién y cómo · 2026","status",[("Exportador","Puede certificar","lbl","Art. 5.2"),("Productor","Puede certificar","lbl","Art. 5.2"),("Importador","Puede certificar","lbl","Desde 2024"),("Formato oficial","No existe","res","En factura vale"),("Periodo blanket","Hasta 12 meses","res","Aceptación 4 años")]),
"nom-051-etiquetado-alimentos": ("NOM-051: sellos y fechas","Etiquetado frontal · 2026","status",[("Sellos EXCESO","Octagonales negros","lbl","5 nutrientes"),("Fase 2 (actual)","Hasta 31 dic 2027","res","Vigente"),("Fase 3","1 enero 2028","res","No en 2026"),("Leyendas","Cafeína · edulcorantes","lbl","Niños"),("Sin etiqueta","Se detiene en aduana","pro","NOM-051")]),
"mercado-libre-mi-amazon-mi": ("Mercado Libre mi Amazon mı?","Meksika pazaryeri · 2026","cmp",("Amazon Meksika","Mercado Libre",[("Konum","Güçlü ikinci","Meksika'da en büyük"),("Alıcı","Prime sadakati","Yerel, Mercado Pago"),("Lojistik","FBA / NARF","Envíos Full"),("Yerel stok","Gerekir","Gerekir"),("En uygun","Amazon satıcısı","Derin yerel erişim")])),
"meksikada-uretim-vs-ihracat": ("Meksika'da üretim mi ihracat mı?","Stratejik karşılaştırma · 2026","cmp",("Türkiye'den ihracat","Meksika'da üretim",[("Gümrük","Genel IGI tarifesi","ABD'ye T-MEC %0"),("Başlangıç","Düşük","Yüksek yatırım"),("Teslim süresi","Uzun","Yakın pazar"),("Nearshoring","Hayır","Evet, teşvikli"),("En uygun","Test, düşük hacim","Kanıtlı, yüksek hacim")])),
"nom-004-tekstil": ("NOM-004: tekstil etiketi","Zorunlu bilgiler · 2026","status",[("Lif bileşimi","% ağırlıkça","lbl","Azalan sırada"),("Bakım talimatı","İspanyolca","lbl","Semboller"),("Beden / ölçü","Zorunlu","lbl","NOM-004"),("Sorumlu taraf","RFC ile","res","İthalatçı / üretici"),("Menşe","Hecho en...","res","Dikili etiket")]),
"dropshipping-delivery-times-mexico": ("Dropshipping delivery times","Cross-border vs local stock","cmp",("Ship from abroad","Stock in Mexico",[("Delivery","A week or more","1-2 days"),("Customs","Per parcel","Once, bulk"),("Per-order cost","High","Low"),("Promise","Be honest","Fast local"),("Best for","Testing","Steady sellers")])),
"sell-mercadolibre-from-us": ("Sell on Mercado Libre from the US","Cross-border vs in-country","cmp",("Ship each order","Stock in Mexico",[("Delivery","About a week","1-2 days"),("Ranking","Penalized","Rewarded, Full"),("Import cost","Every parcel","Once, bulk"),("Fulfillment","You ship","Envíos Full"),("Best for","Rarely competitive","Ranked sales")])),
"nearshoring-freight-rates-impact": ("US truckload spot rates","DAT national · June 2026","stat",[("$3.00","Dry van / mi"),("$3.39","Reefer / mi"),("$3.69","Flatbed / mi")],"Up 39%+ YoY · driven by capacity, not only nearshoring · rates move weekly"),
"shipping-electronics-to-mexico": ("Shipping electronics to Mexico","NOMs and tax · 2026","status",[("NOM-024-SCFI","Commercial info + warranty","lbl","Spanish"),("NOM-001-SCFI","Safety certification","res","Covered apparatus"),("NOM-019-SCFI","IT equipment, under review","res","In force"),("Import IVA","16% nationwide","lbl","On customs value"),("Jul 1 2026","Telecom at import","pro","Verify fractions")]),
"puentes-internacionales-laredo-carga": ("Puentes de carga de Laredo","Cruce comercial · 2026","stat",[("2 de 4","puentes mueven carga"),("8","carriles · World Trade Bridge"),("~40%","de los cruces de camión")],"World Trade Bridge (solo carga) y Colombia Solidaridad · 14,000-18,000 camiones/día"),
"etiquetado-fnsku-amazon": ("Etiquetado FNSKU para FBA","Cómo etiquetar · 2026","step",[("Genera el FNSKU","En Seller Central"),("Imprime la etiqueta","1x2 a 2x3 pulgadas"),("Tinta negra, blanco","Superficie lisa"),("Tapa el código original","Solo uno escaneable"),("Revendedores 2026","FNSKU obligatorio (EE.UU.)")]),
"laredo-depo-hizmeti": ("Laredo depo hizmeti","Sınırda ne çözer · 2026","step",[("Teslim alma","Farklı tedarikçiler"),("Konsolidasyon","Tek ithalat"),("NOM etiketleme","İspanyolca"),("Gümrük","Pedimento · %16 IVA"),("Monterrey'e","1-2 iş günü")]),
"abdden-meksikaya-kargo": ("ABD'den Meksika'ya kargo","Tekil vs konsolide · 2026","cmp",("Kurye / tekil","Konsolide geçiş",[("Gümrük","Paket başına","Tek pedimento"),("Birim maliyet","Yüksek","Düşük, bölünür"),("Uygun","Ara sıra, numune","Düzenli ithalat"),("Belge","Her pakette","Bir kez"),("En iyi","Küçük gönderi","Artan hacim")])),
"reverse-logistics-mexico-3pl": ("Reverse logistics in Mexico","The return chain · 2026","step",[("Return collection","In-country address"),("Inspection","Resell / repair / dispose"),("Restocking","Back to inventory"),("Repair / repackage","Recover value"),("Consolidated return","Only what must go back")]),
"ftz-warehouse-laredo": ("FTZ warehousing in Laredo","How the duty benefit works","step",[("Admit to FTZ","No US duty on arrival"),("Hold in the zone","Duty deferred"),("Re-export to Mexico","US duty avoided"),("Mexican customs","Pedimento · 16% IVA"),("US-origin goods","Duty-free under USMCA")]),
"documents-ship-freight-mexico": ("Documents to ship to Mexico","The core checklist · 2026","status",[("Commercial invoice","Value + parties","lbl","Exporter"),("Packing list","Contents per box","lbl","Exporter"),("Certificate of origin","Claims USMCA 0%","lbl","3 parties"),("Pedimento","Import declaration","res","Licensed broker"),("NOM label / permits","Before crossing","res","Most goods")]),
"enable-narf-seller-central": ("Enable NARF in Seller Central","Step by step · as of 2026","step",[("Pro NA unified account","FBA + FBA Export"),("Remote Fulfillment settings","Under Inventory"),("Enroll Mexico","amazon.com.mx"),("Build International Listings","Sync prices"),("Confirm eligible ASINs","In Seller Central")]),
"capital-para-empezar-importar": ("Capital para empezar a importar","Rubros a presupuestar · 2026","cost",[("Mercancía","Pago al proveedor","n"),("Flete","Transporte y cruce","mut"),("IVA","16% · valor en aduana","n"),("Arancel · origen EE.UU.","0% · T-MEC","hi"),("Despacho aduanal","No regulado · rango","mut"),("Colchón","Imprevistos","n")]),
"importar-sin-padron-importadores": ("Importar sin Padrón","Vías y límites · 2026","status",[("Courier autorizado","Hasta 2,500 USD","lbl","Por destinatario"),("Uso personal","Topes por pedimento","res","No comercial"),("Única vez (A4/A5)","Máx. una al año","res","No sectorial"),("NOM y permisos","Siguen aplicando","pro","Sin excepción"),("Recurrente / comercial","Requiere Padrón","pro","Regla general")]),
"amazon-meksika-fbm": ("Amazon Meksika FBM","FBM vs FBA / NARF · 2026","cmp",("FBM","FBA / NARF",[("Depolama / kargo","Satıcı","Amazon"),("FNSKU / hazırlık","Gerekmez","Gerekir"),("Prime rozeti","Otomatik yok","Var"),("Meksika Prime","SFP ABD'ye özel","NARF / yerel FBA"),("En uygun","Kontrol, maliyet","Prime, kolaylık")])),
"palet-basina-maliyet-senaryo": ("Palet başına maliyet","Örnek kalem yapısı · doğrula","cost",[("Mal bedeli","Tedarikçiye","n"),("Navlun (TR-ABD)","Değişken","mut"),("Elleçleme + NOM","Laredo depo","n"),("IVA","%16 · gümrük değeri","n"),("Gümrük · TR menşe","T-MEC dışı · vergi var","mut"),("Depolama","Meksika içi","n")]),
"meksika-gumruk-vergisi-ne-kadar": ("Meksika gümrük vergisi","Menşeine göre · 2026 · doğrula","cost",[("IVA (ithalat)","%16 · ülke geneli","n"),("Gümrük · ABD menşe","%0 · T-MEC","hi"),("Kurye ≤50$ (T-MEC)","Vergisiz","hi"),("Kurye 50-117$ / >117$","%17 / %19","n"),("T-MEC dışı menşe","%33,5","mut"),("FTA'sız tarifeler","%5-50","mut")]),
# --- Gundem: MVE (Manifestacion de Valor Electronica) ---
"mexico-mve-customs-value-declaration": ("Mexico's electronic value declaration","Before vs after 1 Aug 2026","cmp",("Through 31 Jul","From 1 Aug",[("Filing","Electronic or paper","Electronic via VUCEM"),("Obligation","Importer","Importer"),("Transmits","Broker","Broker"),("Non-transmission","Allowed","Required"),("Deadline","Extended before","Verify again")])),
"manifestacion-valor-electronica-mve": ("Cumplir con la MVE","Antes del 1 de agosto 2026","step",[("Agente listo","Transmite por VUCEM"),("Factura y valor","Exactos y consistentes"),("Formato electrónico","E2 por VUCEM"),("Verificar el plazo","El SAT ya prorrogó antes")]),
"meksika-elektronik-deger-beyani": ("Elektronik Değer Beyanı (MVE)","Meksika · 2026","stat",[("31 Tem","geçiş biter"),("1 Ağu","zorunlu"),("VUCEM","elektronik form E2")],"İthalatçı sorumlu · gümrük müşaviri iletir · SAT ertelemesi mümkün, doğrula"),
}

OUT=os.path.dirname(os.path.abspath(__file__))
count=0
for slug,entry in D.items():
    title,sub,kind=titlecase(entry[0], slug in TR_SLUGS),entry[1],entry[2]
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

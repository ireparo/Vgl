#!/usr/bin/env python3
"""
Generador estático para VG Logistics.
Toma fragmentos de contenido y los envuelve con header/footer compartidos.
Uso: python3 build/template.py
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------- Plantillas -----------
HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Vidal Gurghian Logistics S.L.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{og_locale}">
<link rel="canonical" href="https://www.vglogistics.es/{canonical}">
<link rel="alternate" hreflang="es" href="https://www.vglogistics.es/{alt_es}">
<link rel="alternate" hreflang="en" href="https://www.vglogistics.es/en/{alt_en}">
<link rel="alternate" hreflang="ca" href="https://www.vglogistics.es/ca/{alt_ca}">
<link rel="alternate" hreflang="fr" href="https://www.vglogistics.es/fr/{alt_fr}">
<link rel="alternate" hreflang="it" href="https://www.vglogistics.es/it/{alt_it}">
<link rel="alternate" hreflang="x-default" href="https://www.vglogistics.es/{alt_es}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}">
{schema}
</head>
<body>
"""

HEADER = """<header class="site-header">
  <div class="container">
    <nav class="nav" aria-label="{nav_label}">
      <a href="{home}" class="brand">
        <span class="brand-mark">VGL</span>
        <span>VG Logistics<small>Committed Frigo Transport</small></span>
      </a>
      <button class="nav-toggle" aria-label="{menu_label}" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul class="nav-links">
{nav_items}
      </ul>
      <div class="nav-cta">
        <div class="lang-switch">
          <button class="lang-toggle" aria-haspopup="true" aria-expanded="false">🌐 {lang_short} ▾</button>
          <ul class="lang-menu" role="menu">
            <li><a href="{lang_es}">Español</a></li>
            <li><a href="{lang_en}">English</a></li>
            <li><a href="{lang_ca}">Català</a></li>
            <li><a href="{lang_fr}">Français</a></li>
            <li><a href="{lang_it}">Italiano</a></li>
          </ul>
        </div>
        <a href="{cta_href}" class="btn btn--primary">{cta_label}</a>
      </div>
    </nav>
  </div>
</header>
"""

FOOTER = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="brand"><span class="brand-mark">VGL</span><span style="color:#fff;">VG Logistics<small>Committed Frigo Transport</small></span></div>
        <p>{footer_about}</p>
      </div>
      <div><h4>{f_company}</h4><ul>
        <li><a href="{l_about}">{f_about}</a></li>
        <li><a href="{l_sustain}">{f_sustain}</a></li>
        <li><a href="{l_blog}">{f_blog}</a></li>
        <li><a href="{l_jobs}">{f_jobs}</a></li>
      </ul></div>
      <div><h4>{f_services}</h4><ul>
        <li><a href="{l_services}">{f_freight}</a></li>
        <li><a href="{l_sectors}">{f_sectors}</a></li>
        <li><a href="{l_fleet}">{f_fleet}</a></li>
        <li><a href="{l_coverage}">{f_coverage}</a></li>
      </ul></div>
      <div><h4>{f_contact}</h4><ul>
        <li>C/ Ivars d'Urgell 10<br>Edificio Neoparc I, 5º Of. 3<br>P.I. Neoparc — 25190 Lleida</li>
        <li><a href="tel:+34973677173">+34 973 677 173</a></li>
        <li><a href="mailto:admin@vglogistics.es">admin@vglogistics.es</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <div>© <span data-year>2026</span> Vidal Gurghian Logistics S.L. — CIF B25791773</div>
      <div><a href="{l_legal}">{f_legal}</a> · <a href="{l_privacy}">{f_privacy}</a> · <a href="{l_cookies}">{f_cookies}</a> · <a href="{l_terms}">{f_terms}</a></div>
    </div>
  </div>
</footer>
<script src="{js_path}"></script>
</body>
</html>
"""

# ----------- Configuración por idioma -----------
LANGS = {
    "es": {
        "lang": "es", "lang_short": "ES", "og_locale": "es_ES",
        "prefix": "", "css_path": "assets/css/styles.css", "js_path": "assets/js/main.js",
        "nav_label": "Principal", "menu_label": "Abrir menú",
        "cta_label": "Solicitar cotización",
        "footer_about": "Vidal Gurghian Logistics S.L. — Operador de transporte frigorífico internacional con base en Lleida. Especialistas en alimentación perecedera por toda Europa.",
        "f_company": "Empresa", "f_about": "Nosotros", "f_sustain": "Sostenibilidad", "f_blog": "Blog", "f_jobs": "Trabaja con nosotros",
        "f_services": "Servicios", "f_freight": "Transporte frigorífico", "f_sectors": "Sectores", "f_fleet": "Flota y recursos", "f_coverage": "Cobertura europea",
        "f_contact": "Contacto",
        "f_legal": "Aviso legal", "f_privacy": "Privacidad", "f_cookies": "Cookies", "f_terms": "Condiciones de transporte",
        "nav": [
            ("index.html", "Inicio"),
            ("nosotros.html", "Nosotros"),
            ("servicios.html", "Servicios"),
            ("sectores.html", "Sectores"),
            ("flota.html", "Flota"),
            ("cobertura.html", "Cobertura"),
            ("transportistas.html", "Transportistas"),
            ("sostenibilidad.html", "Sostenibilidad"),
            ("blog.html", "Blog"),
            ("contacto.html", "Contacto"),
        ],
        "links": {"home":"index.html","about":"nosotros.html","sustain":"sostenibilidad.html","blog":"blog.html","jobs":"transportistas.html","services":"servicios.html","sectors":"sectores.html","fleet":"flota.html","coverage":"cobertura.html","legal":"legal/aviso-legal.html","privacy":"legal/privacidad.html","cookies":"legal/cookies.html","terms":"legal/condiciones.html","contact":"contacto.html","cta":"contacto.html#cotizar"},
    },
    "en": {
        "lang": "en", "lang_short": "EN", "og_locale": "en_GB",
        "prefix": "en/", "css_path": "../assets/css/styles.css", "js_path": "../assets/js/main.js",
        "nav_label": "Main", "menu_label": "Open menu",
        "cta_label": "Request a quote",
        "footer_about": "Vidal Gurghian Logistics S.L. — International refrigerated road transport operator based in Lleida (Spain). Specialists in perishable food across Europe.",
        "f_company": "Company", "f_about": "About us", "f_sustain": "Sustainability", "f_blog": "Blog", "f_jobs": "Work with us",
        "f_services": "Services", "f_freight": "Frigo transport", "f_sectors": "Industries", "f_fleet": "Fleet & resources", "f_coverage": "European coverage",
        "f_contact": "Contact",
        "f_legal": "Legal notice", "f_privacy": "Privacy", "f_cookies": "Cookies", "f_terms": "Carriage conditions",
        "nav": [
            ("index.html", "Home"),
            ("about.html", "About"),
            ("services.html", "Services"),
            ("industries.html", "Industries"),
            ("fleet.html", "Fleet"),
            ("coverage.html", "Coverage"),
            ("carriers.html", "Carriers"),
            ("sustainability.html", "Sustainability"),
            ("blog.html", "Blog"),
            ("contact.html", "Contact"),
        ],
        "links": {"home":"index.html","about":"about.html","sustain":"sustainability.html","blog":"blog.html","jobs":"carriers.html","services":"services.html","sectors":"industries.html","fleet":"fleet.html","coverage":"coverage.html","legal":"../legal/aviso-legal.html","privacy":"../legal/privacidad.html","cookies":"../legal/cookies.html","terms":"../legal/condiciones.html","contact":"contact.html","cta":"contact.html#quote"},
    },
    "ca": {
        "lang": "ca", "lang_short": "CA", "og_locale": "ca_ES",
        "prefix": "ca/", "css_path": "../assets/css/styles.css", "js_path": "../assets/js/main.js",
        "nav_label": "Principal", "menu_label": "Obrir menú",
        "cta_label": "Sol·licitar pressupost",
        "footer_about": "Vidal Gurghian Logistics S.L. — Operador de transport frigorífic internacional amb base a Lleida. Especialistes en alimentació peridera per tot Europa.",
        "f_company": "Empresa", "f_about": "Nosaltres", "f_sustain": "Sostenibilitat", "f_blog": "Blog", "f_jobs": "Treballa amb nosaltres",
        "f_services": "Serveis", "f_freight": "Transport frigorífic", "f_sectors": "Sectors", "f_fleet": "Flota i recursos", "f_coverage": "Cobertura europea",
        "f_contact": "Contacte",
        "f_legal": "Avís legal", "f_privacy": "Privacitat", "f_cookies": "Galetes", "f_terms": "Condicions de transport",
        "nav": [
            ("index.html", "Inici"),
            ("nosaltres.html", "Nosaltres"),
            ("serveis.html", "Serveis"),
            ("sectors.html", "Sectors"),
            ("flota.html", "Flota"),
            ("cobertura.html", "Cobertura"),
            ("transportistes.html", "Transportistes"),
            ("sostenibilitat.html", "Sostenibilitat"),
            ("blog.html", "Blog"),
            ("contacte.html", "Contacte"),
        ],
        "links": {"home":"index.html","about":"nosaltres.html","sustain":"sostenibilitat.html","blog":"blog.html","jobs":"transportistes.html","services":"serveis.html","sectors":"sectors.html","fleet":"flota.html","coverage":"cobertura.html","legal":"../legal/aviso-legal.html","privacy":"../legal/privacidad.html","cookies":"../legal/cookies.html","terms":"../legal/condiciones.html","contact":"contacte.html","cta":"contacte.html#pressupost"},
    },
    "fr": {
        "lang": "fr", "lang_short": "FR", "og_locale": "fr_FR",
        "prefix": "fr/", "css_path": "../assets/css/styles.css", "js_path": "../assets/js/main.js",
        "nav_label": "Principal", "menu_label": "Ouvrir le menu",
        "cta_label": "Demander un devis",
        "footer_about": "Vidal Gurghian Logistics S.L. — Opérateur de transport frigorifique international basé à Lleida (Espagne). Spécialistes des denrées périssables en Europe.",
        "f_company": "Entreprise", "f_about": "À propos", "f_sustain": "Durabilité", "f_blog": "Blog", "f_jobs": "Carrières",
        "f_services": "Services", "f_freight": "Transport frigo", "f_sectors": "Secteurs", "f_fleet": "Flotte & ressources", "f_coverage": "Couverture européenne",
        "f_contact": "Contact",
        "f_legal": "Mentions légales", "f_privacy": "Confidentialité", "f_cookies": "Cookies", "f_terms": "Conditions de transport",
        "nav": [
            ("index.html", "Accueil"),
            ("a-propos.html", "À propos"),
            ("services.html", "Services"),
            ("secteurs.html", "Secteurs"),
            ("flotte.html", "Flotte"),
            ("couverture.html", "Couverture"),
            ("transporteurs.html", "Transporteurs"),
            ("durabilite.html", "Durabilité"),
            ("blog.html", "Blog"),
            ("contact.html", "Contact"),
        ],
        "links": {"home":"index.html","about":"a-propos.html","sustain":"durabilite.html","blog":"blog.html","jobs":"transporteurs.html","services":"services.html","sectors":"secteurs.html","fleet":"flotte.html","coverage":"couverture.html","legal":"../legal/aviso-legal.html","privacy":"../legal/privacidad.html","cookies":"../legal/cookies.html","terms":"../legal/condiciones.html","contact":"contact.html","cta":"contact.html#devis"},
    },
    "it": {
        "lang": "it", "lang_short": "IT", "og_locale": "it_IT",
        "prefix": "it/", "css_path": "../assets/css/styles.css", "js_path": "../assets/js/main.js",
        "nav_label": "Principale", "menu_label": "Apri il menù",
        "cta_label": "Richiedi preventivo",
        "footer_about": "Vidal Gurghian Logistics S.L. — Operatore di trasporto frigorifero internazionale con sede a Lleida (Spagna). Specialisti in alimenti deperibili in tutta Europa.",
        "f_company": "Azienda", "f_about": "Chi siamo", "f_sustain": "Sostenibilità", "f_blog": "Blog", "f_jobs": "Lavora con noi",
        "f_services": "Servizi", "f_freight": "Trasporto frigo", "f_sectors": "Settori", "f_fleet": "Flotta e risorse", "f_coverage": "Copertura europea",
        "f_contact": "Contatti",
        "f_legal": "Note legali", "f_privacy": "Privacy", "f_cookies": "Cookie", "f_terms": "Condizioni di trasporto",
        "nav": [
            ("index.html", "Home"),
            ("chi-siamo.html", "Chi siamo"),
            ("servizi.html", "Servizi"),
            ("settori.html", "Settori"),
            ("flotta.html", "Flotta"),
            ("copertura.html", "Copertura"),
            ("trasportatori.html", "Trasportatori"),
            ("sostenibilita.html", "Sostenibilità"),
            ("blog.html", "Blog"),
            ("contatti.html", "Contatti"),
        ],
        "links": {"home":"index.html","about":"chi-siamo.html","sustain":"sostenibilita.html","blog":"blog.html","jobs":"trasportatori.html","services":"servizi.html","sectors":"settori.html","fleet":"flotta.html","coverage":"copertura.html","legal":"../legal/aviso-legal.html","privacy":"../legal/privacidad.html","cookies":"../legal/cookies.html","terms":"../legal/condiciones.html","contact":"contatti.html","cta":"contatti.html#preventivo"},
    },
}

# Mapeo nombre interno -> nombre de fichero por idioma (para hreflang)
SLUGS = {
    "home":     {"es":"index.html","en":"index.html","ca":"index.html","fr":"index.html","it":"index.html"},
    "about":    {"es":"nosotros.html","en":"about.html","ca":"nosaltres.html","fr":"a-propos.html","it":"chi-siamo.html"},
    "services": {"es":"servicios.html","en":"services.html","ca":"serveis.html","fr":"services.html","it":"servizi.html"},
    "sectors":  {"es":"sectores.html","en":"industries.html","ca":"sectors.html","fr":"secteurs.html","it":"settori.html"},
    "fleet":    {"es":"flota.html","en":"fleet.html","ca":"flota.html","fr":"flotte.html","it":"flotta.html"},
    "coverage": {"es":"cobertura.html","en":"coverage.html","ca":"cobertura.html","fr":"couverture.html","it":"copertura.html"},
    "carriers": {"es":"transportistas.html","en":"carriers.html","ca":"transportistes.html","fr":"transporteurs.html","it":"trasportatori.html"},
    "sustain":  {"es":"sostenibilidad.html","en":"sustainability.html","ca":"sostenibilitat.html","fr":"durabilite.html","it":"sostenibilita.html"},
    "blog":     {"es":"blog.html","en":"blog.html","ca":"blog.html","fr":"blog.html","it":"blog.html"},
    "contact":  {"es":"contacto.html","en":"contact.html","ca":"contacte.html","fr":"contact.html","it":"contatti.html"},
}


def render_header(lang_cfg, current_slug):
    nav_items = ""
    for href, label in lang_cfg["nav"]:
        active = ' class="is-active"' if href == SLUGS[current_slug][lang_cfg["lang"]] else ""
        nav_items += f'        <li><a href="{href}"{active}>{label}</a></li>\n'

    return HEADER.format(
        nav_label=lang_cfg["nav_label"],
        menu_label=lang_cfg["menu_label"],
        home=lang_cfg["links"]["home"],
        nav_items=nav_items,
        lang_short=lang_cfg["lang_short"],
        lang_es="../" + SLUGS[current_slug]["es"] if lang_cfg["lang"] != "es" else SLUGS[current_slug]["es"],
        lang_en="../en/" + SLUGS[current_slug]["en"] if lang_cfg["lang"] != "en" else SLUGS[current_slug]["en"],
        lang_ca="../ca/" + SLUGS[current_slug]["ca"] if lang_cfg["lang"] != "ca" else SLUGS[current_slug]["ca"],
        lang_fr="../fr/" + SLUGS[current_slug]["fr"] if lang_cfg["lang"] != "fr" else SLUGS[current_slug]["fr"],
        lang_it="../it/" + SLUGS[current_slug]["it"] if lang_cfg["lang"] != "it" else SLUGS[current_slug]["it"],
        cta_href=lang_cfg["links"]["cta"],
        cta_label=lang_cfg["cta_label"],
    )


def render_footer(lang_cfg):
    L = lang_cfg["links"]
    return FOOTER.format(
        footer_about=lang_cfg["footer_about"],
        f_company=lang_cfg["f_company"], f_about=lang_cfg["f_about"], f_sustain=lang_cfg["f_sustain"], f_blog=lang_cfg["f_blog"], f_jobs=lang_cfg["f_jobs"],
        f_services=lang_cfg["f_services"], f_freight=lang_cfg["f_freight"], f_sectors=lang_cfg["f_sectors"], f_fleet=lang_cfg["f_fleet"], f_coverage=lang_cfg["f_coverage"],
        f_contact=lang_cfg["f_contact"],
        f_legal=lang_cfg["f_legal"], f_privacy=lang_cfg["f_privacy"], f_cookies=lang_cfg["f_cookies"], f_terms=lang_cfg["f_terms"],
        l_about=L["about"], l_sustain=L["sustain"], l_blog=L["blog"], l_jobs=L["jobs"],
        l_services=L["services"], l_sectors=L["sectors"], l_fleet=L["fleet"], l_coverage=L["coverage"],
        l_legal=L["legal"], l_privacy=L["privacy"], l_cookies=L["cookies"], l_terms=L["terms"],
        js_path=lang_cfg["js_path"],
    )


def render_page(slug, lang, title, description, body_html, schema=""):
    cfg = LANGS[lang]
    canonical = (cfg["prefix"] + SLUGS[slug][lang]).rstrip("/")
    head = HEAD.format(
        lang=cfg["lang"],
        title=title,
        description=description,
        og_locale=cfg["og_locale"],
        canonical=canonical,
        alt_es=SLUGS[slug]["es"],
        alt_en=SLUGS[slug]["en"],
        alt_ca=SLUGS[slug]["ca"],
        alt_fr=SLUGS[slug]["fr"],
        alt_it=SLUGS[slug]["it"],
        css_path=cfg["css_path"],
        schema=schema,
    )
    out = head + render_header(cfg, slug) + body_html + render_footer(cfg)
    return out


def write_page(slug, lang, title, description, body_html, schema=""):
    cfg = LANGS[lang]
    out_dir = os.path.join(ROOT, cfg["prefix"]) if cfg["prefix"] else ROOT
    os.makedirs(out_dir, exist_ok=True)
    filename = SLUGS[slug][lang]
    path = os.path.join(out_dir, filename)
    html = render_page(slug, lang, title, description, body_html, schema)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    print("Builder cargado. Importa y llama write_page() desde build/pages.py.")

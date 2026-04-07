# VG Logistics — Web corporativa

Rediseño de la web de **Vidal Gurghian Logistics S.L.** (VGL), operador
de transporte frigorífico internacional con base en Lleida.

- **CIF:** B25791773
- **Dominio actual:** vglogistics.es
- **Lema:** *Committed Frigo Transport*

## Stack

Sitio 100 % estático. Sin frameworks, sin build. Solo:

- **HTML5** semántico y accesible.
- **CSS** puro con sistema de diseño en `assets/css/styles.css` (variables CSS,
  componentes reutilizables, responsive mobile-first).
- **JavaScript** vanilla en `assets/js/main.js` (nav móvil, selector de
  idiomas, contadores animados, reveal on scroll, formulario de cotización).
- **Google Fonts** (Inter) como única dependencia externa.

Se puede desplegar en cualquier hosting estático: Netlify, Vercel, GitHub
Pages, Cloudflare Pages, o un servidor clásico.

## Estructura

```
/
├── index.html                Home (ES — idioma principal)
├── nosotros.html             Historia, misión, valores, ficha legal
├── servicios.html            FTL, LTL, control térmico, docs, GPS
├── sectores.html             Cárnico, hortofrutícola, lácteo, alimentación
├── flota.html                Equipamiento, certificaciones, tecnología
├── cobertura.html            Mapa europeo y destinos por región
├── transportistas.html       Programa para autónomos + alta
├── sostenibilidad.html       Acciones ambientales y hoja de ruta
├── blog.html                 Blog (próximamente)
├── contacto.html             Datos + OpenStreetMap + cotizador multicampo
├── 404.html                  Página de error amigable
├── sitemap.xml               Mapa del sitio con hreflang
├── robots.txt                Indexación
│
├── assets/
│   ├── css/styles.css        Sistema de diseño
│   ├── js/main.js            Interacciones
│   ├── img/                  (reservado para fotografía propia)
│   └── icons/                (reservado para favicons)
│
├── legal/
│   ├── aviso-legal.html      LSSI-CE
│   ├── privacidad.html       RGPD completo
│   ├── cookies.html          Política de cookies
│   └── condiciones.html      Condiciones generales de transporte (CMR)
│
├── en/                       Inglés — 10 páginas completas
│   ├── index.html            about.html        services.html
│   ├── industries.html       fleet.html        coverage.html
│   ├── carriers.html         sustainability.html  blog.html
│   └── contact.html
│
├── ca/index.html             Català — home
├── fr/index.html             Français — home
└── it/index.html             Italiano — home
```

## Idiomas

- **Español** (idioma principal): 10 páginas + 4 legales = 14 páginas.
- **Inglés**: 10 páginas completas.
- **Catalán / Francés / Italiano**: home con selector de idiomas que
  redirige a las secciones equivalentes en ES o EN.

### Cómo añadir más traducciones

Para tener CA, FR o IT completos, basta con copiar cualquier página de
`/en/` al directorio `/ca/`, `/fr/` o `/it/` y traducir el contenido. El
sistema de diseño y el JavaScript funcionan sin cambios.

## SEO y rendimiento

- Meta titles y descriptions únicos por página.
- `<link rel="alternate" hreflang>` en cada página multilingüe.
- `<link rel="canonical">` en todas las páginas.
- `sitemap.xml` con alternates por idioma.
- `robots.txt` permitiendo todo salvo `/legal/`.
- Datos estructurados **schema.org `MovingCompany`** en la home.
- HTML semántico con `<nav>`, `<section>`, `<article>`, `<header>`, `<footer>`.
- Google Fonts con `preconnect` y `display=swap`.
- Sin dependencias pesadas: se puede alcanzar Lighthouse 95+ fácilmente.

## Formularios

Los formularios (cotización y alta de transportistas) están implementados
como `mailto:` a `admin@vglogistics.es`. Funciona sin backend, pero para
producción se recomienda integrar un servicio como:

- **Formspree**, **Getform**, **Web3Forms** (sin backend propio).
- Un **endpoint propio** (Node/PHP) con validación y anti-spam.
- **Zapier / Make** para enviar a CRM.

Basta con cambiar el `action` del `<form>` en `contacto.html`,
`transportistas.html` y sus equivalentes EN.

## Desarrollo local

Al ser 100 % estático, abre cualquier archivo HTML con un servidor web
simple:

```bash
# Python
python3 -m http.server 8080

# Node (si tienes serve)
npx serve .

# PHP
php -S localhost:8080
```

Luego visita `http://localhost:8080`.

## Propuesta de próximos pasos

Mejoras que se pueden implementar después de validar el rediseño:

1. **Fotografía real** de la flota, el equipo y las oficinas en Lleida
   (sustituir los iconos emoji por imágenes propias).
2. **Favicon y logo SVG** definitivos.
3. **Completar traducciones** CA/FR/IT al mismo nivel que ES/EN.
4. **Publicar artículos** del blog (los placeholders están listos).
5. **Formulario conectado** a backend real + captcha.
6. **Banner de cookies** si se añaden cookies no esenciales.
7. **Google Business Profile** y Google Analytics 4 / Matomo.
8. **Portal cliente** con seguimiento GPS en tiempo real.
9. **Área "Trabaja con nosotros"** con ofertas de empleo para conductores.
10. **Certificaciones reales** (ISO, IFS Logistics, SQAS, OEA) cuando se
    obtengan, en `flota.html` y `nosotros.html`.

---

© Vidal Gurghian Logistics S.L. — CIF B25791773

# Sophiq Assets

Repositorio centralizado de assets visuales y plantillas de Sophiq Properties.

## Estructura

```
sophiq-assets/
├── email-templates/           # Plantillas y emails HTML
│   ├── campañas/              # Emails generados por campaña
│   │   ├── agencias-2026-W03/
│   │   └── capital-partners-enero-2026/
│   └── previews/              # HTMLs de preview para QA
├── hero-propiedades/          # Fotos hero de propiedades (JPG)
├── logos/                     # Logos de Sophiq
│   ├── sophiq-logo-dark.png
│   └── sophiq-logo-white.png
└── podcast-banners/           # Banners para SQ Insights podcast
```

## URLs públicas (GitHub Pages)

Las imágenes están disponibles públicamente via GitHub Pages:

```
https://grsnmyr.github.io/sophiq-assets/hero-propiedades/{codigo}.jpg
https://grsnmyr.github.io/sophiq-assets/logos/sophiq-logo-dark.png
https://grsnmyr.github.io/sophiq-assets/podcast-banners/sophiq-shots-8.jpg
```

### Ejemplo de uso en emails

```html
<img src="https://grsnmyr.github.io/sophiq-assets/hero-propiedades/lag94.jpg" alt="Propiedad LAG94">
```

## Convenciones de nombres

### Propiedades
- Formato: `{codigo}{numero}.jpg` (ej: `lag94.jpg`, `zur89a.jpg`)
- Los códigos son abreviaciones de ubicaciones o proyectos
- Siempre en minúsculas, solo JPG

### Campañas de email
- Formato: `{tipo}-{año}-{periodo}/` (ej: `agencias-2026-W03`, `capital-partners-enero-2026`)
- Dentro: archivos nombrados por email del destinatario

## Agregar nuevos assets

1. Colocar en la carpeta correspondiente
2. Usar convención de nombres establecida
3. Commit y push a main
4. GitHub Pages actualiza automáticamente

## Notas

- Los PNGs de propiedades fueron removidos (usar JPG)
- Tamaño máximo recomendado por imagen: 2MB
- GitHub Pages tiene un límite de 1GB para el repositorio

# Resultados reales de los generadores

Estos archivos se han creado ejecutando los scripts con datos sintéticos.
Los SVG son editables y los PNG se pueden usar como fondos estáticos.
No se han aplicado cambios al escritorio de ningún equipo.

## Vista de los PNG generados

![Hoja de contacto](diseno/contacto.png)

- [Degradado PNG](diseno/degradado.png)
- [Foto geométrica de prueba](diseno/geometria.png)
- [Fondo desenfocado](diseno/desenfocado.png)
- [Avatar cuadrado](diseno/avatar.png)
- [Icono ICO de siete tamaños](diseno/icono.ico)
- [Paleta extraída en JSON](diseno/paleta.json)

## Fondos y recursos SVG

### fondo-degradado-svg

![fondo-degradado-svg](diseno/fondo-degradado-svg.svg)

[Descargar SVG](diseno/fondo-degradado-svg.svg)

### fondo-mosaico-svg

![fondo-mosaico-svg](diseno/fondo-mosaico-svg.svg)

[Descargar SVG](diseno/fondo-mosaico-svg.svg)

### fondo-ondas-svg

![fondo-ondas-svg](diseno/fondo-ondas-svg.svg)

[Descargar SVG](diseno/fondo-ondas-svg.svg)

### fondo-orbitas-svg

![fondo-orbitas-svg](diseno/fondo-orbitas-svg.svg)

[Descargar SVG](diseno/fondo-orbitas-svg.svg)

### icono-monograma-svg

![icono-monograma-svg](diseno/icono-monograma-svg.svg)

[Descargar SVG](diseno/icono-monograma-svg.svg)

### panel-inspiracion-svg

![panel-inspiracion-svg](diseno/panel-inspiracion-svg.svg)

[Descargar SVG](diseno/panel-inspiracion-svg.svg)

### rejilla-puntos-svg

![rejilla-puntos-svg](diseno/rejilla-puntos-svg.svg)

[Descargar SVG](diseno/rejilla-puntos-svg.svg)

### zonas-escritorio-svg

![zonas-escritorio-svg](diseno/zonas-escritorio-svg.svg)

[Descargar SVG](diseno/zonas-escritorio-svg.svg)

## Reproducir desde la raíz

Usa nombres nuevos o una carpeta distinta: los generadores no sobrescriben.

```powershell
py fondo-ondas-svg/script.py ondas.svg --primario "#0B1026" --secundario "#56DCC6"
py icono-monograma-svg/script.py iniciales.svg --ancho 512 --alto 512 --texto SP
py fondo-degradado-png/script.py escritorio.png --ancho 2560 --alto 1440
py fondo-desenfocado/script.py ejemplos/diseno/geometria.png suave.png
py imagen-a-ico/script.py ejemplos/diseno/avatar.png icono.ico
py contraste-colores/script.py "#FFFFFF" "#0B1026"
```

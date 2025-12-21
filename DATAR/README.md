# {DATAR} Integraciones

[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Plataforma Bogotá](https://img.shields.io/badge/Plataforma-Bogotá-7B2CBF)](https://plataformabogota.gov.co/)
[![MangleRojo ORG](https://img.shields.io/badge/MangleRojo-ORG-DC143C)](https://manglerojo.org)
[![LaBosquescuela UBA](https://img.shields.io/badge/LaBosquescuela-UBA-228B22)](https://labosquescuela.org)
<a href="https://codewiki.google/github.com/DATAR-lab/integraciones"><img src="https://www.gstatic.com/_/boq-sdlc-agents-ui/_/r/Mvosg4klCA4.svg" alt="Ask Code Wiki" height="20"></a>


## Laboratorio de experimentación con datos ambientales basado en la orquestación de agentes autónomos.

Franja Plataforma Satélite de **[Plataforma Bogotá](https://plataformabogota.gov.co/)**.

Laboratorio a cargo de:
**[MangleRojo ORG](https://manglerojo.org)** y **[LaBosquescuela UBA](https://labosquescuela.org)**.

![DATAR Web App](../docs/images/DATAR_web-app.png)

**Vínculos importantes:**
- **[Web](datar-lab.github.io/integraciones/)**
- **[Prototipo](https://datar-integraciones-web-app-dd3vrcpotq-rj.a.run.app/)**
- **[Invitaciones Culturales](https://invitaciones.scrd.gov.co/verInvitacion/938)**

---

Prototipo desarrollado con **Google ADK [(Agent Development Kit)](https://google.github.io/adk-docs/)** que orquesta múltiples sub-agentes especializados. Cada agente está diseñado para facilitar diferentes formas de interacción y exploración del entorno natural, promoviendo una relación más sensible y relacional con los ecosistemas.

## Arquitectura

El prototipo está organizado en una arquitectura jerárquica:

- **Agente Raíz (Gente_Raiz)**: Orquestador principal que gestiona y enruta las interacciones hacia los sub-agentes especializados.
- **Sub-agentes**: Agentes especializados que ofrecen diferentes perspectivas y herramientas para explorar el entorno.

## Sub-agentes Disponibles

### Gente_Montaña
Un agente que siempre saluda desde la Montaña.

### Gente_Pasto
Puede comunicarse con sonidos y palabras, pero prefiere el sonido para mostrar lo que sabe. Las pocas palabras que usa son apenas destellos de tu ser y sentir.

### Gente_Intuitiva
Es un asistente que ayuda a identificar patrones del trazo o signo del pensamiento que se percibe en una interacción con el territorio.

### Gente_Interpretativa
Sistema de interpretación y re-interpretación del entorno usando emojis y texto, con múltiples capas de agentes que procesan y fusionan perspectivas.

### Gente_Bosque
Este agente está diseñado para despertar interés y curiosidad, basado en las sensaciones iniciales que le produce un lugar. Su tono es descriptivo, informativo y curioso, con el objetivo de abrir la percepción hacia la complejidad natural del bosque, puede sugerir preguntas filosóficas.

### Gente_Sonora
Exploración de ambientes sonoros y experiencias auditivas, creando un puente entre múltiples perspectivas sonoras del entorno natural del humedal de la Conejera.

### Gente_Horaculo
Su misión es conectar una experiencia humana en la naturaleza con el tejido vivo y legendario del territorio. Para ello, guia una conversación en dos fases: primero, la recolección de hebras de memoria (las preguntas) y, segundo, el tejido de una leyenda futurista corta y significativa.

### Gente_Compostada
Herramienta para el conocimiento ecológico, educativo y práctico que es capaz de ayudar al usuario a reconocer la importancia de la descomposición de los reisudos orgánicos como insumo para alimentar el crecimiento de bosques urbanos en la zona del Parkway, en Bogotá.

## Configuración

### Modelo LLM

Por defecto, el prototipo utiliza el modelo `minimax-m2` a través de OpenRouter.

## Funcionalidades

- **Orquestación de agentes**: El agente raíz enruta automáticamente las interacciones al sub-agente más apropiado.
- **Generación de medios**: Los agentes pueden generar archivos de audio (`.wav`, `.m4a`, `.mp3`) e imágenes (`.png`) que se almacenan en Cloud Storage.
- **Herramientas especializadas**: Cada sub-agente tiene acceso a herramientas específicas (por ejemplo, `inferir_especies`, `crear_cartografía_emocional` en Gente_Bosque).

## Contacto

Únete a nuestra comunidad en Discord: [{DATAR}](https://discord.gg/ch9Zebzm)

## Licencia

Este proyecto está licenciado bajo la licencia Apache 2.0 - ver [LICENSE](LICENSE) para detalles.
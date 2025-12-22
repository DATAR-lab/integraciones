"""
Agente re-interpretativa que utiliza agentes paralelos
para generar respuestas enriquecidas.
"""
import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import ParallelAgent, SequentialAgent
from google.genai import types
from ...agents_utils import get_openrouter_config

from .utils import (
    leer_instrucciones, cambiar_respuesta_emojis, 
    cambiar_respuesta_textual, cambiar_respuesta_fusionadora,
    verificar_estado_fusionador
)

# ==========
# Agentes paralelos
# ==========

config = get_openrouter_config()

# Agente especializado en interpretar respuestas usando solo emojis
agente_interprete_emojis = Agent(
    model=LiteLlm(
        model="openrouter/minimax/minimax-m2",
        api_key=config.api_key,
        api_base=config.api_base,
    ),
    name='GenteInterpreteDeEmojis',
    description=(
        'Recibe una interacción y retorna una '
        'interpretación con sólo emojis'
    ),
    instruction=leer_instrucciones("ins_emoji_agent.md"),
    generate_content_config=types.GenerateContentConfig(
        temperature=1.8
    ),
    after_model_callback=cambiar_respuesta_emojis
)

# Agente especializado en responder con narrativas, 
# dando su perspectiva en texto invitando a interpretar 
# y generando preguntas.
agente_interprete_textual = Agent(
    model=LiteLlm(
        model="openrouter/minimax/minimax-m2",
        api_key=config.api_key,
        api_base=config.api_base,
    ),
    name='GenteInterpreteDeTexto',
    description=(
        'Recibe una interacción y retorna una '
        'interpretación invitando a interpretar su respuesta e '
        'generando preguntas a su interlocutor.'
    ),
    instruction=leer_instrucciones("ins_agente_textual.md"),
    generate_content_config=types.GenerateContentConfig(
        temperature=1.6
    ),
    after_model_callback=cambiar_respuesta_textual
)

# ==========
# Agentes paralelos y fusionador
# ==========

# Agente que ejecuta los agentes en paralelo
agente_paralelizador = ParallelAgent(
    name='GenteParalelizador',
    description='Corre múltiples agentes en paralelo.',
    sub_agents=[agente_interprete_emojis, agente_interprete_textual],
)

# Agente que combina las respuestas de los agentes paralelos
agente_fusionador = Agent(
    model=LiteLlm(
        model="openrouter/minimax/minimax-m2",
        api_key=config.api_key,
        api_base=config.api_base,
    ),
    name='GenteFusionador',
    description=(
        'Recibe las respuestas de múltiples agentes '
        'y las combina en una sola respuesta coherente. '
        'Las respuestas están disponibles en el estado como respuesta_textual y respuesta_emojis.'
    ),
    instruction=leer_instrucciones("ins_merger_agent.md"),
    before_model_callback=verificar_estado_fusionador,
    after_model_callback=cambiar_respuesta_fusionadora
)

# =======
# Agente de interacción
# =======

# Definir un agente normal que interactúe con lxs usuarixs
# y les defina una forma de interactuar
agente_re_interpretativa = Agent(
    model=LiteLlm(
        model="openrouter/minimax/minimax-m2",
        api_key=config.api_key,
        api_base=config.api_base,
    ),
    name='GenteReInterpretativa',
    description=(
        'Un asistente presto a ayudar e informar '
        'con datos ambientales de Bogotá'
    ),
    instruction=leer_instrucciones("ins_re_interpretativa.md"),
)

# Agente secuencial que ejecuta los agentes paralelos, fusiona las respuestas
# y luego reinterpreta para el usuario.
# Eliminamos el LoopAgent ya que con max_iterations=1 no aporta valor
# y puede causar problemas de estado. Esto reduce las llamadas al API.
agente_interpretativa_secuencial = SequentialAgent(
    name="GenteInterpretativa",
    sub_agents=[agente_paralelizador, agente_fusionador, agente_re_interpretativa],
    description="Coordina agentes paralelos, fusiona respuestas y reinterpreta."
)

# Agente raíz que se utilizará para interactuar
root_agent = agente_interpretativa_secuencial
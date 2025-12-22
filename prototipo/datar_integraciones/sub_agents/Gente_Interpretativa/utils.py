"""
Utilidades para GenteInterpretativa.
"""
from pathlib import Path
from google.adk.models.llm_response import LlmResponse
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

def obtener_path_instrucciones():
    """
    Obtiene el path absoluto de la carpeta 'instrucciones'.
    """
    path_agentes = Path(__file__).parent
    return path_agentes / "instrucciones"

def leer_instrucciones(archivo: str = "ins_defecto.md"):
    """
    Lee el contenido de un archivo de instrucciones 
    ubicado en la carpeta 'instrucciones'.

    Args:
        archivo (str): Nombre del archivo de instrucciones. 
        Por defecto es 'ins_defecto.md'.
        
    Returns:
        str: Contenido del archivo de instrucciones.
    """

    path_archivo = obtener_path_instrucciones() / archivo

    with open(path_archivo, "r") as a:
        instrucciones = a.read()
 
    return instrucciones

def cambiar_respuesta_emojis(callback_context: CallbackContext, llm_response: LlmResponse):
    """
    Función para guardar respuesta del LLM en una variable de 
    contexto y modificar la respuesta del agente al usuario para mostrar "Procesando...". 
    
    Este callback oculta la respuesta del agente paralelo de emojis, ya que solo
    el agente final debe mostrar su respuesta al usuario. El streaming se aplica
    solo al agente final (agente_re_interpretativa) que no tiene callback.
    """
    # Verificar si hay contenido en la respuesta
    if llm_response.content and llm_response.content.parts and len(llm_response.content.parts) > 0:
        texto_respuesta = llm_response.content.parts[0].text
        
        # Asignar respuesta del modelo a una variable en estado
        callback_context.state['respuesta_emojis'] = texto_respuesta
        
        # Debug: confirmar que se guardó
        print(f"[DEBUG] respuesta_emojis guardada: {len(callback_context.state['respuesta_emojis'])} caracteres", flush=True)

        # Ocultar la respuesta mostrando "Procesando..." para mantener el flujo correcto
        # El streaming se aplicará solo al agente final que no tiene callback
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )
    else:
        # Si no hay contenido, mostrar "Procesando..."
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )

def cambiar_respuesta_textual(callback_context: CallbackContext, llm_response: LlmResponse):
    """
    Función para guardar respuesta del LLM en una variable de 
    contexto y modificar la respuesta del agente al usuario para mostrar "Procesando...". 
    
    Este callback oculta la respuesta del agente paralelo textual, ya que solo
    el agente final debe mostrar su respuesta al usuario. El streaming se aplica
    solo al agente final (agente_re_interpretativa) que no tiene callback.
    """
    # Verificar si hay contenido en la respuesta
    if llm_response.content and llm_response.content.parts and len(llm_response.content.parts) > 0:
        texto_respuesta = llm_response.content.parts[0].text
        
        # Asignar respuesta del modelo a una variable en estado
        callback_context.state['respuesta_textual'] = texto_respuesta
        
        # Debug: confirmar que se guardó
        print(f"[DEBUG] respuesta_textual guardada: {len(callback_context.state['respuesta_textual'])} caracteres", flush=True)

        # Ocultar la respuesta mostrando "Procesando..." para mantener el flujo correcto
        # El streaming se aplicará solo al agente final que no tiene callback
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )
    else:
        # Si no hay contenido, mostrar "Procesando..."
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )

def verificar_estado_fusionador(callback_context: CallbackContext, llm_request=None):
    """
    Verifica que el estado tenga las variables necesarias antes de ejecutar el fusionador.
    Si faltan, las inicializa con valores por defecto para evitar errores.
    También muestra "Procesando..." para indicar que el fusionador está trabajando.
    
    Args:
        callback_context: Contexto del callback con el estado
        llm_request: Request del LLM (parámetro requerido por before_model_callback)
    """
    print("[DEBUG] verificar_estado_fusionador llamado", flush=True)
    
    # Verificar que las variables del estado estén disponibles
    if 'respuesta_emojis' not in callback_context.state:
        callback_context.state['respuesta_emojis'] = ''
        print("[DEBUG] respuesta_emojis no encontrada en estado, inicializada como vacía", flush=True)
    else:
        print(f"[DEBUG] respuesta_emojis encontrada: {len(callback_context.state['respuesta_emojis'])} caracteres", flush=True)
        
    if 'respuesta_textual' not in callback_context.state:
        callback_context.state['respuesta_textual'] = ''
        print("[DEBUG] respuesta_textual no encontrada en estado, inicializada como vacía", flush=True)
    else:
        print(f"[DEBUG] respuesta_textual encontrada: {len(callback_context.state['respuesta_textual'])} caracteres", flush=True)
    
    # Debug: mostrar qué hay en el estado
    print(f"[DEBUG] Estado fusionador completo - respuesta_emojis: {bool(callback_context.state.get('respuesta_emojis'))}, respuesta_textual: {bool(callback_context.state.get('respuesta_textual'))}", flush=True)
    
    # Mostrar "Procesando..." mientras el fusionador se prepara
    # Nota: before_model_callback no puede retornar LlmResponse, solo puede modificar el estado
    # El mensaje "Procesando..." se mostrará cuando el agente comience a procesar
    return None

def cambiar_respuesta_fusionadora(callback_context: CallbackContext, llm_response: LlmResponse):
    """
    Función para guardar respuesta del LLM en una variable de 
    contexto y modificar la respuesta del agente al usuario para mostrar "Procesando...". 
    
    Este callback oculta la respuesta del fusionador, ya que solo
    el agente final debe mostrar su respuesta al usuario. El streaming se aplica
    solo al agente final (agente_re_interpretativa) que no tiene callback.
    """
    # Verificar si hay contenido en la respuesta
    if llm_response.content and llm_response.content.parts and len(llm_response.content.parts) > 0:
        texto_respuesta = llm_response.content.parts[0].text
        
        # Asignar respuesta del modelo a una variable en estado
        callback_context.state['respuesta_fusionadora'] = texto_respuesta
        
        # Debug: confirmar que se guardó
        print(f"[DEBUG] respuesta_fusionadora guardada: {len(callback_context.state['respuesta_fusionadora'])} caracteres", flush=True)

        # Ocultar la respuesta mostrando "Procesando..." para mantener el flujo correcto
        # El streaming se aplicará solo al agente final que no tiene callback
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )
    else:
        # Si no hay contenido, mostrar "Procesando..."
        return LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='Procesando...')])
        )
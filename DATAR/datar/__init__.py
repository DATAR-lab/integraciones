from . import agent
from .agent import root_agent

# Metadata de los agentes disponibles
AGENTS_METADATA = {
    "root_agent": {
        "name": "root_agent",
        "description": "Agente raíz DATAR - Orquestador de sub-agentes",
        "type": "root",
        "model": "openrouter/minimax/minimax-m2",
        "sub_agents": [
            "Gente_Montaña",
            "Gente_Pasto",
            "Gente_Intuitiva",
            "Gente_Interpretativa",
            "Gente_Bosque",
            "Gente_Sonora",
            "Gente_Horaculo",
            "Gente_Compostada",
        ]
    }
}

# Exportar
__all__ = ["root_agent", "AGENTS_METADATA"]

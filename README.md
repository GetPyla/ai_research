# AI Research - Exemples d'utilisation des LLMs

Ce dépôt contient des implémentations pratiques de modèles de langage (LLMs) pour différentes tâches complexes.

## 🚀 Fonctionnalités

- **RAG (Retrieval-Augmented Generation)**
  - Indexation de documents
  - Recherche contextuelle
  - Interface Streamlit pour interactions
  - Exemple : `RAG/streamlit_ui.py`

- **Task Agents**
  - Orchestration de tâches complexes
  - Classification d'intentions
  - Intégration Gmail (lecture/rédaction emails)
  - Synthèse vocale (TTS/STT)
  - Exemple : `Task_Agents/task_manager.py`

- **Interfaces Utilisateur**
  - Chat conversationnel (`chat_ui.py`)
  - Assistant de génération de code (`code_ui.py`)

## 🛠 Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/ai_research.git

# Installer les dépendances
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configuration requise
cp .env.example .env  # Configurer les clés API
```

## 💻 Utilisation

### Lancer l'interface RAG
```bash
streamlit run RAG/streamlit_ui.py
```

### Démarrer le système de Task Agents
```bash
cd Task_Agents
python task_manager.py   # Mode vocal
```

### Démarrer le système de Task Agents mode vocal
```bash
cd Task_Agents
python task_manager_voice.py   # Mode vocal
```

### Utiliser le chat conversationnel
```bash
python chat_ui.py 
```

### Utiliser le chat conversationnel avec interaction python
```bash
python code_ui.py 
```

## Licence
MIT License

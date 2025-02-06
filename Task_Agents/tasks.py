import json
import os
from dataclasses import asdict, dataclass

import yaml

from typing import List, Optional
from datetime import date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.oauth2 import credentials
from google.auth.transport.requests import Request
from pydantic import BaseModel, Field, validator
import os

TOKEN_FILE = os.getenv("TOKEN_FILE")
CREDS_FILE = os.getenv("CREDS_FILE")

class Task(BaseModel):
    """Modèle Pydantic pour une tâche Google."""
    title: str = Field(..., description="Titre de la tâche.")
    id: Optional[str] = Field(None, description="ID unique de la tâche (seulement lors de la lecture).")
    status: Optional[str] = Field(None, description="Status de la tâche (seulement lors de la lecture).")
    due: Optional[date] = Field(None, description="Date d'échéance de la tâche.")
    notes: Optional[str] = Field(None, description="Notes supplémentaires sur la tâche.")


    @validator('due', pre=True, always=True)
    def parse_due_date(cls, value):
      """Convertir la date d'échéance si elle n'est pas déjà une date"""
      if value is None:
          return None
      if isinstance(value, date):
         return value
      if isinstance(value, str):
         return date.fromisoformat(value[:10])  # Récupérer la date du format ISO
      
      raise ValueError("La date doit être dans un format ISO standard YYYY-MM-DD")

class TaskList(BaseModel):
    """Modèle Pydantic pour une liste de tâches."""
    tasks: List[Task] = Field(default_factory=list, description="Liste des tâches dans la liste.")


def get_ceredntials():
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


def get_google_tasks(tasklist_id: str = '@default') -> TaskList | None:
    """Récupère les tâches Google d'une liste spécifique."""
    tasklist_id = '@default'
    try:
        creds = get_ceredntials()
        service = build('tasks', 'v1', credentials=creds)
        results = service.tasks().list(tasklist=tasklist_id).execute()
        tasks = results.get('items', [])
        
        if not tasks:
            print('Aucune tâche trouvée.')
            return TaskList()
        
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append(
              Task(
                title=task.get('title', 'Sans titre'),
                id=task.get('id', None),
                status=task.get('status', None),
                due=task.get('due', None),
                notes=task.get('notes', None),
               )
              )
        return TaskList(tasks=formatted_tasks)
            

    except Exception as e:
        print(f"Erreur lors de la récupération des tâches : {e}")
        return None


def create_google_task(task: Task, tasklist_id: str = '@default') -> Task | None:
    """Crée une tâche Google dans une liste spécifiée."""
    try:
        creds = get_ceredntials()

        service = build('tasks', 'v1', credentials=creds)

        task_body = task.dict(exclude_none=True) # Exclure les champs None
        if task_body.get('due'):
            task_body['due'] = task_body['due'].isoformat() + "T00:00:00.000Z"
          
        created_task = service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()

        # Retourner une instance Task
        return Task(
           title=created_task.get('title', 'Sans titre'),
           id=created_task.get('id', None),
           status=created_task.get('status', None),
           due=created_task.get('due', None),
           notes=created_task.get('notes', None),
        )
    except Exception as e:
        print(f"Erreur lors de la création de la tâche : {e}")
        return None

def complete_google_task(task_id: str, tasklist_id: str = '@default') -> Task | None:
    """Marque une tâche Google comme complétée (fermée)."""
    tasklist_id = '@default' 
    try:
        creds = get_ceredntials()

        service = build('tasks', 'v1', credentials=creds)

        # Fetch the right task

        completed_task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        completed_task['status'] = 'completed'
        updated_task = service.tasks().update(tasklist=tasklist_id, task=task_id, body=completed_task).execute()


        return Task(
           title=updated_task.get('title', 'Sans titre'),
           id=updated_task.get('id', None),
           status=updated_task.get('status', None),
           due=updated_task.get('due', None),
           notes=updated_task.get('notes', None),
        )
    except Exception as e:
        print(f"Erreur lors de la complétion de la tâche : {e}")
        return None




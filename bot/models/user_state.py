import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any

class UserState:
    """Управление состоянием пользователей в flow"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Создать таблицу для состояний пользователей"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_states (
                user_id INTEGER PRIMARY KEY,
                flow_id TEXT NOT NULL,
                current_node_id TEXT NOT NULL,
                context TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_state(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить состояние пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT flow_id, current_node_id, context FROM user_states WHERE user_id = ?',
            (user_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'flow_id': row[0],
                'current_node_id': row[1],
                'context': json.loads(row[2])
            }
        return None
    
    def set_state(self, user_id: int, flow_id: str, node_id: str, context: Dict = None):
        """Установить состояние пользователя"""
        if context is None:
            context = {}
        
        now = datetime.utcnow().isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_states (user_id, flow_id, current_node_id, context, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                flow_id = excluded.flow_id,
                current_node_id = excluded.current_node_id,
                context = excluded.context,
                updated_at = excluded.updated_at
        ''', (user_id, flow_id, node_id, json.dumps(context), now, now))
        
        conn.commit()
        conn.close()
    
    def update_context(self, user_id: int, context: Dict):
        """Обновить контекст пользователя"""
        state = self.get_state(user_id)
        if state:
            merged_context = {**state['context'], **context}
            self.set_state(user_id, state['flow_id'], state['current_node_id'], merged_context)
    
    def clear_state(self, user_id: int):
        """Очистить состояние пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_states WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()

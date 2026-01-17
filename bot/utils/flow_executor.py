import aiohttp
from typing import Optional, Dict, Any, List
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class FlowExecutor:
    """Исполнитель flow - обрабатывает узлы и переходы"""
    
    def __init__(self, api_url: str, bot_id: int):
        self.api_url = api_url
        self.bot_id = bot_id
    
    async def get_active_flow(self) -> Optional[Dict[str, Any]]:
        """Получить активный flow из API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/flows/{self.bot_id}') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    flows = data.get('flows', [])
                    # Найти активный flow
                    for flow in flows:
                        if flow.get('is_active'):
                            return flow
                return None
    
    async def get_flow_data(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Получить данные flow по ID"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/flows/{self.bot_id}/{flow_id}') as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
    
    def find_node(self, flow_data: Dict, node_id: str) -> Optional[Dict]:
        """Найти узел по ID"""
        nodes = flow_data.get('flow', {}).get('nodes', [])
        for node in nodes:
            if node['id'] == node_id:
                return node
        return None
    
    def get_next_nodes(self, flow_data: Dict, current_node_id: str) -> List[Dict]:
        """Получить следующие узлы после текущего"""
        edges = flow_data.get('flow', {}).get('edges', [])
        next_node_ids = [edge['target'] for edge in edges if edge['source'] == current_node_id]
        
        nodes = []
        for node_id in next_node_ids:
            node = self.find_node(flow_data, node_id)
            if node:
                nodes.append(node)
        return nodes
    
    async def execute_node(self, bot: Bot, user_id: int, node: Dict, context: Dict) -> Dict[str, Any]:
        """Выполнить узел и вернуть результат"""
        node_type = node.get('type')
        node_data = node.get('data', {})
        
        result = {
            'success': True,
            'next_node_id': None,
            'wait_for_input': False
        }
        
        if node_type == 'input':
            # Стартовый узел - просто переходим дальше
            result['next_node_id'] = 'auto'
        
        elif node_type == 'textNode':
            # Отправка текста
            text = node_data.get('text', node_data.get('label', 'No text'))
            await bot.send_message(user_id, text)
            result['next_node_id'] = 'auto'
        
        elif node_type == 'buttonNode':
            # Отправка кнопок
            text = node_data.get('text', 'Choose an option:')
            buttons = node_data.get('buttons', [])
            
            if buttons:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=btn.get('text', 'Button'),
                        callback_data=f"btn:{node['id']}:{i}"
                    )] for i, btn in enumerate(buttons)
                ])
                await bot.send_message(user_id, text, reply_markup=keyboard)
                result['wait_for_input'] = True  # Ждём нажатия кнопки
            else:
                await bot.send_message(user_id, text)
                result['next_node_id'] = 'auto'
        
        elif node_type == 'imageNode':
            # Отправка изображения
            image_url = node_data.get('imageUrl', '')
            caption = node_data.get('caption', '')
            if image_url:
                await bot.send_photo(user_id, image_url, caption=caption)
            result['next_node_id'] = 'auto'
        
        elif node_type == 'videoNode':
            # Отправка видео
            video_url = node_data.get('videoUrl', '')
            caption = node_data.get('caption', '')
            if video_url:
                await bot.send_video(user_id, video_url, caption=caption)
            result['next_node_id'] = 'auto'
        
        elif node_type == 'conditionNode':
            # Условный переход
            # TODO: реализовать логику проверки условий
            result['next_node_id'] = 'auto'
        
        elif node_type == 'delayNode':
            # Задержка
            # TODO: реализовать отложенную отправку
            result['next_node_id'] = 'auto'
        
        else:
            # Неизвестный тип узла
            result['next_node_id'] = 'auto'
        
        return result

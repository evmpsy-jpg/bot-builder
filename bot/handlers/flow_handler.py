from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from models.user_state import UserState
from utils.flow_executor import FlowExecutor
import config

router = Router()
user_state = UserState(config.DB_PATH)
executor = FlowExecutor(config.API_URL, config.BOT_ID)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start - запуск активного flow"""
    user_id = message.from_user.id
    
    # Получаем активный flow
    active_flow = await executor.get_active_flow()
    
    if not active_flow:
        await message.answer("⚠️ No active flow configured. Please set up a flow in the admin panel.")
        return
    
    flow_id = active_flow['flow_id']
    
    # Получаем данные flow
    flow_data = await executor.get_flow_data(flow_id)
    
    if not flow_data:
        await message.answer("❌ Failed to load flow data.")
        return
    
    # Находим стартовый узел (type: 'input')
    nodes = flow_data.get('flow', {}).get('nodes', [])
    start_node = None
    for node in nodes:
        if node.get('type') == 'input':
            start_node = node
            break
    
    if not start_node:
        await message.answer("❌ Flow has no start node.")
        return
    
    # Устанавливаем состояние пользователя
    user_state.set_state(user_id, flow_id, start_node['id'], {})
    
    # Выполняем стартовый узел
    await execute_current_node(message.bot, user_id, flow_data)


async def execute_current_node(bot, user_id: int, flow_data: dict = None):
    """Выполнить текущий узел пользователя"""
    state = user_state.get_state(user_id)
    
    if not state:
        return
    
    # Если flow_data не передан, загружаем
    if not flow_data:
        flow_data = await executor.get_flow_data(state['flow_id'])
    
    if not flow_data:
        return
    
    current_node = executor.find_node(flow_data, state['current_node_id'])
    
    if not current_node:
        return
    
    # Выполняем узел
    result = await executor.execute_node(bot, user_id, current_node, state['context'])
    
    if not result['success']:
        return
    
    # Если нужно ждать ввода пользователя - останавливаемся
    if result['wait_for_input']:
        return
    
    # Если указан следующий узел
    if result['next_node_id'] == 'auto':
        # Автоматический переход к следующему узлу
        next_nodes = executor.get_next_nodes(flow_data, state['current_node_id'])
        
        if next_nodes:
            next_node = next_nodes[0]  # Берём первый доступный
            user_state.set_state(user_id, state['flow_id'], next_node['id'], state['context'])
            # Рекурсивно выполняем следующий узел
            await execute_current_node(bot, user_id, flow_data)
        else:
            # Достигнут конец flow
            user_state.clear_state(user_id)
    elif result['next_node_id']:
        # Переход к конкретному узлу
        user_state.set_state(user_id, state['flow_id'], result['next_node_id'], state['context'])
        await execute_current_node(bot, user_id, flow_data)


@router.callback_query(F.data.startswith('btn:'))
async def handle_button_callback(callback: CallbackQuery):
    """Обработка нажатий на inline кнопки"""
    user_id = callback.from_user.id
    
    # Парсим callback_data: btn:node_id:button_index
    parts = callback.data.split(':')
    if len(parts) != 3:
        await callback.answer("Invalid button data")
        return
    
    node_id = parts[1]
    button_index = int(parts[2])
    
    state = user_state.get_state(user_id)
    
    if not state or state['current_node_id'] != node_id:
        await callback.answer("⚠️ This button is no longer active")
        return
    
    # Получаем flow data
    flow_data = await executor.get_flow_data(state['flow_id'])
    
    if not flow_data:
        await callback.answer("❌ Failed to load flow")
        return
    
    # Находим узел с кнопкой
    button_node = executor.find_node(flow_data, node_id)
    
    if not button_node:
        await callback.answer("❌ Button node not found")
        return
    
    # Получаем данные кнопки
    buttons = button_node.get('data', {}).get('buttons', [])
    
    if button_index >= len(buttons):
        await callback.answer("❌ Invalid button")
        return
    
    button = buttons[button_index]
    
    # Сохраняем выбор в контекст
    context_update = {
        'last_button': button.get('text', ''),
        'last_button_value': button.get('value', '')
    }
    user_state.update_context(user_id, context_update)
    
    await callback.answer(f"✅ {button.get('text', 'Selected')}")
    
    # Переходим к следующему узлу
    next_nodes = executor.get_next_nodes(flow_data, node_id)
    
    if next_nodes:
        next_node = next_nodes[0]
        user_state.set_state(user_id, state['flow_id'], next_node['id'], state['context'])
        await execute_current_node(callback.bot, user_id, flow_data)
    else:
        # Конец flow
        user_state.clear_state(user_id)
        await callback.message.answer("✅ Flow completed!")

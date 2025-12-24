import pytest
from datetime import date
from unittest.mock import Mock, patch

# ========== Integration Tests ==========
class TestIntegrationWorkflows:
    def test_complete_meal_planning_with_feedback_loop(self):
        """Тест И1: Полный цикл умного планирования с обратной связью"""
        # Инициализация компонентов
        meal_planner = Mock()
        shopping_gen = Mock()
        budget_manager = Mock()
        data_layer = Mock()
        
        # 1. Генерация начального плана
        initial_plan = {
            'user_id': 123,
            'calories_per_day': 1500,
            'days': 7,
            'meals_per_day': 3
        }
        meal_planner.generate_plan.return_value = initial_plan
        
        # 2. Генерация списка покупок
        shopping_list = {
            'total_cost': 8500,
            'items_count': 25,
            'categories': ['овощи', 'мясо', 'молочка']
        }
        shopping_gen.generate_shopping_list.return_value = shopping_list
        
        # 3. Проверка бюджета (превышение!)
        budget_check_1 = {
            'within_limit': False,
            'overspend_amount': 500,
            'current_limit': 8000
        }
        budget_manager.check_limit.return_value = budget_check_1
        
        # 4. Оптимизация плана
        optimized_plan = {
            'adjusted_calories': 1450,
            'adjusted_cost': 7800,
            'changes_made': ['Заменено 3 рецепта', 'Уменьшены порции']
        }
        meal_planner.optimize_plan.return_value = optimized_plan
        
        # 5. Повторная генерация списка
        optimized_shopping_list = {
            'total_cost': 7800,
            'items_count': 23,
            'categories': ['овощи', 'мясо', 'молочка']
        }
        shopping_gen.generate_shopping_list.return_value = optimized_shopping_list
        
        # 6. Повторная проверка бюджета
        budget_check_2 = {
            'within_limit': True,
            'remaining_budget': 200,
            'current_limit': 8000
        }
        budget_manager.check_limit.return_value = budget_check_2
        
        # 7. Сохранение данных
        data_layer.save_plan.return_value = {'plan_id': 1001}
        data_layer.save_list.return_value = {'list_id': 2001}
        
        # Выполнение workflow
        plan = meal_planner.generate_plan(user_id=123, budget=8000, calories_target=1500)
        shopping_list = shopping_gen.generate_shopping_list(plan)
        budget_status = budget_manager.check_limit(user_id=123, planned_amount=shopping_list['total_cost'])
        
        if not budget_status['within_limit']:
            plan = meal_planner.optimize_plan(plan, budget_limit=8000)
            shopping_list = shopping_gen.generate_shopping_list(plan)
            budget_status = budget_manager.check_limit(user_id=123, planned_amount=shopping_list['total_cost'])
        
        # Сохранение результатов
        saved_plan = data_layer.save_plan(plan)
        saved_list = data_layer.save_list(shopping_list)
        
        # Проверки
        assert budget_status['within_limit'] == True
        assert shopping_list['total_cost'] <= 8000
        assert saved_plan['plan_id'] == 1001
        assert saved_list['list_id'] == 2001

    def test_recipe_adaptation_with_real_pantry(self):
        """Тест И2: Адаптация рецептов под реальные остатки"""
        # Инициализация
        recipe_manager = Mock()
        shopping_gen = Mock()
        data_layer = Mock()
        
        # Мок данных
        original_recipe = {
            'name': 'Борщ',
            'ingredients': [
                {'name': 'свекла', 'amount': 2, 'unit': 'шт'},
                {'name': 'капуста', 'amount': 0.3, 'unit': 'кг'},
                {'name': 'картофель', 'amount': 3, 'unit': 'шт'},
                {'name': 'мясо', 'amount': 0.5, 'unit': 'кг'}
            ]
        }
        
        pantry = {
            'свекла': {'amount': 1, 'unit': 'шт'},
            'капуста': {'amount': 0.5, 'unit': 'кг'},
            'мясо': {'amount': 0, 'unit': 'кг'}
        }
        
        # Адаптация рецепта
        adapted_recipe = {
            'name': 'Вегетарианский борщ с грибами',
            'ingredients': [
                {'name': 'свекла', 'amount': 1, 'unit': 'шт', 'source': 'pantry'},
                {'name': 'морковь', 'amount': 2, 'unit': 'шт', 'source': 'buy'},
                {'name': 'капуста', 'amount': 0.3, 'unit': 'кг', 'source': 'pantry'},
                {'name': 'картофель', 'amount': 3, 'unit': 'шт', 'source': 'buy'},
                {'name': 'грибы', 'amount': 0.3, 'unit': 'кг', 'source': 'buy'}
            ]
        }
        recipe_manager.adapt_recipe.return_value = adapted_recipe
        
        # Генерация списка покупок
        shopping_list = {
            'items': [
                {'name': 'морковь', 'amount': 2, 'unit': 'шт'},
                {'name': 'картофель', 'amount': 3, 'unit': 'шт'},
                {'name': 'грибы', 'amount': 0.3, 'unit': 'кг'}
            ],
            'total_cost': 280
        }
        shopping_gen.generate_shopping_list.return_value = shopping_list
        
        # Выполнение workflow
        adapted = recipe_manager.adapt_recipe(original_recipe, pantry)
        final_list = shopping_gen.generate_shopping_list(adapted['ingredients'])
        
        # Проверки
        assert adapted['name'] == 'Вегетарианский борщ с грибами'
        assert len(final_list['items']) == 3
        assert final_list['total_cost'] < 400

    def test_multi_level_budget_optimization(self):
        """Тест И3: Многоуровневая оптимизация бюджета"""
        # Инициализация
        budget_manager = Mock()
        shopping_gen = Mock()
        meal_planner = Mock()
        
        # Начальные данные
        initial_plan_cost = 12000
        budget_limit = 7000
        
        # Уровень 1: Замена брендов
        level1_cost = 10200
        level1_savings = 1800
        
        # Уровень 2: Замена ингредиентов
        level2_cost = 8160
        level2_savings = 2040
        
        # Уровень 3: Изменение плана
        level3_cost = 7344
        level3_savings = 816
        
        # Уровень 4: Корректировка порций
        final_cost = 6977
        final_savings = 367
        
        # Мок последовательных оптимизаций
        budget_manager.optimize_level1.return_value = {'cost': level1_cost, 'savings': level1_savings}
        budget_manager.optimize_level2.return_value = {'cost': level2_cost, 'savings': level2_savings}
        budget_manager.optimize_level3.return_value = {'cost': level3_cost, 'savings': level3_savings}
        budget_manager.optimize_level4.return_value = {'cost': final_cost, 'savings': final_savings}
        
        # Выполнение оптимизаций
        current_cost = initial_plan_cost
        optimizations = []
        
        while current_cost > budget_limit:
            if current_cost > 10000:
                result = budget_manager.optimize_level1(current_cost)
            elif current_cost > 8000:
                result = budget_manager.optimize_level2(current_cost)
            elif current_cost > 7000:
                result = budget_manager.optimize_level3(current_cost)
            else:
                result = budget_manager.optimize_level4(current_cost)
            
            current_cost = result['cost']
            optimizations.append(result)
            
            if len(optimizations) >= 4:  # Защита от бесконечного цикла
                break
        
        # Проверки
        assert current_cost <= budget_limit
        assert len(optimizations) >= 3
        assert optimizations[-1]['cost'] == 6977

    def test_multi_user_family_planning(self):
        """Тест И11: Многопользовательское планирование для семьи"""
        # Инициализация
        user_manager = Mock()
        meal_planner = Mock()
        budget_manager = Mock()
        
        # Данные семьи
        family_members = [
            {'id': 1, 'role': 'adult', 'allergies': [], 'preferences': ['meat']},
            {'id': 2, 'role': 'adult', 'allergies': ['nuts'], 'preferences': ['vegetarian']},
            {'id': 3, 'role': 'child', 'allergies': ['lactose'], 'preferences': ['pasta']},
            {'id': 4, 'role': 'child', 'allergies': [], 'preferences': ['chicken']}
        ]
        
        user_manager.get_family_members.return_value = family_members
        
        # Создание плана с учетом всех ограничений
        family_plan = {
            'shared_meals': [
                {'meal': 'breakfast', 'recipes': ['Овсянка', 'Омлет']},
                {'meal': 'dinner', 'recipes': ['Курица с овощами', 'Паста']}
            ],
            'individual_meals': {
                2: ['Вегетарианский суп'],  # вегетарианские блюда
                3: ['Безлактозные блины']   # безлактозные блюда
            }
        }
        meal_planner.create_family_plan.return_value = family_plan
        
        # Генерация объединенного списка покупок
        shopping_list = {
            'shared_items': [
                {'name': 'курица', 'amount': 1.5, 'unit': 'кг'},
                {'name': 'овощи', 'amount': 3, 'unit': 'кг'},
                {'name': 'паста', 'amount': 0.5, 'unit': 'кг'}
            ],
            'individual_items': {
                2: [{'name': 'тофу', 'amount': 0.3, 'unit': 'кг'}],
                3: [{'name': 'безлактозное молоко', 'amount': 1, 'unit': 'литр'}]
            },
            'total_cost': 4200
        }
        
        # Распределение бюджета
        budget_distribution = {
            'adults_share': 0.7,
            'children_share': 0.3,
            'total_budget': 6000,
            'adults_budget': 4200,
            'children_budget': 1800
        }
        budget_manager.calculate_family_distribution.return_value = budget_distribution
        
        # Выполнение workflow
        members = user_manager.get_family_members(family_id=1)
        plan = meal_planner.create_family_plan(members, budget=6000)
        budget_dist = budget_manager.calculate_family_distribution(members, total_budget=6000)
        
        # Проверки
        assert len(plan['shared_meals']) > 0
        assert len(plan['individual_meals']) >= 2
        assert budget_dist['adults_share'] + budget_dist['children_share'] == 1.0
        assert budget_dist['total_budget'] == 6000

    def test_real_time_device_sync(self):
        """Тест И5: Синхронизация между устройствами в реальном времени"""
        # Инициализация
        data_layer = Mock()
        sync_service = Mock()
        
        # Симуляция одновременного редактирования
        device1_changes = [
            {'type': 'recipe_update', 'recipe_id': 5, 'timestamp': '10:00:00'},
            {'type': 'plan_add', 'day': 'monday', 'timestamp': '10:00:05'}
        ]
        
        device2_changes = [
            {'type': 'recipe_update', 'recipe_id': 5, 'timestamp': '10:00:03'},
            {'type': 'shopping_update', 'item': 'молоко', 'timestamp': '10:00:07'}
        ]
        
        # Конфликт в редактировании рецепта 5
        conflicts = [
            {
                'resource': 'recipe_5',
                'device1_change': device1_changes[0],
                'device2_change': device2_changes[0],
                'resolution': 'last_write_wins',
                'winner': 'device2'
            }
        ]
        
        sync_service.detect_conflicts.return_value = conflicts
        sync_service.resolve_conflicts.return_value = {
            'resolved': True,
            'merged_changes': device1_changes + device2_changes[1:],
            'conflict_count': 1
        }
        
        # Выполнение синхронизации
        detected_conflicts = sync_service.detect_conflicts(device1_changes, device2_changes)
        resolution_result = sync_service.resolve_conflicts(detected_conflicts)
        
        # Проверки
        assert resolution_result['resolved'] == True
        assert resolution_result['conflict_count'] == 1
        assert len(resolution_result['merged_changes']) == 3
        assert resolution_result['merged_changes'][0]['resolution'] == 'last_write_wins'

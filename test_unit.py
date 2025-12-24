import pytest
from datetime import date
from shopping import ShoppingGenerator
from budget import BudgetManager
from recipes import RecipeManager
from planner import MealPlanner

# ========== ShoppingGenerator Tests ==========
class TestShoppingGenerator:
    def test_optimize_packaging_decision(self):
        """Тест Б2.2: Выбор между большой выгодной упаковкой и маленькими"""
        sg = ShoppingGenerator()
        
        result = sg.optimize_packaging(
            product_name="майонез",
            needed_amount=0.3,
            packaging_options=[
                {'size': 0.2, 'price': 100, 'unit': 'кг'},
                {'size': 0.5, 'price': 200, 'unit': 'кг'}
            ],
            weekly_usage=0.05,
            shelf_life_opened=28
        )
        
        assert result['recommended_packaging']['size'] == 0.5
        assert result['savings_percentage'] > 0

    def test_smart_consolidation_with_context(self):
        """Тест Б2.1: Интеллектуальное объединение списков"""
        sg = ShoppingGenerator()
        
        lists = [
            [{"name": "Молоко 3.2%", "amount": 1, "unit": "литр"}],
            [{"name": "Молоко 2.5%", "amount": 0.5, "unit": "литр"}],
            [{"name": "Сливки 10%", "amount": 0.2, "unit": "литр"}]
        ]
        
        result = sg.smart_consolidate(lists, context="выпечка")
        assert len(result) == 2
        assert any("Молоко" in item['name'] for item in result)

    def test_compare_store_strategies_full(self):
        """Тест Б2.3: Сравнение 'один магазин' vs 'несколько магазинов'"""
        sg = ShoppingGenerator()
        
        result = sg.compare_store_strategies(
            items={"Молоко": 80, "Хлеб": 50, "Сыр": 300, "Кофе": 500},
            store1_total=930,
            store1_time=10,
            store2_total=830,
            store2_time=40,
            parking_cost=50,
            time_value=100
        )
        
        assert 'recommendation' in result
        assert 'total_cost_1' in result
        assert 'total_cost_2' in result

    def test_calculate_cross_utilization(self):
        """Тест Б2.4: Учет cross-utilization ингредиентов"""
        sg = ShoppingGenerator()
        
        result = sg.calculate_cross_utilization(
            ingredient="лимон",
            usages=[
                {"day": "day1", "amount": 0.25, "use_case": "маринад"},
                {"day": "day3", "amount": 0.25, "use_case": "подача"},
                {"day": "day5", "amount": 0.25, "use_case": "чай"}
            ],
            shelf_life_days=7
        )
        
        assert result['buy_quantity'] == 1
        assert len(result['usage_schedule']) == 3

# ========== BudgetManager Tests ==========
class TestBudgetManager:
    def test_predict_spending_with_ml(self):
        """Тест Б3.1: Прогнозирование бюджета с машинным обучением"""
        bm = BudgetManager()
        
        result = bm.predict_spending(
            user_id=123,
            forecast_date=date(2025, 12, 31),
            include_seasonality=True,
            include_holidays=True
        )
        
        assert 'predicted_amount' in result
        assert 'confidence_interval_min' in result
        assert 'confidence_interval_max' in result

    def test_calculate_waste_impact(self):
        """Тест Б3.2: Расчет влияния отходов на бюджет"""
        bm = BudgetManager()
        
        result = bm.calculate_waste_impact([
            {"name": "Морковь 1кг", "price": 80, "waste_percentage": 20},
            {"name": "Куриное филе 500г", "price": 300, "waste_percentage": 8},
            {"name": "Батон", "price": 40, "waste_percentage": 15}
        ])
        
        assert result['total_effective_cost'] > 0
        assert result['total_waste_loss'] > 0
        assert len(result['recommendations']) > 0

    def test_rebalance_budget_dynamically(self):
        """Тест Б3.3: Динамическое перераспределение бюджета"""
        bm = BudgetManager()
        
        result = bm.rebalance_budget(
            original_budget={"основы": 4000, "овощи": 3000, "молочка": 2000, "прочее": 1000},
            current_spending={"основы": 4500, "овощи": 2800},
            total_overspend=1200
        )
        
        assert sum(result.values()) <= 10000
        assert result['основы'] == 4500

    def test_calculate_carbon_footprint(self):
        """Тест Б3.4: Расчет углеродного следа"""
        bm = BudgetManager()
        
        result = bm.calculate_carbon_footprint([
            {"product": "Говядина", "amount": 1, "co2_per_kg": 20},
            {"product": "Курица", "amount": 1, "co2_per_kg": 5},
            {"product": "Овощи местные", "amount": 2, "co2_per_kg": 0.3}
        ], carbon_price=5000)
        
        assert result['total_co2_kg'] > 0
        assert result['hidden_cost_rub'] > 0
        assert len(result['alternatives']) > 0

# ========== RecipeManager Tests ==========
class TestRecipeManager:
    def test_calculate_nutrition_with_cooking(self):
        """Тест Б1.1: Расчет КБЖУ с учетом способа приготовления"""
        rm = RecipeManager()
        
        result = rm.calculate_nutrition(
            ingredients=[
                {"name": "Картофель", "amount": 500, "unit": "г", "calories_raw": 77}
            ],
            cooking_method="Жарка во фритюре",
            cooking_params={"temperature": 180, "time": 10, "oil_absorption": 0.15}
        )
        
        assert result['calories'] > 400
        assert 'fat' in result
        assert 'vitamin_c_loss_percentage' in result

    def test_adapt_recipe_for_diet_restrictions(self):
        """Тест Б1.2: Коррекция рецепта под диетические ограничения"""
        rm = RecipeManager()
        
        result = rm.adapt_for_diet(
            original_recipe={
                "name": "Салат Цезарь",
                "ingredients": ["сухарики", "сыр пармезан", "соус с яйцом"]
            },
            restrictions=["веган", "без глютена"],
            substitution_database={
                "сухарики": ["гренки из безглютенового хлеба"],
                "пармезан": ["дрожжевые хлопья"],
                "яйцо": ["аквафаба"]
            }
        )
        
        assert "сухарики" not in str(result['adapted_ingredients'])
        assert result['similarity_score'] > 0.7

    def test_calculate_seasonal_cost_optimization(self):
        """Тест Б1.3: Расчет себестоимости с учетом сезонности"""
        rm = RecipeManager()
        
        result = rm.calculate_seasonal_cost(
            recipe_name="Клубничный пирог",
            ingredients=[{"name": "клубника", "amount": 0.5, "unit": "кг"}],
            target_date=date(2025, 1, 15),
            region="Москва"
        )
        
        assert result['fresh_cost'] > result['frozen_cost']
        assert len(result['alternative_suggestions']) > 0

# ========== MealPlanner Tests ==========
class TestMealPlanner:
    def test_balance_macronutrients_weekly(self):
        """Тест Б4.1: Балансировка макронутриентов в недельном плане"""
        mp = MealPlanner()
        
        result = mp.balance_macronutrients(
            current_plan={"углеводы": 400, "белки": 50, "жиры": 80},
            targets={"белки": 100, "жиры": 70, "углеводы": 300},
            recipe_database_size=200
        )
        
        assert result['белки'] >= 90
        assert result['углеводы'] <= 310
        assert result['recipe_repetitions'] <= 2

    def test_optimize_for_time_energy_distribution(self):
        """Тест Б4.3: Планирование с учетом времени и энергии"""
        mp = MealPlanner()
        
        result = mp.optimize_for_time_energy(
            user_schedule={"work_days": ["mon", "tue", "wed", "thu", "fri"]},
            recipes_by_difficulty={
                "easy": [{"name": "Омлет", "time": 15}],
                "medium": [{"name": "Суп", "time": 45}],
                "hard": [{"name": "Пирог", "time": 90}]
            }
        )
        
        assert len(result['weekdays']) > 0
        assert len(result['weekend']) > 0
        assert result['total_cooking_time_hours'] < 10

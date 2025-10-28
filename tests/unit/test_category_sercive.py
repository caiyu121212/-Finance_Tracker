import pytest
from src.services.category_service import CategoryService


class TestCategoryService:
    def test_get_categories(self,temp_database):
        service = CategoryService()
        categories = service.get_categories()
        assert len(categories)>0
        print("分类获取功能正常")

    def test_get_categories_by_type(self,temp_database):
        service = CategoryService()


        income_categories = service.get_categories('income')
        expense_categories = service.get_categories('expense')

        assert all(cat['type'] == 'income' for cat in income_categories)
        assert all(cat['type'] == 'expense' for cat in expense_categories)
        print("分类按类型过滤功能正常")
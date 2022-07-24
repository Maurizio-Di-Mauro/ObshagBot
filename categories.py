from typing import Dict, List, NamedTuple

from objects import Category
import db


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """returns categories"""
        categories: List[Dict] = db.fetchall("category", ["codename", "name", "aliases"])
        categories: List[Category] = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """get aliases of categories"""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Category]:
        """Return Categories"""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Get category by name"""
        founded_category = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    founded_category = category
        if not founded_category:
            founded_category = other_category
        return founded_category

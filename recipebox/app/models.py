from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Date, Boolean
)
from sqlalchemy.orm import relationship
from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    servings = Column(Integer, default=4)
    prep_minutes = Column(Integer, default=0)
    cook_minutes = Column(Integer, default=0)
    tags = Column(String, default="")          # comma-separated
    image = Column(String, default="")          # filename in uploads
    source_url = Column(String, default="")
    favorite = Column(Boolean, default=False)
    difficulty = Column(String, default="")     # easy / medium / hard
    cuisine = Column(String, default="")
    translations = Column(Text, default="")     # JSON {"fr":{"title":..,"description":..}, "ar":{...}}
    nutrition = Column(Text, default="")        # JSON {"calories":"270","protein":"5 g",...}
    created_at = Column(DateTime, default=datetime.utcnow)

    ingredients = relationship(
        "Ingredient", back_populates="recipe",
        cascade="all, delete-orphan", order_by="Ingredient.position",
    )
    steps = relationship(
        "Step", back_populates="recipe",
        cascade="all, delete-orphan", order_by="Step.position",
    )


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    position = Column(Integer, default=0)
    text = Column(String, nullable=False)       # full/fallback text e.g. "500 g flour"
    quantity = Column(String, default="")       # kept as string to allow "1/2", "2-3"
    unit = Column(String, default="")           # g, ml, tbsp, cup...
    name = Column(String, default="")           # flour, salt...
    name_translations = Column(Text, default="")  # JSON {"fr": "...", "ar": "..."} for name
    image = Column(String, default="")          # per-ingredient photo filename
    recipe = relationship("Recipe", back_populates="ingredients")


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    position = Column(Integer, default=0)
    text = Column(Text, nullable=False)
    translations = Column(Text, default="")     # JSON {"fr": "...", "ar": "..."}
    image = Column(String, default="")          # per-step photo filename
    timer_seconds = Column(Integer, default=0)  # 0 = no timer
    recipe = relationship("Recipe", back_populates="steps")


class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    category = Column(String, default="")
    quantity = Column(Integer, default=1)
    checked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String, default="")


class IngredientImage(Base):
    """Remembered photo for an ingredient name, reused across recipes."""
    __tablename__ = "ingredient_images"
    name = Column(String, primary_key=True)     # lowercased ingredient name
    image = Column(String, default="")          # stored image ref (uploads/icon/usericon)


class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True)
    day = Column(Date, default=date.today)
    meal_type = Column(String, default="dinner")  # breakfast/lunch/dinner
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    note = Column(String, default="")
    recipe = relationship("Recipe")

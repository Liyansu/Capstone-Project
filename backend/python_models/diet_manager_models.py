"""Domain models for building Diet Manager training and testing datasets.

The models in this module capture the key entities required to curate
supervised learning corpora for a diet management system that:

* Profiles a user via health parameters and diet plans
* Identifies foods from images and retrieves their recipes
* Breaks recipes into ingredient-level nutrient estimates
* Determines whether a food portion aligns with a personalised diet plan

These dataclasses provide a structured, type-safe vocabulary that can be used
to assemble datasets, persist annotations, and feed downstream model training
pipelines.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import random


class Gender(Enum):
    """Biological sex/gender options captured for BMR calculations."""

    FEMALE = "female"
    MALE = "male"
    NON_BINARY = "non_binary"
    UNSPECIFIED = "unspecified"


class Ethnicity(Enum):
    """High-level ethnicity groupings for population-specific nutrition heuristics."""

    AFRICAN = "african"
    ASIAN = "asian"
    EUROPEAN = "european"
    HISPANIC = "hispanic"
    MIDDLE_EASTERN = "middle_eastern"
    NATIVE = "native"
    OCEANIAN = "oceanian"
    OTHER = "other"
    UNSPECIFIED = "unspecified"


class ActivityLevel(Enum):
    """Activity multipliers typically used in calorie requirement estimation."""

    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    ATHLETE = "athlete"


class PortionEstimationMethod(Enum):
    """How the portion estimate was derived from the food image."""

    REFERENCE_OBJECT = "reference_object"
    DEPTH_SENSOR = "depth_sensor"
    MULTI_VIEW = "multi_view"
    USER_INPUT = "user_input"
    MODEL_INFERRED = "model_inferred"


class ComplianceLabel(Enum):
    """Target labels for diet compliance classification."""

    COMPLIANT = "compliant"
    BORDERLINE = "borderline"
    NON_COMPLIANT = "non_compliant"


@dataclass(frozen=True)
class MacroNutrientProfile:
    """Macro nutrient representation in grams with an optional alcohol channel."""

    protein_g: float
    fat_g: float
    carbohydrates_g: float
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    alcohol_g: float = 0.0

    def total_macros_g(self) -> float:
        return self.protein_g + self.fat_g + self.carbohydrates_g + self.fiber_g + self.sugar_g + self.alcohol_g


@dataclass(frozen=True)
class NutrientProfile:
    """Consolidated nutrient profile for an ingredient or a full meal."""

    calories_kcal: float
    macronutrients: MacroNutrientProfile
    micronutrients_mg: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, float]:
        """Flatten macro + micro nutrients for ML friendly structures."""

        flattened = {
            "calories_kcal": self.calories_kcal,
            "protein_g": self.macronutrients.protein_g,
            "fat_g": self.macronutrients.fat_g,
            "carbohydrates_g": self.macronutrients.carbohydrates_g,
            "fiber_g": self.macronutrients.fiber_g,
            "sugar_g": self.macronutrients.sugar_g,
            "alcohol_g": self.macronutrients.alcohol_g,
        }
        for name, value in self.micronutrients_mg.items():
            flattened[f"micro_{name}_mg"] = value
        return flattened


@dataclass(frozen=True)
class IngredientAnnotation:
    """Ingredient-level annotation extracted from a recipe or detection model."""

    ingredient_id: str
    display_name: str
    quantity_g: float
    preparation: Optional[str]
    nutrient_profile: NutrientProfile


@dataclass(frozen=True)
class RecipeStep:
    """Individual recipe instruction step."""

    order: int
    instruction: str


@dataclass(frozen=True)
class Recipe:
    """Recipe metadata used as ground truth for retrieval tasks."""

    recipe_id: str
    title: str
    cuisine: str
    source_url: Optional[str]
    steps: Tuple[RecipeStep, ...]


@dataclass(frozen=True)
class FoodImageContext:
    """Metadata describing an annotated food image."""

    image_id: str
    image_path: str
    captured_at_iso: Optional[str]
    lighting: Optional[str]
    surface: Optional[str]
    reference_objects: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PortionEstimate:
    """Estimated portion derived from the image analysis pipeline."""

    method: PortionEstimationMethod
    weight_g: Optional[float]
    volume_ml: Optional[float]
    confidence: float


@dataclass(frozen=True)
class DietRestriction:
    """A named restriction expressed against a specific nutrient target."""

    name: str
    nutrient_key: str
    max_value: Optional[float]
    min_value: Optional[float]
    unit: str
    per: str = "per_day"
    notes: Optional[str] = None


@dataclass(frozen=True)
class DietPlan:
    """User-specified or clinician-defined diet plan targets."""

    plan_id: str
    title: str
    total_calories_per_day: float
    macro_split_percent: Dict[str, float]
    restrictions: Tuple[DietRestriction, ...]
    notes: Optional[str] = None


@dataclass(frozen=True)
class UserHealthParameters:
    """Anthropometric and demographic descriptors required for calorie baselines."""

    user_id: str
    height_cm: float
    weight_kg: float
    age_years: int
    gender: Gender
    ethnicity: Ethnicity
    activity_level: ActivityLevel
    health_conditions: Tuple[str, ...] = field(default_factory=tuple)

    def bmi(self) -> float:
        """Compute body mass index."""

        height_m = self.height_cm / 100
        return self.weight_kg / (height_m * height_m)


@dataclass(frozen=True)
class ComplianceAssessment:
    """Ground truth signal for compliance classification tasks."""

    label: ComplianceLabel
    score: float
    rationale: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DietManagerExample:
    """Single multi-task example linking user context, food image, and annotations."""

    example_id: str
    user: UserHealthParameters
    diet_plan: DietPlan
    image: FoodImageContext
    detected_food_label: str
    recipe: Recipe
    ingredients: Tuple[IngredientAnnotation, ...]
    portion: Optional[PortionEstimate]
    nutrient_profile: NutrientProfile
    compliance: ComplianceAssessment
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_targets(self) -> Dict[str, object]:
        """Export dictionary of task-specific targets for model training."""

        return {
            "food_classification": self.detected_food_label,
            "recipe_retrieval": self.recipe.recipe_id,
            "ingredients": [asdict(ingredient) for ingredient in self.ingredients],
            "nutrients": self.nutrient_profile.to_dict(),
            "portion": asdict(self.portion) if self.portion else None,
            "compliance_label": self.compliance.label.value,
            "compliance_score": self.compliance.score,
        }


def split_train_test(
    examples: Sequence[DietManagerExample],
    test_ratio: float = 0.2,
    seed: Optional[int] = None,
) -> Tuple[List[DietManagerExample], List[DietManagerExample]]:
    """Randomly split examples into train and test subsets."""

    if not 0 < test_ratio < 1:
        raise ValueError("test_ratio must be between 0 and 1")

    examples_list = list(examples)
    if seed is not None:
        random.Random(seed).shuffle(examples_list)
    else:
        random.shuffle(examples_list)

    split_index = int(len(examples_list) * (1 - test_ratio))
    train_examples = examples_list[:split_index]
    test_examples = examples_list[split_index:]
    return train_examples, test_examples


@dataclass
class DietManagerDataset:
    """Container for train and test splits with dataset-level metadata."""

    train_examples: List[DietManagerExample]
    test_examples: List[DietManagerExample]
    version: str
    description: Optional[str] = None

    def task_targets(self, split: str) -> Iterable[Dict[str, object]]:
        """Yield task-aligned target dictionaries for a given split."""

        if split not in {"train", "test"}:
            raise ValueError("split must be 'train' or 'test'")

        selected = self.train_examples if split == "train" else self.test_examples
        for example in selected:
            yield example.to_targets()


__all__ = [
    "ActivityLevel",
    "ComplianceAssessment",
    "ComplianceLabel",
    "DietManagerDataset",
    "DietManagerExample",
    "DietPlan",
    "DietRestriction",
    "Ethnicity",
    "FoodImageContext",
    "Gender",
    "IngredientAnnotation",
    "MacroNutrientProfile",
    "NutrientProfile",
    "PortionEstimate",
    "PortionEstimationMethod",
    "Recipe",
    "RecipeStep",
    "split_train_test",
    "UserHealthParameters",
]


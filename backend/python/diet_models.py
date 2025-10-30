"""Domain data models for Diet Manager experimentation.

This module defines structured python representations to support model
training and testing for a diet management assistant.  The types capture
user health context, diet plans, computer vision outputs, and nutritional
analysis so datasets can be exchanged cleanly between stages such as image
classification, recipe retrieval, and compliance evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class Gender(str, Enum):
    """Gender options with string compatibility for serialization."""

    FEMALE = "female"
    MALE = "male"
    NON_BINARY = "non_binary"
    UNSPECIFIED = "unspecified"


class Ethnicity(str, Enum):
    """Simplified ethnicity buckets to contextualize nutritional guidance."""

    AFRICAN = "african"
    EAST_ASIAN = "east_asian"
    SOUTH_ASIAN = "south_asian"
    EUROPEAN = "european"
    LATIN_AMERICAN = "latin_american"
    MIDDLE_EASTERN = "middle_eastern"
    INDIGENOUS = "indigenous"
    OTHER = "other"


@dataclass(frozen=True)
class HealthParameters:
    """Baseline user attributes used to compute daily requirements."""

    height_cm: float
    weight_kg: float
    age_years: int
    gender: Gender
    ethnicity: Ethnicity


@dataclass(frozen=True)
class DietRestriction:
    """Individual nutrient constraint within a diet plan."""

    name: str
    max_value_per_day: Optional[float] = None
    min_value_per_day: Optional[float] = None
    unit: str = "g"


@dataclass(frozen=True)
class DietPlan:
    """User defined or clinician prescribed dietary requirements."""

    name: str
    total_calories_per_day: float
    restrictions: List[DietRestriction] = field(default_factory=list)


@dataclass(frozen=True)
class NutrientProfile:
    """Macro and micro nutrient composition for a food item."""

    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float


class PortionEstimationMethod(str, Enum):
    """Detection techniques for estimating serving size."""

    REFERENCE_OBJECT = "reference_object"
    SENSOR_DEPTH = "sensor_depth"
    USER_INPUT = "user_input"
    MODEL_ESTIMATE = "model_estimate"


@dataclass(frozen=True)
class PortionEstimate:
    """Estimated portion size for the observed meal."""

    method: PortionEstimationMethod
    estimated_weight_g: float
    confidence: float
    reference_notes: Optional[str] = None


@dataclass(frozen=True)
class Ingredient:
    """Single ingredient with measured quantity and nutritional profile."""

    name: str
    quantity: float
    unit: str
    preparation: Optional[str] = None
    nutrients: Optional[NutrientProfile] = None


@dataclass(frozen=True)
class Recipe:
    """Structured cooking recipe derived from the detected food."""

    title: str
    cuisine: Optional[str]
    description: Optional[str]
    ingredients: List[Ingredient]
    instructions: Optional[List[str]] = None


@dataclass(frozen=True)
class FoodIdentification:
    """Vision model output describing cuisine and dish candidates."""

    predicted_label: str
    confidence: float
    cuisine: Optional[str] = None
    alternate_labels: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class FoodImageSample:
    """Training sample linking an image to its nutritional ground truth."""

    image_path: Path
    identification: FoodIdentification
    recipe: Recipe
    portion: PortionEstimate
    total_nutrients: NutrientProfile


class ComplianceStatus(str, Enum):
    """Outcome classes for diet compliance evaluation."""

    COMPLIANT = "compliant"
    EXCEEDS_LIMITS = "exceeds_limits"
    BELOW_REQUIRED = "below_required"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass(frozen=True)
class ComplianceAnalysis:
    """Evaluation comparing meal nutrients with a diet plan."""

    diet_plan: DietPlan
    user_health: HealthParameters
    consumed_nutrients: NutrientProfile
    status: ComplianceStatus
    triggered_restrictions: List[str] = field(default_factory=list)
    recommendations: Optional[List[str]] = None


@dataclass(frozen=True)
class InferenceRecord:
    """Bundle prediction data for benchmarking and offline analysis."""

    sample: FoodImageSample
    predicted_nutrients: NutrientProfile
    predicted_status: ComplianceStatus
    compliance_analysis: Optional[ComplianceAnalysis] = None


@dataclass(frozen=True)
class UserDietSession:
    """End-to-end dataset row combining user input with meal assessment."""

    user_id: str
    health: HealthParameters
    diet_plan: DietPlan
    meals: List[InferenceRecord]


__all__ = [
    "ComplianceAnalysis",
    "ComplianceStatus",
    "DietPlan",
    "DietRestriction",
    "Ethnicity",
    "FoodIdentification",
    "FoodImageSample",
    "Gender",
    "HealthParameters",
    "InferenceRecord",
    "Ingredient",
    "NutrientProfile",
    "PortionEstimate",
    "PortionEstimationMethod",
    "Recipe",
    "UserDietSession",
]

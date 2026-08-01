from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE
from app.prompts.coding import build_coding_prompt
from app.prompts.behavioral import build_behavioral_prompt
from app.prompts.programming import build_programming_prompt
from app.prompts.database import build_database_prompt
from app.prompts.systems import build_systems_prompt
from app.prompts.system_design import build_system_design_prompt
from app.prompts.backend import build_backend_prompt
from app.prompts.cloud import build_cloud_prompt
from app.prompts.ai import build_ai_prompt
from app.prompts.career import build_career_prompt
from app.prompts.general import build_general_prompt


# Behavioral
BEHAVIORAL_CATEGORIES = {
    Category.BEHAVIORAL,
    Category.LEADERSHIP,
    Category.COMMUNICATION,
}

# Programming Fundamentals
PROGRAMMING_CATEGORIES = {
    Category.PROGRAMMING,
    Category.OBJECT_ORIENTED_PROGRAMMING,
}

# Coding / Algorithms
CODING_CATEGORIES = {
    Category.ARRAYS,
    Category.STRINGS,
    Category.HASH_TABLES,
    Category.LINKED_LISTS,
    Category.STACKS,
    Category.QUEUES,
    Category.TREES,
    Category.HEAPS,
    Category.TRIES,
    Category.GRAPHS,
    Category.SORTING,
    Category.SEARCHING,
    Category.RECURSION,
    Category.BACKTRACKING,
    Category.GREEDY,
    Category.DYNAMIC_PROGRAMMING,
    Category.DIVIDE_AND_CONQUER,
    Category.BIT_MANIPULATION,
    Category.MATH,
}

# Databases
DATABASE_CATEGORIES = {
    Category.DATABASES,
    Category.SQL,
}

# Computer Systems
SYSTEMS_CATEGORIES = {
    Category.OPERATING_SYSTEMS,
    Category.NETWORKING,
    Category.CONCURRENCY,
    Category.COMPUTER_ARCHITECTURE,
}

# System Design
SYSTEM_DESIGN_CATEGORIES = {
    Category.SYSTEM_DESIGN,
    Category.LOW_LEVEL_DESIGN,
    Category.DESIGN_PATTERNS,
}

# Backend / Software Engineering
BACKEND_CATEGORIES = {
    Category.API_DESIGN,
    Category.MICROSERVICES,
    Category.TESTING,
    Category.SECURITY,
}

# Cloud / DevOps
CLOUD_CATEGORIES = {
    Category.CLOUD_COMPUTING,
    Category.DEVOPS,
}

# AI / Machine Learning
AI_CATEGORIES = {
    Category.MACHINE_LEARNING,
    Category.DEEP_LEARNING,
    Category.NATURAL_LANGUAGE_PROCESSING,
    Category.COMPUTER_VISION,
    Category.GENERATIVE_AI,
    Category.LARGE_LANGUAGE_MODELS,
    Category.RAG,
    Category.VECTOR_DATABASES,
    Category.PROMPT_ENGINEERING,
}

# Career
CAREER_CATEGORIES = {
    Category.RESUME,
    Category.PROJECTS,
}


class PromptBuilder:
    @staticmethod
    def build(
        category: Category,
        difficulty: Difficulty,
    ) -> str:

        if category in CODING_CATEGORIES:
            return build_coding_prompt(category, difficulty)
        elif category in BEHAVIORAL_CATEGORIES:
            return build_behavioral_prompt(category, difficulty)
        elif category in PROGRAMMING_CATEGORIES:
            return build_programming_prompt(category, difficulty)
        elif category in DATABASE_CATEGORIES:
            return build_database_prompt(category, difficulty)
        elif category in SYSTEMS_CATEGORIES:
            return build_systems_prompt(category, difficulty)
        elif category in SYSTEM_DESIGN_CATEGORIES:
            return build_system_design_prompt(category, difficulty)
        elif category in BACKEND_CATEGORIES:
            return build_backend_prompt(category, difficulty)
        elif category in CLOUD_CATEGORIES:
            return build_cloud_prompt(category, difficulty)
        elif category in AI_CATEGORIES:
            return build_ai_prompt(category, difficulty)
        elif category in CAREER_CATEGORIES:
            return build_career_prompt(category, difficulty)
        else:
            return build_general_prompt(category, difficulty)

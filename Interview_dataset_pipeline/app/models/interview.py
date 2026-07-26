'''
| Field        | Decision                | Reason                                 |
| ------------ | ----------------------- | -------------------------------------- |
| `id`         | Integer                 | Unique identifier                      |
| `question`   | String                  | Variable-length text                   |
| `answer`     | String                  | Variable-length text                   |
| `difficulty` | Enum                    | Prevent invalid values                 |
| `category`   | Enum (for this project) | We control the taxonomy                |
| `company`    | Optional string         | Not every question is company-specific |
| `tags`       | List of strings         | A question can have multiple tags      |
| `created_at` | Timestamp               | Useful for tracking generation         |
'''

from enum import Enum
from datetime import datetime, timezone
import time
from typing import Optional
from unicodedata import category
from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


class Category(str, Enum):
    # Behavioral
    BEHAVIORAL = "Behavioral"

    # Programming Fundamentals
    PROGRAMMING = "Programming"
    OBJECT_ORIENTED_PROGRAMMING = "Object-Oriented Programming"

    # Data Structures
    ARRAYS = "Arrays"
    STRINGS = "Strings"
    HASH_TABLES = "Hash Tables"
    LINKED_LISTS = "Linked Lists"
    STACKS = "Stacks"
    QUEUES = "Queues"
    TREES = "Trees"
    HEAPS = "Heaps"
    TRIES = "Tries"
    GRAPHS = "Graphs"

    # Algorithms
    SORTING = "Sorting"
    SEARCHING = "Searching"
    RECURSION = "Recursion"
    BACKTRACKING = "Backtracking"
    GREEDY = "Greedy Algorithms"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    DIVIDE_AND_CONQUER = "Divide and Conquer"
    BIT_MANIPULATION = "Bit Manipulation"
    MATH = "Mathematics"

    # Computer Science Fundamentals
    DATABASES = "Databases"
    SQL = "SQL"
    OPERATING_SYSTEMS = "Operating Systems"
    NETWORKING = "Networking"
    CONCURRENCY = "Concurrency"
    COMPUTER_ARCHITECTURE = "Computer Architecture"

    # Software Engineering
    SYSTEM_DESIGN = "System Design"
    LOW_LEVEL_DESIGN = "Low-Level Design"
    DESIGN_PATTERNS = "Design Patterns"
    API_DESIGN = "API Design"
    MICROSERVICES = "Microservices"
    CLOUD_COMPUTING = "Cloud Computing"
    DEVOPS = "DevOps"
    TESTING = "Testing"
    SECURITY = "Security"

    # AI / ML
    MACHINE_LEARNING = "Machine Learning"
    DEEP_LEARNING = "Deep Learning"
    NATURAL_LANGUAGE_PROCESSING = "Natural Language Processing"
    COMPUTER_VISION = "Computer Vision"
    GENERATIVE_AI = "Generative AI"
    LARGE_LANGUAGE_MODELS = "Large Language Models"
    RAG = "Retrieval-Augmented Generation"
    VECTOR_DATABASES = "Vector Databases"
    PROMPT_ENGINEERING = "Prompt Engineering"

    # Career
    RESUME = "Resume"
    PROJECTS = "Projects"
    LEADERSHIP = "Leadership"
    COMMUNICATION = "Communication"
    

class InterviewExample(BaseModel):
    id: int
    question: str
    answer: str
    
    difficulty: Difficulty
    category: Category
    
    company: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
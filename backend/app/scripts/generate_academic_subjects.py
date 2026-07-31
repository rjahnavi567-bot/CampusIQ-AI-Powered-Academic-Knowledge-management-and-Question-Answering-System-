from app.knowledge_base.common_subjects import COMMON_SUBJECTS
from app.knowledge_base.cse import CSE_SUBJECTS
from app.knowledge_base.aiml import AIML_SUBJECTS
from app.knowledge_base.data_science import DATA_SCIENCE_SUBJECTS
from app.knowledge_base.cyber_security import CYBER_SECURITY_SUBJECTS
from app.knowledge_base.it import IT_SUBJECTS
from app.knowledge_base.ece import ECE_SUBJECTS
from app.knowledge_base.eee import EEE_SUBJECTS
from app.knowledge_base.mechanical import MECHANICAL_SUBJECTS
from app.knowledge_base.mechanical_robotics import MECHANICAL_ROBOTICS_SUBJECTS
from app.knowledge_base.civil import CIVIL_SUBJECTS
from app.knowledge_base.chemical import CHEMICAL_SUBJECTS

ALL_SUBJECTS = []

ALL_SUBJECTS.extend(COMMON_SUBJECTS)
ALL_SUBJECTS.extend(CSE_SUBJECTS)
ALL_SUBJECTS.extend(AIML_SUBJECTS)
ALL_SUBJECTS.extend(DATA_SCIENCE_SUBJECTS)
ALL_SUBJECTS.extend(CYBER_SECURITY_SUBJECTS)
ALL_SUBJECTS.extend(IT_SUBJECTS)
ALL_SUBJECTS.extend(ECE_SUBJECTS)
ALL_SUBJECTS.extend(EEE_SUBJECTS)
ALL_SUBJECTS.extend(MECHANICAL_SUBJECTS)
ALL_SUBJECTS.extend(MECHANICAL_ROBOTICS_SUBJECTS)
ALL_SUBJECTS.extend(CIVIL_SUBJECTS)
ALL_SUBJECTS.extend(CHEMICAL_SUBJECTS)

print(f"Total Subjects: {len(ALL_SUBJECTS)}")
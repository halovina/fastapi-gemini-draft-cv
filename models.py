from pydantic import BaseModel

# --- Model Data untuk Input Pengguna ---
class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str = "Present"
    responsibilities: list[str]

class Education(BaseModel):
    degree: str
    university: str
    start_date: str
    end_date: str

class Skill(BaseModel):
    name: str
    level: str = "Advanced" # Contoh: Beginner, Intermediate, Advanced

class UserResumeInput(BaseModel):
    full_name: str
    email: str
    phone: str = None
    linkedin_profile: str = None
    summary_objective: str = None
    experiences: list[Experience] = []
    education: list[Education] = []
    skills: list[Skill] = []
    achievements: list[str] = [] # Tambahan untuk pencapaian spesifik
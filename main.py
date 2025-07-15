import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from models import UserResumeInput

# Muat variabel  dari file .env
load_dotenv()

# Konfigurasi Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

app = FastAPI(
    title="API Otomatisasi Pembuatan Résumé/CV",
    description="Menerima detail pengalaman, pendidikan, dan keahlian dari pengguna, lalu menggunakan Gemini untuk membuat draf résumé atau CV yang profesional."
)



# --- Endpoint API ---
@app.post("/generate_resume/")
async def generate_resume(user_input: UserResumeInput):
    """
    Menerima detail pengalaman, pendidikan, dan keahlian dari pengguna,
    lalu menggunakan Gemini untuk membuat draf résumé atau CV.
    """
    try:
        # Bangun prompt untuk Gemini
        prompt_parts = [
            f"Sebagai AI profesional pembuat résumé/CV, buatkan draf résumé/CV yang menarik dan profesional berdasarkan informasi berikut. "
            f"Pastikan untuk menonjolkan poin-poin penting dan menggunakan format yang mudah dibaca.\n\n"
            f"**Nama Lengkap:** {user_input.full_name}\n"
            f"**Email:** {user_input.email}\n"
        ]
        if user_input.phone:
            prompt_parts.append(f"**Telepon:** {user_input.phone}\n")
        if user_input.linkedin_profile:
            prompt_parts.append(f"**Profil LinkedIn:** {user_input.linkedin_profile}\n")
        
        if user_input.summary_objective:
            prompt_parts.append(f"\n**Ringkasan/Tujuan Karir:**\n{user_input.summary_objective}\n")
        
        if user_input.experiences:
            prompt_parts.append("\n**Pengalaman Kerja:**\n")
            for exp in user_input.experiences:
                prompt_parts.append(f"- **{exp.title}** di {exp.company} ({exp.start_date} - {exp.end_date})\n")
                if exp.responsibilities:
                    prompt_parts.append("  Tanggung Jawab:\n")
                    for resp in exp.responsibilities:
                        prompt_parts.append(f"    * {resp}\n")

        if user_input.education:
            prompt_parts.append("\n**Pendidikan:**\n")
            for edu in user_input.education:
                prompt_parts.append(f"- **{edu.degree}** dari {edu.university} ({edu.start_date} - {edu.end_date})\n")

        if user_input.skills:
            prompt_parts.append("\n**Keahlian:**\n")
            for skill in user_input.skills:
                prompt_parts.append(f"- {skill.name} ({skill.level})\n")
        
        if user_input.achievements:
            prompt_parts.append("\n**Pencapaian (Opsional):**\n")
            for achievement in user_input.achievements:
                prompt_parts.append(f"- {achievement}\n")

        full_prompt = "".join(prompt_parts)

        # Minta Gemini untuk membuat résumé
        response = model.generate_content(full_prompt)
        
        if not response.parts:
            raise HTTPException(status_code=500, detail="Gemini tidak menghasilkan konten.")

        # Ambil teks dari respons Gemini
        resume_content = response.text

        return {"status": "success", "resume_draft": resume_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


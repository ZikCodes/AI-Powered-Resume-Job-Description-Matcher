import fitz
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


#Text extraction from pdf
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
        
    return text



def get_results_back(user_resume, job_description):
    
    try:
    
        #Key prompt for the whole project
        
        user_prompt = f"""
        Act as an expert Technical Recruiter, ATS Specialist, and AI Resume Parser.

        Your task is to analyze a candidate's resume against a targeted Job Description (JD), but **FIRST validate that both inputs are usable and appropriate for resume matching**.

        You must follow the validation rules below before performing any scoring or comparison.

        ---

        # INPUT DATA

        <resume>
        {user_resume}
        </resume>

        <job_description>
        {job_description}
        </job_description>

        ---

        # STEP 1 — INPUT VALIDATION

        Before analyzing the resume or calculating any scores, determine whether each input is valid.

        ## Resume is VALID if:

        The text appears to contain meaningful information about a candidate's professional, academic, technical, or project background.

        A valid resume may contain some or all of:

        * Candidate name
        * Contact information
        * Professional summary
        * Work experience
        * Internships
        * Education
        * Projects
        * Technical skills
        * Certifications
        * Achievements
        * Volunteer experience
        * Relevant coursework

        A resume does NOT need to be professionally formatted or complete to be valid.

        A resume should NOT be considered invalid merely because:

        * It has few skills.
        * It has little experience.
        * It is poorly written.
        * It has spelling mistakes.
        * It is missing contact information.
        * It is missing work experience.
        * It is a student resume.
        * It is an entry-level resume.
        * It does not match the JD well.

        ## Resume is INVALID if:

        Examples include:

        * Empty or nearly empty input.
        * Placeholder text such as "[PASTE RESUME HERE]".
        * Random/unrelated text.
        * A job description accidentally supplied as the resume.
        * A generic question or conversation instead of a resume.
        * Text that contains insufficient information to identify it as a candidate profile.
        * Corrupted or unintelligible content.

        ---

        ## Job Description is VALID if:

        The text appears to describe a real job, internship, apprenticeship, contract role, or professional position.

        A valid JD may contain:

        * Job title
        * Responsibilities
        * Required qualifications
        * Preferred qualifications
        * Technical skills
        * Soft skills
        * Experience requirements
        * Education requirements
        * Tools/frameworks/platforms
        * Job duties
        * Company/team information

        A JD does NOT need to contain all of these.

        ## Job Description is INVALID if:

        Examples include:

        * Empty or nearly empty input.
        * Placeholder text such as "[PASTE JOB DESCRIPTION HERE]".
        * Random/unrelated text.
        * A resume accidentally supplied as the JD.
        * A generic question or conversation instead of a job description.
        * Text that contains insufficient information to identify an actual job opportunity.
        * Corrupted or unintelligible content.

        ---

        # STEP 2 — DETERMINE INPUT STATUS

        Classify the input into exactly ONE of these statuses:

        * `VALID`
        * `INVALID_RESUME`
        * `INVALID_JOB_DESCRIPTION`
        * `INVALID_BOTH`

        Rules:

        ### If both are valid:

        Return `VALID` and perform the full resume-to-JD analysis.

        ### If resume is invalid but JD is valid:

        Return `INVALID_RESUME`.

        ### If resume is valid but JD is invalid:

        Return `INVALID_JOB_DESCRIPTION`.

        ### If both are invalid:

        Return `INVALID_BOTH`.

        Do NOT perform matching or generate scores when either required input is invalid.

        Do NOT attempt to "fix" or infer a missing resume/JD.

        ---

        # STEP 3 — INVALID INPUT RESPONSE

        If the input is invalid, return ONLY the following JSON structure:

        {{
        "status": "INVALID_RESUME",
        "message": "The provided resume is missing or does not contain enough information to identify it as a candidate resume.",
        "scores": null,
        "keywords": null,
        "skill_breakdown": null,
        "recommendations": []
        }}

        Replace `status` and `message` appropriately depending on the validation result.

        For example:

        {{
        "status": "INVALID_JOB_DESCRIPTION",
        "message": "The provided job description is missing or does not contain enough information to identify it as a job description.",
        "scores": null,
        "keywords": null,
        "skill_breakdown": null,
        "recommendations": []
        }}

        For both invalid:

        {{
        "status": "INVALID_BOTH",
        "message": "Both the resume and job description are missing, invalid, or contain insufficient information for comparison.",
        "scores": null,
        "keywords": null,
        "skill_breakdown": null,
        "recommendations": []
        }}

        Do not include additional fields for invalid inputs.

        ---

        # STEP 4 — VALID INPUT ANALYSIS

        Only if BOTH inputs are valid, analyze the candidate's resume against the JD.

        Return raw JSON only.

        Do not use Markdown.

        Do not wrap the JSON in ```json unless the calling application explicitly requires Markdown code blocks.

        ---

        # 1. SCORES

        Calculate real scores based ONLY on information contained in the provided resume and JD.

        ```text
        scores:
        overall_match: Integer 0-100
        hard_skills_match: Integer 0-100
        soft_skills_match: Integer 0-100
        ```

        ## Hard Skills Match

        Evaluate technical and job-specific requirements such as:

        * Programming languages
        * Frameworks
        * Libraries
        * Databases
        * Cloud platforms
        * DevOps tools
        * APIs
        * Development methodologies
        * Software/tools
        * Certifications
        * Technical domains
        * Required technical qualifications

        Do not award credit for a skill that is not supported by the resume.

        ## Soft Skills Match

        Evaluate explicitly stated or reasonably supported evidence for:

        * Communication
        * Leadership
        * Teamwork
        * Collaboration
        * Problem solving
        * Adaptability
        * Project management
        * Time management
        * Mentoring
        * Stakeholder management

        Do not assume a soft skill simply because the candidate has worked in a professional environment.

        ## Overall Match

        The overall score should reflect the candidate's total alignment with the JD, including:

        * Hard skills
        * Soft skills
        * Relevant experience
        * Education
        * Projects
        * Certifications
        * Responsibilities
        * Seniority/experience level
        * Job-specific requirements

        The score must be evidence-based.

        Do not inflate scores simply because the resume contains many keywords.

        ---

        # 2. KEYWORD AND SKILL MATCHING

        Return:

        ```text
        keywords:
        matched: []
        missing: []
        ```

        ## matched

        Include important skills, technologies, qualifications, tools, and job-specific terms that are supported by BOTH:

        1. The JD
        2. The resume

        Normalize obvious variations where appropriate.

        For example:

        * "Python programming" and "Python" → `Python`
        * "Amazon Web Services" and "AWS" → `AWS`
        * "PostgreSQL database" and "PostgreSQL" → `PostgreSQL`
        * "RESTful APIs" and "REST API" → `REST APIs`

        Do not count unrelated words as matches.

        ## missing

        Include important requirements from the JD that are not supported by the resume.

        Prioritize:

        1. Required technical skills
        2. Required qualifications
        3. Required experience
        4. Important tools/platforms
        5. Important responsibilities
        6. Relevant soft skills

        Do NOT include every minor word from the JD.

        Do NOT mark a skill as missing if the resume clearly demonstrates equivalent experience using different terminology.

        Do NOT assume that a skill is present simply because it is commonly associated with another skill.

        ---

        # 3. SKILL BREAKDOWN

        Return:

        ```text
        skill_breakdown:
        matched_skills_count: Integer
        missing_skills_count: Integer
        top_categories: []
        ```

        `matched_skills_count` must equal the number of items in `keywords.matched`.

        `missing_skills_count` must equal the number of items in `keywords.missing`.

        Categorize the candidate's alignment into relevant categories.

        Examples:

        * Programming Languages
        * Backend Development
        * Frontend Development
        * Databases
        * Cloud & Infrastructure
        * DevOps & CI/CD
        * AI & Machine Learning
        * Data Engineering
        * Data Analysis
        * APIs & Integrations
        * Testing & Quality
        * Security
        * Project Management
        * Communication
        * Leadership

        Each category must have exactly one of:

        * `Strong`
        * `Moderate`
        * `Weak`

        Only include categories relevant to the JD.

        ---

        # 4. RECOMMENDATIONS

        Return an array of specific, actionable recommendations.

        Recommendations should be based on actual gaps identified between the resume and JD.

        Good examples:

        * "Add PostgreSQL to the Skills section if you have actual experience using it."
        * "Quantify the impact of your backend projects with measurable results such as latency reduction, throughput, users served, or deployment frequency."
        * "Move your Python and FastAPI experience higher in the resume because both are directly relevant to the target role."
        * "If you have AWS experience, explicitly mention the AWS services used rather than listing only 'AWS'."
        * "Add testing technologies such as pytest only if you have actually used them."

        Avoid vague recommendations such as:

        * "Improve your resume."
        * "Add more skills."
        * "Make your resume better."

        NEVER recommend adding a technology, qualification, experience, certification, or achievement that the candidate does not actually have.

        If a recommendation depends on experience that is not confirmed, explicitly phrase it conditionally using language such as:

        "If you have experience with X, consider adding it..."

        ---

        # IMPORTANT ANTI-HALLUCINATION RULES

        1. Use ONLY information present in the supplied resume and JD.
        2. Never invent candidate experience.
        3. Never assume that a candidate knows a technology because they know a related technology.
        4. Never treat keyword stuffing as genuine experience.
        5. Do not give credit for a skill unless the resume provides evidence for it.
        6. Do not penalize a candidate for missing information that the JD does not require.
        7. Distinguish between:

        * skill explicitly stated,
        * skill demonstrated through experience/project,
        * skill implied by closely equivalent terminology.
        8. If evidence is ambiguous, do not assume the candidate has the skill.
        9. A poor match is NOT an invalid resume.
        10. A junior or inexperienced candidate is NOT an invalid resume.
        11. An incomplete resume can still be valid if there is enough information to identify it as a candidate profile.
        12. Do not calculate scores until BOTH inputs pass validation.

        ---

        # OUTPUT SCHEMA — VALID INPUTS

        Return exactly this JSON structure:

        {{
        "status": "VALID",
        "scores": {{
        "overall_match": 82,
        "hard_skills_match": 78,
        "soft_skills_match": 90
        }},
        
        "keywords": {{
        "matched": [
        "Python",
        "FastAPI",
        "REST APIs",
        "Git",
        "Docker"
        ],
        "missing": [
        "Kubernetes",
        "GraphQL",
        "AWS S3"
        ]
        }},
        "skill_breakdown": {{
        "matched_skills_count": 5,
        "missing_skills_count": 3,
        "top_categories": [
        {{
        "category": "Programming Languages",
        "status": "Strong"
        }},
        {{
        "category": "Backend Development",
        "status": "Strong"
        }},
        {{
        "category": "Cloud & Infrastructure",
        "status": "Weak"
        }}
        ]
        }},
        "recommendations": [
        "Highlight your FastAPI and REST API experience more prominently because they are directly relevant to the target role.",
        "If you have AWS experience, explicitly list the AWS services you have used.",
        "Quantify the results of your backend projects using measurable metrics where possible."
        ]
        }}

        ---

        # FINAL REQUIREMENT

        Your response MUST be valid JSON.

        For valid inputs, the top-level `status` MUST be `VALID`.

        For invalid inputs, return the appropriate invalid status and DO NOT provide scores.

        Never return explanatory text outside the JSON object. 
        """
        
        API_KEY = os.getenv("API_KEY") #Load API_KEY from .env file
        URL = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "openrouter/free", #Free random model from openrouter
            "messages": [
                {
                    "role":"user",
                    "content": f"{user_prompt}"
                }
            ]
        }
        response = requests.post(URL, headers=headers, json=payload)
        
        if response.status_code == 200:
                response_data = response.json()
                reply = response_data["choices"][0]["message"]["content"]
                data = json.loads(reply)
                keywords = data.get("keywords") or {}
                recommendations = data.get("recommendations") or {}
                scores = data.get("scores") or {}
                status = data.get("status") or {}
                matched = keywords.get("matched",[])
                missing = keywords.get("missing",[])
                skill_breakdown = data.get("skill_breakdown") or {}
                
                return matched, missing, recommendations, scores, status, skill_breakdown
            
        else:
            return response.status_code
    
    
    
    except Exception:
        pass

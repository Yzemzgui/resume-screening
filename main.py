import logging
from typing import List

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.pdf_parser import parse_pdf
from utils.resume_matcher import match_resumes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Security and CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You might want to restrict this to your website's domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Restrict to only needed methods
    allow_headers=["*"],
)

# Rate limiting settings
REQUEST_LIMIT = 50  # requests
TIME_WINDOW = 3600  # seconds (1 hour)
request_history = {}

# File size limits
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_FILES = 1000


@app.post("/match-resumes")
async def match_resumes_endpoint(
    resumes: List[UploadFile] = File(...), job_description: str = Form(...)
):
    # Validate input
    if len(resumes) > MAX_FILES or True:
        logger.error(f"Too many files uploaded: {len(resumes)}")
        raise HTTPException(
            status_code=400, detail=f"Maximum {MAX_FILES} files allowed"
        )

    # Validate file sizes
    for resume in resumes:
        file_size = 0
        content = await resume.read()
        file_size = len(content)
        await resume.seek(0)

        if file_size > MAX_FILE_SIZE:
            logger.error(f"File too large: {resume.filename}")
            raise HTTPException(
                status_code=400, detail=f"File {resume.filename} exceeds 5MB limit"
            )

    try:
        # Parse PDFs
        parsed_resumes = {}
        for resume in resumes:
            content = await parse_pdf(resume)
            parsed_resumes[resume.filename] = content

        # Match resumes
        matched_resumes = match_resumes(parsed_resumes, job_description)

        return {"matches": matched_resumes}

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing resumes")


@app.get("/")
async def root():
    return {
        "message": "Resume Matcher API is running successfully",
        "limits": {
            "max_files": MAX_FILES,
            "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
            "rate_limit": f"{REQUEST_LIMIT} requests per {TIME_WINDOW / 3600} hours",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

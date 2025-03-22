# Resume Screening API

A FastAPI-based API that helps automate the process of screening resumes by matching them against a job description. This tool is particularly useful for organizations that receive a large number of resumes and need to efficiently identify the best candidates based on specific technical requirements.

## Features

- PDF resume parsing and analysis
- Automated matching against job descriptions
- Support for multiple resume uploads
- Rate limiting and file size restrictions
- CORS enabled for web integration
- Health check endpoint for monitoring

## Live Demo

You can test a more advanced version of the resume screening API here: [Resume Screening Tool](https://www.yzemzgui.com/resume-screening)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-screening.git
cd resume-screening
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the API

1. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /match-resumes
- Accepts multiple PDF resumes and a job description
- Returns matched resumes based on the job description
- Maximum file size: 5MB per file
- Maximum files: 1000

### GET /
- Returns API status and limits information

### GET /health
- Health check endpoint for monitoring

## API Limits

- Maximum file size: 5MB per file
- Maximum number of files: 1000
- Rate limit: 50 requests per hour

## Development

The project structure is organized as follows:
```
resume-screening/
├── main.py              # Main FastAPI application
├── requirements.txt     # Project dependencies
├── utils/              # Utility modules
│   ├── pdf_parser.py   # PDF parsing functionality
│   └── resume_matcher.py # Resume matching logic
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
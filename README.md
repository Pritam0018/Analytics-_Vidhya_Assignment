# ReadMe: Smart Course Search System

This project involves creating a **Smart Course Search System** using web scraping, Retrieval-Augmented Generation (RAG) development, and deployment on Hugging Face Spaces. The system leverages machine learning models and embeddings for enhanced search and response capabilities.

---

## Project Overview

The Smart Course Search System enables users to search for relevant courses based on their queries. The project pipeline includes:

1. **Web Scraping**: Extracting course data.
2. **Preprocessing**: Cleaning and preparing the scraped data.
3. **RAG Development**: Implementing the system using embeddings, vector search, and an LLM (Large Language Model).
4. **Deployment**: Hosting the application on Hugging Face Spaces.

---

## Prerequisites

Ensure the following tools and libraries are installed:

1. **Python**: Version 3.12.1.
2. **Virtual Environment**: Recommended to avoid dependency conflicts.
3. Required Python libraries:
    - `streamlit`
    - `pandas`
    - `langchain`
    - `langchain_huggingface`
    - `langchain_groq`
    - `langchain_community`
    - `faiss-cpu`
    - `python-dotenv`

---

## Steps to Build and Deploy the System

### Step 1: Web Scraping

#### Tools Required:
- **Python**
- **Libraries**: `requests`, `BeautifulSoup4`, `pandas`

#### Instructions:
1. Identify the website containing the course data.
2. Use `BeautifulSoup` to parse the HTML and extract course titles and descriptions.
3. Save the data in a CSV file (e.g., `analytics_vidhya_courses.csv`).

Example:
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.example.com/courses"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract course titles
courses = []
for course in soup.find_all("div", class_="course-title"):
    courses.append(course.text.strip())

# Save to CSV
pd.DataFrame({"title": courses}).to_csv("analytics_vidhya_courses.csv", index=False)
```

---

### Step 2: Preprocessing Data

1. Load the CSV file containing course titles.
2. Prepare the data for embedding by ensuring it contains clean text data in a `title` column.

---

### Step 3: RAG Development

#### Tools Required:
- **LangChain**
- **Embeddings**: Hugging Face
- **Vector Store**: FAISS
- **LLM**: Groq API

#### Implementation:
1. **Environment Setup**:
    - Create a `.env` file with your API keys:
      ```
      GROQ_API_KEY=your_groq_api_key
      HF_TOKEN=your_huggingface_token
      ```

2. **Vector Embedding**:
    - Load the course data and create vector embeddings.

3. **RAG Integration**:
    - Combine embeddings, vector search, and LLM responses for query answering.

4. **Streamlit Frontend**:
    - Use Streamlit to build the user interface.

---

### Step 4: Deployment on Hugging Face Spaces

#### Prerequisites:
- Hugging Face account.
- Install the `huggingface_hub` library.

#### Instructions:
1. **Prepare the Application**:
    - Save your Streamlit app as `app.py`.
    - Include the required libraries in `requirements.txt`.

2. **Upload to Hugging Face**:
    - Initialize a repository on Hugging Face Spaces.
    - Push your code to the repository.

3. **Run the Application**:
    - Your app will be live at `https://huggingface.co/spaces/<your-username>/<your-app>`.

Example `requirements.txt`:
```
streamlit
pandas
langchain
langchain_huggingface
langchain_groq
langchain_community
faiss-cpu
python-dotenv
```

---

## Usage

1. **Start the Application**:
   - Run the Streamlit app locally:
     ```bash
     streamlit run app.py
     ```

2. **Query the System**:
   - Enter a search query to find relevant courses.
   - View the system’s response and relevant course titles.

---

## Example Workflow

1. **Input**:
    - User query: *"Beginner Python courses"*
2. **Processing**:
    - The system searches for similar course titles using vector embeddings.
3. **Output**:
    - Displays 2-3 relevant courses:
      - *"Python Basics for Beginners"*
      - *"Introduction to Python Programming"*

---

## Directory Structure

```
SmartCourseSearch/
├── app.py                  # Main application file
├── requirements.txt        # Dependency file
├── analytics_vidhya_courses.csv # Course data
├── .env                    # API keys
└── README.md               # Project documentation
```

---

## Additional Notes

1. Ensure the CSV file is updated with the latest course data.
2. Use efficient embeddings (e.g., `all-MiniLM-L6-v2`) for faster processing.
3. Monitor the Hugging Face Spaces dashboard for logs and performance metrics.

---

## Python Version

This project is tested on **Python 3.12.1**.

---

## References

1. [LangChain Documentation](https://langchain.readthedocs.io/)
2. [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
3. [Streamlit Documentation](https://docs.streamlit.io/)

---

## Contact

For questions or suggestions, please contact [Your Name/Team].


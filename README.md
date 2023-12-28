# FastAPI Project
 script to fetch language content from a MongoDB

##### Prerequisites
- Python 3.11+
- Pip

##### 1. Check out the repository

clone the project or download the zip with the source code

##### 2. Install all dependencies

```bash
pip install -r requirements.txt
```

##### 3. Create a .env file and write a MongoDB connection string

```bash
DB_URL = "YOUR DB URL"
```

##### 4. Start the server

```bash
uvicorn main:app --reload
```


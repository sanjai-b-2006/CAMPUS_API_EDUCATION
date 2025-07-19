from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse 
from routers import courses, faculty, advanced

app = FastAPI(title="College Campus API", version="1.0")
app.include_router(courses.router)
app.include_router(faculty.router)
app.include_router(advanced.router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>College Campus API</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f7fafc; margin:0; }
            .container { max-width: 700px; margin: 5rem auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 16px #d0e6fb; padding: 2rem; }
            h1 { color: #2557a7; }
            .links { margin: 2rem 0; }
            .btn { display: inline-block; margin: 0.5rem 1rem 0.5rem 0; padding: 0.6rem 1.3rem; background: #2557a7; color: #fff; border-radius: 4px; text-decoration: none; font-weight: bold; transition: background .2s; }
            .btn:hover { background: #003366; }
            ul { margin: 0 0 2rem 1.2rem; }
            .about { margin-top: 1.3rem; color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 College Campus API</h1>
            <p>Welcome to the backend of the college portal. Browse API docs or use smart endpoints below.</p>
            <div class="links">
                <a class="btn" href="/docs">Swagger UI Docs</a>
                <a class="btn" href="/redoc">ReDoc UI</a>
            </div>
            <div class="about">
                <h2>About :</h2>
                <p>
                The College Campus API is a modern, RESTful backend designed to efficiently manage and analyze data related to college courses and faculty. Built with FastAPI, it offers a streamlined experience for academic administration, student advising, and technical integration with digital campus systems.  
                </p>
            </div>
        </div>
    </body>
    </html>
    """
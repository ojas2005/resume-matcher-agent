"""Canonical skill names and the aliases people actually write on resumes and JDs."""

SKILL_ALIASES: dict[str, list[str]] = {
    # languages
    "c#": ["c#", "csharp", "c sharp"],
    "python": ["python", "python3"],
    "java": ["java"],
    "javascript": ["javascript", "js", "es6"],
    "typescript": ["typescript", "ts"],
    "sql": ["sql", "t-sql", "tsql", "pl/sql"],
    "go": ["golang"],
    # .NET ecosystem
    ".net": [".net", "dotnet", ".net core", ".net 6", ".net 8", ".net framework"],
    "asp.net core": ["asp.net core", "asp.net", "aspnet core", "asp.net mvc", "web api"],
    "entity framework": ["entity framework", "ef core", "entity framework core"],
    "linq": ["linq"],
    "blazor": ["blazor"],
    "grpc": ["grpc"],
    "signalr": ["signalr"],
    # web / frontend
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angularjs"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap"],
    "rest api": ["rest api", "restful", "rest apis", "rest"],
    # python web / AI
    "fastapi": ["fastapi", "fast api"],
    "django": ["django"],
    "flask": ["flask"],
    "langchain": ["langchain"],
    "langgraph": ["langgraph"],
    "llm": ["llm", "llms", "large language models", "genai", "gen ai", "generative ai"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "prompt engineering": ["prompt engineering"],
    "semantic kernel": ["semantic kernel"],
    "machine learning": ["machine learning", "ml"],
    # data
    "sql server": ["sql server", "mssql", "ms sql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "vector database": ["vector database", "vector db", "pinecone", "faiss", "chromadb", "qdrant"],
    # cloud / devops
    "azure": ["azure", "microsoft azure"],
    "azure openai": ["azure openai"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker", "containers"],
    "kubernetes": ["kubernetes", "k8s", "aks", "eks"],
    "ci/cd": ["ci/cd", "cicd", "github actions", "azure devops", "jenkins"],
    "git": ["git", "github", "gitlab"],
    "microservices": ["microservices", "microservice"],
    "rabbitmq": ["rabbitmq", "kafka", "service bus"],
    # practices
    "unit testing": ["unit testing", "xunit", "nunit", "pytest", "jest", "tdd"],
    "design patterns": ["design patterns", "solid", "clean architecture"],
    "agile": ["agile", "scrum"],
}

# Knowing the left skill reasonably implies familiarity with the right ones.
IMPLIED_SKILLS: dict[str, list[str]] = {
    "asp.net core": [".net", "c#", "rest api"],
    "entity framework": [".net", "sql"],
    "blazor": [".net", "c#"],
    "fastapi": ["python", "rest api"],
    "django": ["python"],
    "langgraph": ["langchain", "llm"],
    "langchain": ["llm", "python"],
    "rag": ["llm"],
    "azure openai": ["azure", "llm"],
    "react": ["javascript"],
    "angular": ["typescript"],
    "kubernetes": ["docker"],
    "sql server": ["sql"],
    "postgresql": ["sql"],
}

# Short hints used when the LLM is not available.
LEARNING_HINTS: dict[str, str] = {
    "docker": "Containerise one of your existing APIs and push the image to a registry.",
    "kubernetes": "Deploy a containerised service to a local kind/minikube cluster with a Deployment and Service.",
    "azure": "Deploy an API to Azure App Service and wire it to an Azure SQL database.",
    "aws": "Host a small API on AWS (Lambda or ECS) and note it on your resume.",
    "microservices": "Split a monolith project into two services that talk over REST or gRPC.",
    "unit testing": "Add a test project with meaningful coverage to one of your repos.",
    "ci/cd": "Add a GitHub Actions workflow that builds, tests and lints on every push.",
    "react": "Build a small React frontend that consumes one of your APIs.",
    "angular": "Build an Angular frontend with routing and a service layer over a REST API.",
    "rag": "Build a document Q&A bot with a vector store and show retrieval quality checks.",
    "langgraph": "Build a multi-step agent graph with tool calls and conditional routing.",
    "redis": "Add Redis caching to a read-heavy endpoint and measure the speed-up.",
    "rabbitmq": "Publish and consume events between two services through a message broker.",
}

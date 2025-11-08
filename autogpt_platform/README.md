# 🐕 SADOCKDOG Platform

> **Powered by AutoGPT** - Building the future of AI agent automation

Welcome to **SADOCKDOG Platform** - an enhanced, production-ready system for creating, deploying, and managing AI agents that automate complex workflows and solve real-world business problems.

Built on top of [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), SADOCKDOG adds powerful features, streamlined deployment, and enterprise-grade tooling to make AI agent development accessible and productive.

[![Backend CI](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/ci-backend.yml/badge.svg)](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/ci-backend.yml)
[![Frontend CI](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/ci-frontend.yml/badge.svg)](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/ci-frontend.yml)
[![CodeQL](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/SADOCKDOG/SADOCKDOG/actions/workflows/codeql-analysis.yml)
[![License](https://img.shields.io/badge/License-PolyForm%20Shield-blue.svg)](LICENSE.md)
[![GitHub Issues](https://img.shields.io/github/issues/SADOCKDOG/SADOCKDOG)](https://github.com/SADOCKDOG/SADOCKDOG/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> 🔒 **Security Note**: Before deploying to production, please review our [Security Checklist](SECURITY.md) to ensure your deployment is secure.

## 📚 Documentation

- 📖 **[Architecture](../ARCHITECTURE.md)** - System design and tech stack
- 🚀 **[Deployment Guide](../DEPLOYMENT.md)** - Production deployment instructions
- 🤝 **[Contributing](../CONTRIBUTING.md)** - How to contribute to SADOCKDOG
- 🔐 **[Security](SECURITY.md)** - Security best practices

## ✨ What Makes SADOCKDOG Different?

- 🤖 **SADOCKDOG Chat** - Simplified agent selector with chat interface (`/sadockdog`)
- 📱 **Android App Developer Agent** - Autonomously creates complete Android apps with Kotlin & Material Design 3
- 💻 **SADOCKDOG CLI** - Command-line interface for rapid agent execution
- 📊 **SADOCKDOG Manager** - Comprehensive control panel for infrastructure management
- 🎯 **Production-Ready** - Enhanced security, monitoring, and deployment tools
- 📚 **Better Documentation** - Clear guides, examples, and troubleshooting

## Getting Started

### Prerequisites

- Docker
- Docker Compose V2 (comes with Docker Desktop, or can be installed separately)

### Running the System

To run the AutoGPT Platform, follow these steps:

1. Clone this repository to your local machine and navigate to the `autogpt_platform` directory within the repository:

   ```bash
   git clone https://github.com/SADOCKDOG/SADOCKDOG.git
   cd SADOCKDOG/autogpt_platform
   ```

2. Run the following command:

   ```
   cp .env.default .env
   ```

   This command will copy the `.env.default` file to `.env`. You can modify the `.env` file to add your own environment variables.

3. Run the following command:

   ```
   docker compose up -d
   ```

   This command will start all the necessary backend services defined in the `docker-compose.yml` file in detached mode.

4. After all the services are in ready state, open your browser and navigate to `http://localhost:3000` to access the AutoGPT Platform frontend.

### SADOCKDOG: Agent selector and chat

We added a minimal page and CLI to quickly select one of your agents and send a prompt.

- Web: open `http://localhost:3000/sadockdog`
   - Choose an agent from "My Agents"
   - Type a message and execute — you'll get a link to the run details

- CLI: `autogpt_platform/cli/sadockdog_cli.py`
   - Create an API key in the web UI (Profile → API Keys) with EXECUTE_GRAPH
   - Set environment variables and run:

      PowerShell (Windows):

      ```powershell
      $Env:AUTOGPT_API_KEY = "<your_api_key>"
      $Env:AGPT_BASE_URL = "http://localhost:8006"  # optional, default shown
      python autogpt_platform/cli/sadockdog_cli.py
      ```

   - The CLI lists your agents, lets you pick one, and starts an execution with a `prompt` input

## 🤖 Android App Developer Agent

### What it does

The **Android App Developer** agent autonomously creates complete Android applications:

- ✅ Creates a GitHub repository with your app name
- ✅ Generates modern Kotlin code with ViewBinding
- ✅ Creates Material Design 3 layouts
- ✅ Configures Gradle automatically
- ✅ Generates AndroidManifest.xml with permissions
- ✅ Creates resources (strings.xml, colors.xml)
- ✅ Adds professional README with instructions
- ✅ Everything committed automatically to GitHub

### Installing the Agent

**Option 1: Automatic Import (Recommended)**

```powershell
# 1. Get your API key from http://localhost:3000/profile
# 2. Set environment variable
$env:AUTOGPT_API_KEY = "your-api-key-here"

# 3. Install requests if you don't have it
pip install requests

# 4. Run the importer
python import_android_agent.py
```

**Option 2: Manual Import**

1. Go to http://localhost:3000/build
2. Click "Import" button (top right)
3. Select file: `graph_templates/Android_App_Developer_Agent.json`
4. **Important:** Open the imported agent and configure credentials:
   - Select each "GitHub Create File" and "GitHub Create Repository" block
   - In "Credentials" field, select your GitHub OAuth2
   - Save the agent

### Using the Agent

**From Chat SADOCKDOG (Easy)**

1. Go to http://localhost:3000/sadockdog
2. Select **"Android App Developer"**
3. Use this prompt format:

```
app_name: CalculadoraSimple
app_description: Basic Android calculator with standard math operations
features: addition, subtraction, multiplication, division, Material Design interface
```

4. Click **"Execute Agent"**
5. Follow the monitoring link to watch real-time progress

**Example Apps**

**Todo List App:**
```
app_name: TodoListApp
app_description: Task list app with local storage
features: add tasks, mark complete, delete, filter by status, SharedPreferences persistence
```

**Notes App:**
```
app_name: QuickNotes
app_description: App for taking and organizing quick notes
features: create notes, edit, delete, search, categories, share notes
```

**Counter App:**
```
app_name: SimpleCounter
app_description: Simple counter with increment and decrement
features: increment, decrement, reset, value history, animations
```

### Expected Output

The agent creates a GitHub repository with this structure:

```
your-app/
├── app/
│   ├── build.gradle                    # Gradle config
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml     # Manifest with permissions
│           ├── java/com/sadockdog/yourapp/
│           │   └── MainActivity.kt     # Main Kotlin code
│           └── res/
│               ├── layout/
│               │   └── activity_main.xml    # Material Design UI
│               └── values/
│                   ├── strings.xml          # Text resources
│                   └── colors.xml           # Color palette
├── build.gradle                        # Root config
└── README.md                          # Professional documentation
```

### Next Steps After Generation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/app-name.git
   cd app-name
   ```

2. **Open in Android Studio:**
   - File → Open → Select project folder
   - Wait for Gradle sync

3. **Run the app:**
   - Connect Android device or start emulator
   - Click "Run" button (▶️) in Android Studio
   - Your app will install and launch!


### Running Just Core services

You can now run the following to enable just the core services.

```
# For help
make help

# Run just Supabase + Redis + RabbitMQ
make start-core

# Stop core services
make stop-core

# View logs from core services 
make logs-core

# Run formatting and linting for backend and frontend
make format

# Run migrations for backend database
make migrate

# Run backend server
make run-backend

# Run frontend development server
make run-frontend

```

### Docker Compose Commands

Here are some useful Docker Compose commands for managing your AutoGPT Platform:

- `docker compose up -d`: Start the services in detached mode.
- `docker compose stop`: Stop the running services without removing them.
- `docker compose rm`: Remove stopped service containers.
- `docker compose build`: Build or rebuild services.
- `docker compose down`: Stop and remove containers, networks, and volumes.
- `docker compose watch`: Watch for changes in your services and automatically update them.

### Sample Scenarios

Here are some common scenarios where you might use multiple Docker Compose commands:

1. Updating and restarting a specific service:

   ```
   docker compose build api_srv
   docker compose up -d --no-deps api_srv
   ```

   This rebuilds the `api_srv` service and restarts it without affecting other services.

2. Viewing logs for troubleshooting:

   ```
   docker compose logs -f api_srv ws_srv
   ```

   This shows and follows the logs for both `api_srv` and `ws_srv` services.

3. Scaling a service for increased load:

   ```
   docker compose up -d --scale executor=3
   ```

   This scales the `executor` service to 3 instances to handle increased load.

4. Stopping the entire system for maintenance:

   ```
   docker compose stop
   docker compose rm -f
   docker compose pull
   docker compose up -d
   ```

   This stops all services, removes containers, pulls the latest images, and restarts the system.

5. Developing with live updates:

   ```
   docker compose watch
   ```

   This watches for changes in your code and automatically updates the relevant services.

6. Checking the status of services:
   ```
   docker compose ps
   ```
   This shows the current status of all services defined in your docker-compose.yml file.

These scenarios demonstrate how to use Docker Compose commands in combination to manage your AutoGPT Platform effectively.

### Persisting Data

To persist data for PostgreSQL and Redis, you can modify the `docker-compose.yml` file to add volumes. Here's how:

1. Open the `docker-compose.yml` file in a text editor.
2. Add volume configurations for PostgreSQL and Redis services:

   ```yaml
   services:
     postgres:
       # ... other configurations ...
       volumes:
         - postgres_data:/var/lib/postgresql/data

     redis:
       # ... other configurations ...
       volumes:
         - redis_data:/data

   volumes:
     postgres_data:
     redis_data:
   ```

3. Save the file and run `docker compose up -d` to apply the changes.

This configuration will create named volumes for PostgreSQL and Redis, ensuring that your data persists across container restarts.

### API Client Generation

The platform includes scripts for generating and managing the API client:

- `pnpm fetch:openapi`: Fetches the OpenAPI specification from the backend service (requires backend to be running on port 8006)
- `pnpm generate:api-client`: Generates the TypeScript API client from the OpenAPI specification using Orval
- `pnpm generate:api`: Runs both fetch and generate commands in sequence

#### Manual API Client Updates

If you need to update the API client after making changes to the backend API:

1. Ensure the backend services are running:

   ```
   docker compose up -d
   ```

2. Generate the updated API client:
   ```
   pnpm generate:api
   ```

This will fetch the latest OpenAPI specification and regenerate the TypeScript client code.

---

## 🤝 Contributing

We welcome contributions to SADOCKDOG Platform! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting PRs.

### Quick Start for Contributors:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test them
4. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the **PolyForm Shield License 1.0.0** - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Built on [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) by Significant Gravitas
- Powered by OpenAI, Anthropic, and other AI providers
- Thanks to all contributors who make this project possible

## 📞 Support & Community

- 🐛 [Report Bugs](https://github.com/SADOCKDOG/SADOCKDOG/issues/new?template=bug_report.yml)
- ✨ [Request Features](https://github.com/SADOCKDOG/SADOCKDOG/issues/new?template=feature_request.yml)
- 📚 [Documentation Issues](https://github.com/SADOCKDOG/SADOCKDOG/issues/new?template=documentation.yml)
- 💬 [Discussions](https://github.com/SADOCKDOG/SADOCKDOG/discussions) (if enabled)

---

<p align="center">
  Made with ❤️ by the SADOCKDOG Team
</p>

<p align="center">
  <sub>SADOCKDOG Platform - Empowering AI Agent Development</sub>
</p>

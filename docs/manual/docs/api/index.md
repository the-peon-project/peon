# 🔗 API Reference

Complete reference for the PEON REST API, enabling programmatic server management and automation.

!!! info "API Version"
    This documentation covers **PEON API v1** - the current stable version.
    
    **Base URL**: `http://your-peon-instance:5000/api/v1`

## 🚀 Quick Start

### Authentication
All API requests require authentication using API tokens:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/v1/servers
```

### Basic Server Operations

```bash
# List all servers
GET /api/v1/servers

# Create new server  
POST /api/v1/servers
{
  "name": "MyServer",
  "game": "valheim", 
  "config": {}
}

# Start server
POST /api/v1/servers/{server_id}/start

# Stop server
POST /api/v1/servers/{server_id}/stop
```

## 📋 Endpoints

### Server Management

#### List Servers
```http
GET /api/v1/servers
```

**Response:**
```json
{
  "servers": [
    {
      "id": "valheim_001",
      "name": "Viking Adventures", 
      "game": "valheim",
      "status": "running",
      "players": 3,
      "max_players": 10,
      "created_at": "2024-01-15T10:30:00Z",
      "last_activity": "2024-01-15T15:45:00Z"
    }
  ],
  "total": 1
}
```

#### Create Server
```http
POST /api/v1/servers
```

**Request Body:**
```json
{
  "name": "My Server",
  "game": "valheim",
  "config": {
    "max_players": 8,
    "password": "secret123",
    "world_name": "Valhalla",
    "difficulty": "normal"
  }
}
```

**Response:**
```json
{
  "id": "valheim_002", 
  "name": "My Server",
  "status": "creating",
  "estimated_ready": "2024-01-15T10:35:00Z"
}
```

#### Get Server Details
```http
GET /api/v1/servers/{server_id}
```

**Response:**
```json
{
  "id": "valheim_001",
  "name": "Viking Adventures",
  "game": "valheim", 
  "status": "running",
  "players": {
    "current": 3,
    "max": 10,
    "list": ["Player1", "Player2", "Player3"]
  },
  "connection": {
    "host": "192.168.1.100",
    "port": 2456,
    "password": "required"
  },
  "resources": {
    "cpu_percent": 45.2,
    "memory_mb": 2048,
    "disk_gb": 1.2
  },
  "uptime": 14400,
  "last_backup": "2024-01-15T06:00:00Z"
}
```

#### Server Actions
```http
POST /api/v1/servers/{server_id}/start
POST /api/v1/servers/{server_id}/stop  
POST /api/v1/servers/{server_id}/restart
POST /api/v1/servers/{server_id}/backup
DELETE /api/v1/servers/{server_id}
```

### Game Catalog

#### List Available Games
```http
GET /api/v1/games
```

**Response:**
```json
{
  "games": [
    {
      "id": "valheim",
      "name": "Valheim", 
      "description": "Viking survival adventure",
      "status": "stable",
      "default_config": {
        "max_players": 10,
        "difficulty": "normal",
        "pvp": false
      },
      "config_schema": {
        "max_players": {"type": "integer", "min": 1, "max": 64},
        "password": {"type": "string", "optional": true},
        "world_name": {"type": "string", "default": "Dedicate"}
      }
    }
  ]
}
```

#### Get Game Configuration Schema  
```http
GET /api/v1/games/{game_id}/config
```

### System Information

#### System Status
```http
GET /api/v1/system/status
```

**Response:**
```json
{
  "version": "3.0.0",
  "uptime": 86400,
  "servers": {
    "total": 5,
    "running": 3,
    "stopped": 2
  },
  "resources": {
    "cpu_cores": 8,
    "cpu_percent": 32.5,
    "memory_total_gb": 32,
    "memory_used_gb": 12.4,
    "disk_total_gb": 1000,
    "disk_used_gb": 156.8
  }
}
```

#### System Health Check
```http
GET /api/v1/system/health
```

## 🔐 Authentication

### Token-Based Authentication
PEON uses Bearer tokens for API authentication:

```http
Authorization: Bearer YOUR_API_TOKEN
```

### Generating Tokens
Tokens are generated through the web interface or orchestrator configuration:

1. **Web UI**: Navigate to Settings → API Tokens
2. **Config File**: Add to `config/api_tokens.json`
3. **Environment Variable**: Set `PEON_API_TOKEN`

### Token Scopes
Different tokens can have different permissions:

- **`read`** - View servers and system status
- **`write`** - Create, modify, and delete servers
- **`admin`** - Full system administration access

## 📊 Response Formats

### Success Responses
All successful API calls return JSON with consistent structure:

```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Responses
Error responses include detailed information:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_GAME",
    "message": "The specified game 'minecraft' is not supported",
    "details": {
      "supported_games": ["valheim", "palworld", "cs2"]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### HTTP Status Codes
| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request parameters |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `409` | Conflict | Resource already exists |
| `422` | Unprocessable Entity | Validation failed |
| `500` | Internal Server Error | Server error occurred |

## 🔄 Webhooks

### Configuring Webhooks
Configure PEON to send notifications to external services:

```json
{
  "webhooks": {
    "server_events": {
      "url": "https://your-app.com/peon-webhook",
      "events": ["server.created", "server.started", "server.stopped"],
      "secret": "webhook_secret_key"
    }
  }
}
```

### Webhook Events
PEON sends webhooks for these events:

| Event | Description | Payload |
|-------|-------------|---------|
| `server.created` | New server created | Server details |
| `server.started` | Server started | Server status |
| `server.stopped` | Server stopped | Server status |  
| `server.deleted` | Server deleted | Server ID |
| `system.maintenance` | System maintenance mode | Maintenance details |

### Webhook Payload Example
```json
{
  "event": "server.started",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "server_id": "valheim_001",
    "name": "Viking Adventures", 
    "game": "valheim",
    "status": "running"
  }
}
```

## 💻 Code Examples

### Python Example
```python
import requests

API_BASE = "http://localhost:5000/api/v1"
TOKEN = "your_api_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Create server
response = requests.post(f"{API_BASE}/servers", 
    headers=headers,
    json={
        "name": "My Valheim Server",
        "game": "valheim",
        "config": {
            "max_players": 8,
            "password": "vikings123"
        }
    }
)

server = response.json()
print(f"Created server: {server['id']}")

# Start server
requests.post(f"{API_BASE}/servers/{server['id']}/start", 
              headers=headers)
```

### JavaScript Example  
```javascript
const API_BASE = 'http://localhost:5000/api/v1';
const TOKEN = 'your_api_token';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

// Create and start server
async function createServer() {
  const response = await fetch(`${API_BASE}/servers`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name: 'Node.js Server',
      game: 'palworld',
      config: {
        max_players: 16
      }
    })
  });
  
  const server = await response.json();
  console.log('Server created:', server.id);
  
  // Start the server
  await fetch(`${API_BASE}/servers/${server.id}/start`, {
    method: 'POST',
    headers
  });
}
```

### cURL Examples
```bash
# List all servers
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/v1/servers

# Create Palworld server
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"Pal Paradise","game":"palworld","config":{"max_players":20}}' \
     http://localhost:5000/api/v1/servers

# Get server status
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/v1/servers/palworld_001

# Start server
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/api/v1/servers/palworld_001/start
```

## 🔧 Advanced Usage

### Batch Operations
Create multiple servers efficiently:

```python
games = ['valheim', 'palworld', 'cs2']
servers = []

for game in games:
    response = requests.post(f"{API_BASE}/servers",
        headers=headers,
        json={
            "name": f"Community {game.title()} Server",
            "game": game,
            "config": {"max_players": 32}
        }
    )
    servers.append(response.json())

# Start all servers
for server in servers:
    requests.post(f"{API_BASE}/servers/{server['id']}/start",
                 headers=headers)
```

### Monitoring and Alerts
Set up automated monitoring:

```python
import time

def monitor_servers():
    while True:
        response = requests.get(f"{API_BASE}/servers", headers=headers)
        servers = response.json()['servers']
        
        for server in servers:
            if server['status'] == 'error':
                send_alert(f"Server {server['name']} has errors!")
                
        time.sleep(60)  # Check every minute
```

### Configuration Templates
Use templates for consistent server deployment:

```python
TEMPLATES = {
    'competitive_cs2': {
        'game': 'cs2',
        'config': {
            'max_players': 10,
            'game_mode': 'competitive',
            'map': 'de_dust2'
        }
    },
    'casual_valheim': {
        'game': 'valheim', 
        'config': {
            'max_players': 6,
            'difficulty': 'easy',
            'pvp': False
        }
    }
}

def create_from_template(template_name, server_name):
    template = TEMPLATES[template_name]
    return requests.post(f"{API_BASE}/servers",
        headers=headers,
        json={
            'name': server_name,
            **template
        }
    )
```

## 🐛 Error Handling

### Common Error Scenarios
Handle typical API errors gracefully:

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Server not found")
        elif response.status_code == 409:
            print("Server already exists") 
        elif response.status_code == 422:
            errors = response.json().get('error', {})
            print(f"Validation failed: {errors}")
        else:
            print(f"HTTP error: {e}")
            
    except RequestException as e:
        print(f"Request failed: {e}")
        
    return None
```

### Rate Limiting
PEON implements rate limiting to prevent abuse:

- **100 requests per minute** per API token
- **429 Too Many Requests** when limit exceeded  
- **Retry-After** header indicates wait time

```python
import time

def rate_limited_request(url, **kwargs):
    response = requests.get(url, **kwargs)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return rate_limited_request(url, **kwargs)
        
    return response
```

## 📚 Additional Resources

### Development Tools
- **[Postman Collection](https://github.com/the-peon-project/peon/blob/main/docs/api/PEON_API.postman_collection.json)** - Pre-configured API requests
- **[OpenAPI Spec](https://github.com/the-peon-project/peon/blob/main/docs/api/openapi.yaml)** - Complete API specification
- **[SDKs and Libraries](https://github.com/the-peon-project/peon/wiki/SDKs)** - Community-contributed API clients

### Community Resources
- **[API Examples Repository](https://github.com/the-peon-project/peon-api-examples)** - Code samples and tutorials
- **[Discord #api-support](https://discord.gg/KJFVyayH8g)** - Get help from developers
- **[API Changelog](https://github.com/the-peon-project/peon/blob/main/CHANGELOG.md)** - Version history and breaking changes

---

## 🆘 Need Help?

- **[Discord Community](https://discord.gg/KJFVyayH8g)** - Real-time API support
- **[GitHub Issues](https://github.com/the-peon-project/peon/issues)** - Report API bugs
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/peon-api)** - Community Q&A
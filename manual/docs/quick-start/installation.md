# Installation Guide

Get PEON running on your system in minutes with Docker Compose.

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **System Requirements**: 4GB RAM, 2 CPU cores minimum

!!! tip "System Check"
    Run these commands to verify your system:
    ```bash
    docker --version
    docker compose version
    ```

## Quick Install (Docker Compose)

### 1. Download PEON

```bash
git clone https://github.com/the-peon-project/peon.git
cd peon
```

### 2. Configure Environment

```bash
cp .env.sample .env
nano .env  # Edit configuration
```

**Key Environment Variables:**

```env
# Orchestrator Configuration
PEON_API_KEY=your_secure_api_key_here
PEON_DIRECTORY=/root/peon

# Optional shared cache proxy for game downloads and updates
PEON_CACHE_ENABLED=true
PEON_CACHE_URL=http://host.docker.internal:3128
PEON_CACHE_BYPASS=localhost,127.0.0.1,host.docker.internal,peon.orc,peon.webui,peon.db

# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
```

### 3. Start PEON Services

```bash
./deploy_peon.sh
```

This will start:

- **Orchestrator**: Core API service (port 5000)
- **Cache Proxy**: Shared HTTP cache for SteamCMD and other proxy-aware downloads (port 3128, when enabled)
- **Discord Bot**: Slash command interface
- **Web UI**: Browser interface (port 80)

When the cache proxy is enabled, newly generated game server manifests receive standard proxy environment variables and a `host.docker.internal` host-gateway alias. Downloads that honor `HTTP_PROXY` or `HTTPS_PROXY` will reuse cached content locally instead of fetching every update from the internet again.

### 4. Verify Installation

Check that all services are running:

```bash
docker compose ps
```

You should see:
```
NAME           SERVICE      STATUS       PORTS
peon-orc-1     orc         running      0.0.0.0:5000->5000/tcp
peon-bot-1     bot         running      
peon-webui-1   webapp      running      0.0.0.0:80->80/tcp
```

For API documentation:

- WebUI API docs: `http://localhost/docs`
- Orchestrator docs through WebUI sub-path: `http://localhost/api/proxy/{orchestrator_id}/docs`

## Discord Bot Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your application (e.g., "PEON Game Server Bot")
4. Go to "Bot" section
5. Click "Add Bot"
6. Copy the bot token to your `.env` file

### 2. Set Bot Permissions

Your bot needs these permissions:
- Send Messages
- Use Slash Commands
- Embed Links
- Attach Files
- Read Message History
- Use External Emojis

**Permission Integer**: `137443262464`

### 3. Invite Bot to Server

Use this URL (replace CLIENT_ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=137443262464&scope=bot%20applications.commands
```

### 4. Test Bot

In your Discord server, type:
```
/peon
```

You should see the PEON interface!

## Manual Installation

### Option A: Individual Containers

Run each component separately:

```bash
# Orchestrator
docker run -d \
  --name peon-orc \
  -p 5000:5000 \
  -e LOCAL_API_KEY=your_api_key \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/home/peon \
  umlatt/peon.orc:latest

# Discord Bot
docker run -d \
  --name peon-bot \
  -e DISCORD_TOKEN=your_token \
  -e LOCAL_API_KEY=your_api_key \
  -v $(pwd)/config:/app/config \
  umlatt/peon.bot.discord:latest

# Web UI
docker run -d \
  --name peon-webui \
  -p 80:80 \
  -e REACT_APP_BACKEND_URL=http://localhost \
  umlatt/peon.webui:latest
```

### Option B: Native Installation

!!! warning "Advanced Users Only"
    Native installation requires managing Python dependencies and system services manually.

See the [development documentation](../development/index.md) for native installation instructions.

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check Discord token in `.env` file
- Verify bot permissions in Discord server
- Check bot container logs: `docker logs peon-bot-1`

**API errors:**
- Verify orchestrator is running: `curl http://localhost:5000/api/v1/orchestrator`
- Check API key configuration
- Review orchestrator logs: `docker logs peon-orc-1`

**Container startup issues:**
- Ensure Docker daemon is running
- Check available disk space
- Verify port availability

### Getting Help

- 📖 [User Guide](../guides/index.md)
- 🐛 [Report Issues](https://github.com/the-peon-project/peon/issues)
- 💬 [Discord Community](https://discord.gg/KJFVyayH8g)
# User Guides

Comprehensive guides for using the PEON platform effectively.

## 🚀 Getting Started

### Essential Guides
- **[Discord Bot Guide](50_bot_discord.md)** - Master the modern Discord interface
- **[REST API Reference](02_rest_api.md)** - Programmatic server management
- **[Supported Games](../games.md)** - Complete catalog of available games

### Quick References
- **[Command Cheat Sheet](50_bot_discord.md#complete-command-reference)** - All Discord commands
- **[API Endpoints](02_rest_api.md#endpoints)** - REST API reference
- **[Troubleshooting](50_bot_discord.md#troubleshooting)** - Common issues and solutions

## 📚 By User Type

### For Players
Want to host servers for you and your friends?

1. **[Discord Bot Guide](50_bot_discord.md)** - Easy server management
2. **[First Server Tutorial](../quick-start/first-server.md)** - Step-by-step server creation
3. **[Game-Specific Guides](games/index.md)** - Optimized setups per game

### For Communities  
Managing servers for gaming communities?

1. **[Advanced Discord Setup](50_bot_discord.md)** - Multi-server organization
2. **[API Integration](02_rest_api.md)** - Automated management
3. **[Web Interface](../development/04_webui.md)** - Browser-based controls

### For Developers
Building integrations with PEON?

1. **[REST API Guide](02_rest_api.md)** - Complete API documentation
2. **[Development Setup](../development/index.md)** - Local development environment
3. **[Component Architecture](../development/00_peon.md)** - System overview

## 🎮 Game-Specific Content

### Popular Games
- **[Valheim](games/valheim.md)** - Viking server configuration  
- **[Palworld](games/palworld.md)** - Creature collection servers
- **[ARK: Survival Evolved](games/ark.md)** - Dinosaur survival setup

### All Supported Games
**[View Complete Game Catalog →](../games.md)**

## 🔧 Advanced Topics

### System Administration
- **[Installation & Setup](../quick-start/installation.md)** - Complete deployment guide
- **[API Security](../api/index.md)** - Authentication and authorization
- **[Performance Optimization](../development/01_orchestrator.md)** - Resource management

### Integration & Automation
- **[Webhook Integration](../api/index.md#webhooks)** - External service notifications
- **[Backup Strategies](50_bot_discord.md)** - Data protection
- **[Monitoring & Alerts](../development/01_orchestrator.md)** - System health

## 📖 Reference Materials

### Quick Links
- **[Command Reference](50_bot_discord.md#complete-command-reference)** - All Discord commands
- **[API Endpoints](02_rest_api.md)** - REST API methods
- **[Configuration Options](../development/index.md)** - Environment variables
- **[Error Codes](../api/index.md)** - API error reference

### External Resources
- **[Discord Server](https://discord.gg/KJFVyayH8g)** - Community support
- **[GitHub Issues](https://github.com/the-peon-project/peon/issues)** - Bug reports
- **[Docker Hub](https://hub.docker.com/u/umlatt)** - Container images

## 🆘 Need Help?

1. **Check the relevant guide** - Most questions are covered in depth
2. **Try the Discord bot** - Use `/help` for quick assistance
3. **Search existing issues** - Someone may have had the same problem
4. **Join our community** - Get help from other users
5. **Report bugs** - Help us improve the platform

**[Join Discord Community →](https://discord.gg/KJFVyayH8g)**

```bash
git clone https://github.com/the-peon-project/peon
```

### 2. Download the latest release

> :warning: If you want to deploy a Discord bot, you need to first create a `DISCORD TOKEN`. You can follow the steps at [this link](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal)

You can now deploy PEON with the following.

```bash
cd peon
./deploy_peon.sh
```

## PEON Usage

```bash
peon
```
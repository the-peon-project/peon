# Discord Bot - Modern Game Server Management

The PEON Discord Bot provides an intuitive, modern interface for managing game servers directly from Discord using slash commands.

!!! success "✨ **Fully Modernized (v3.0.0)**"
    The Discord bot has been completely rewritten with Discord.py v2, featuring slash commands, enhanced UI, auto-completion, and persistent views.

---

## 🚀 Quick Start

### Essential Commands

```
/peon                 # Main server interface
/create valheim bob   # Create new server
/server start         # Quick server actions  
/list servers         # View all servers
/help                 # Command reference
```

### Channel-Based Management

PEON works intelligently based on your Discord channel:

- **Admin channels**: Full administrative controls
- **Game channels** (`game-servername`): Server-specific controls
- **Any channel**: Basic commands work everywhere

---

## 📋 Complete Command Reference

### Core Management

#### `/peon [channel_type]`
**Main interface for server management**

- **Admin Mode**: Full administrative controls
- **Server Mode**: Server-specific management
- **Auto-detect**: Smart channel detection

```
/peon admin           # Force admin interface
/peon server          # Force server interface  
/peon                 # Auto-detect mode
```

#### `/create <game_type> <server_name> [description]`
**Create new game servers with auto-completion**

```
/create minecraft survival-world
/create valheim viking-adventure description:Epic Viking server
/create palworld pals-paradise description:Creature collecting fun
```

**Supported Games**: Minecraft, Valheim, Palworld, ARK, CS2, Rust, Starbound, and 15+ more

#### `/server <action> [server] [timer] [mode]`
**Quick server management commands**

**Actions:**
- `start` - Boot up server
- `stop` - Shutdown server (with optional timer)
- `restart` - Quick restart
- `info` - View detailed server status
- `update` - Update server files
- `backup` - Create and download backup

```
/server start server:valheim.bob
/server stop server:minecraft.world timer:30m
/server update server:palworld.paradise mode:full
/server backup server:ark.island
```

#### `/list <type>`
**View servers, orchestrators, and game plans**

```
/list servers         # All game servers
/list orchestrators   # Registered orchestrators  
/list plans          # Available game types
```

---

## 🎮 Interactive Interface Features

### Enhanced Server Controls

**Server Management Panel:**
- 🚀 **Start** - Instant server startup
- 🛑 **Stop** - Smart shutdown with timer options
- 🔄 **Restart** - Quick restart
- 📊 **Info** - Real-time server status
- ⬆️ **Update** - Multi-mode updates (server/image/full/reinit)
- 📦 **Backup** - One-click backup downloads

**Advanced Features:**
- ⏰ **Timer Stops** - Schedule shutdowns
- 📝 **Edit Description** - Update server info
- 🗑️ **Safe Deletion** - Container-only or complete removal

### Administrator Interface

**Orchestrator Management:**
- 🏢 **Register** - Connect new orchestrators
- 🗑️ **Deregister** - Remove orchestrators
- 📊 **Status Check** - Health monitoring
- 📦 **Import Servers** - Discover existing servers

**Server Creation:**
- 🏗️ **Create Server** - Full server deployment
- 📚 **Browse Plans** - Explore available games
- 🔄 **Update Plans** - Refresh game catalog

---

## ⚡ Advanced Features

### Smart Auto-Completion

All commands feature intelligent auto-completion:

- **Game Types**: Suggests available games as you type
- **Server Names**: Shows your existing servers
- **Timers**: Common time formats (15m, 2h, 22:00)
- **Update Modes**: Available update options

### Flexible Timer System

Schedule server actions with multiple time formats:

**Duration Timers:**
```
15m or 15             # 15 minutes from now
2h                    # 2 hours from now  
1d                    # 1 day from now
```

**Specific Times:**
```
22:30                 # Today at 10:30 PM
2024-12-25.14:00      # Christmas at 2 PM
2024/12/25.14h00      # Alternative format
```

**Examples:**
```
/server stop timer:30m              # Stop in 30 minutes
/server stop timer:22:00            # Stop at 10 PM today
/server stop timer:2024-12-31.23:59 # New Year's Eve stop
```

### Update System

**Update Modes:**
- **Server**: Game files only (safest, fastest)
- **Image**: Container image update  
- **Full**: Both game files and container
- **Reinit**: Complete reinstall (preserves saves)

```
/server update mode:server    # Quick game update
/server update mode:full      # Complete system update
/server update mode:reinit    # Fresh install
```

### Enhanced Error Handling

- **Smart Error Messages**: Clear, actionable error descriptions
- **Troubleshooting Tips**: Built-in help for common issues  
- **Connection Testing**: Automatic orchestrator health checks
- **Fallback Options**: Graceful degradation when services unavailable

---

## 🛠️ Configuration & Setup

### Bot Permissions

Required Discord permissions:
- **Send Messages** - Basic communication
- **Use Slash Commands** - Modern command interface
- **Embed Links** - Rich message formatting
- **Attach Files** - Backup downloads
- **Read Message History** - Context awareness
- **Use External Emojis** - Enhanced visual feedback

**Permission Integer**: `137443262464`

### Environment Variables

```env
# Discord Configuration
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_server_id
DISCORD_ADMIN_CHANNEL_ID=admin_channel_id

# Orchestrator Connection  
LOCAL_API_KEY=your_api_key
ORCHESTRATOR_URL=http://peon.orc:5000

# Optional Features
LOG_LEVEL=INFO
ENABLE_LEGACY_COMMANDS=false
```

### Channel Setup

**Recommended Channel Structure:**
```
📁 PEON Game Servers
  🔧 peon-admin          # Administrative controls
  🎮 minecraft-survival  # Minecraft server management
  ⚔️ valheim-adventure   # Valheim server management  
  🐾 palworld-paradise   # Palworld server management
  📢 server-announcements # Status updates
```

---

## 🔧 Troubleshooting

### Common Issues

??? question "Bot not responding to slash commands"
    **Solutions:**
    - Verify bot has "Use Slash Commands" permission
    - Check bot is online in Discord member list
    - Re-invite bot with updated permissions
    - Restart bot container: `docker restart peon.bot.discord`

??? question "Commands return 'No orchestrators registered'"
    **Solutions:**
    - Use `/peon admin` → "Register Orchestrator"  
    - Verify orchestrator URL and API key
    - Check orchestrator container is running
    - Test connection: `curl http://localhost:5000/api/v1/orchestrator`

??? question "Server creation fails with 404 error"
    **Solutions:**
    - Use `/debug test_connectivity` to diagnose
    - Check available game plans: `/list plans`
    - Verify game name spelling (use auto-completion)
    - Check orchestrator logs for detailed errors

??? question "'Interaction failed' errors"
    **Solutions:**
    - Commands must complete within 15 minutes
    - For long operations, use Web UI instead
    - Check Discord bot logs: `docker logs peon.bot.discord`
    - Verify stable network connection

### Debug Commands

```
/debug test_connectivity  # Test orchestrator connection
/debug list_plans        # Show available game plans
```

### Log Analysis

**Bot Logs:**
```bash
docker logs peon.bot.discord -f     # Follow bot logs
docker logs peon.orc -f             # Follow orchestrator logs  
```

**Common Log Patterns:**
- `Server create` - Server creation attempts
- `Response status: 404` - API endpoint issues
- `Connection failed` - Network problems
- `Permission denied` - Discord permission issues

---

## 🚀 Tips & Best Practices

### Efficient Server Management

1. **Use Channel Names**: Name channels `game-servername` for automatic detection
2. **Leverage Auto-completion**: Start typing and let Discord suggest options
3. **Set Timers**: Use scheduled stops to save resources
4. **Regular Backups**: Download saves before major updates
5. **Monitor Status**: Use `/server info` to check server health

### Discord Organization

1. **Dedicated Categories**: Group game channels together
2. **Clear Naming**: Use consistent `game-servername` format  
3. **Admin Separation**: Keep admin commands in dedicated channels
4. **Announcement Channel**: Share server status updates
5. **Role Permissions**: Limit admin commands to trusted roles

### Performance Optimization

1. **Resource Monitoring**: Check server resource usage regularly
2. **Scheduled Updates**: Update during off-peak hours
3. **Cleanup**: Remove unused servers to free resources
4. **Efficient Restarts**: Use restart instead of stop/start cycle

---

## 📈 Migration from Legacy Commands

The bot automatically handles migration from old prefix commands (`!command`) to modern slash commands (`/command`).

### Command Mapping

| Legacy | Modern | Notes |
|---------|---------|-------|
| `!peon` | `/peon` | Enhanced interface |
| `!get servername` | `/server info` | Auto-completion |
| `!start servername` | `/server start` | Faster execution |
| `!stop servername 30m` | `/server stop timer:30m` | Improved timer parsing |
| `!plans` | `/list plans` | Better formatting |
| `!getall` | `/list servers` | Cleaner output |

### Legacy Support

Legacy commands show helpful migration messages:
```
🔄 Command Updated!
This bot now uses Slash Commands for a better experience!
✨ Try /peon instead of !peon
```

---

## 🔗 Related Documentation

- **[Quick Start Guide](../quick-start/first-server.md)** - Deploy your first server
- **[REST API](02_rest_api.md)** - Programmatic server management  
- **[Web Interface](../development/04_webui.md)** - Browser-based management
- **[Supported Games](../games.md)** - Complete game catalog

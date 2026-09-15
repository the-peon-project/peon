# Deploy Your First Server

Let's create your first game server using PEON's Discord bot interface.

## Prerequisites

- PEON installed and running ([Installation Guide](installation.md))
- Discord bot configured and online
- Admin permissions in your Discord server

## Step 1: Access PEON Interface

In your Discord server, use the slash command:

```
/peon admin
```

This opens the **administrator interface** with full controls.

*Administrator interface screenshot will be added in v3.1.0*

## Step 2: Register an Orchestrator (First Time Only)

If this is your first time using PEON, you'll need to register your orchestrator:

1. Click **"🏢 Register Orchestrator"**
2. Fill in the modal:
   - **Name**: `Main Server`
   - **URL**: `http://peon.orc:5000` (or your server IP)
   - **API Key**: Your configured API key from `.env`
3. Click **Submit**

✅ **Success**: You'll see "Orchestrator registered successfully!"

## Step 3: Browse Available Games

Click **"📚 Browse Plans"** to see all supported games:

- 🧩 Minecraft
- ⚔️ Valheim  
- 🐾 Palworld
- 🦕 ARK: Survival Evolved
- 🔫 Counter-Strike 2
- 🌟 Starbound
- And many more!

## Step 4: Create Your First Server

### Method A: Using Admin Interface

1. Click **"🏗️ Create Server"**
2. Select your game (e.g., **Valheim**)
3. Fill in server details:
   - **Server Name**: `myvalheim` (no spaces)
   - **Description**: `My first Valheim server`
4. Click **Submit**

### Method B: Using Slash Commands

Use the quick create command:

```
/create valheim myvalheim
```

Optional with description:
```
/create game_type:valheim server_name:myvalheim description:My awesome server
```

### Method C: Using the Web UI

1. Open your PEON Web UI host (for example `http://<your-host>:8080` when proxy mode is enabled).
2. Go to **Server Management** and click **Deploy**.
3. Select a game plan tile.
4. Fill in:
   - **Server Name**
   - Dynamic **Configuration** fields generated from that game's plan
5. Click **Deploy Server**.

The deploy form automatically pre-fills known defaults from each plan and validates required settings before submitting the deployment request.

## Step 5: Monitor Server Creation

PEON will:

1. **Download** game files
2. **Configure** server settings
3. **Create** secure container
4. **Start** the server

This takes 2-10 minutes depending on game size.

## Step 6: Manage Your Server

### Quick Server Actions

```
/server action:start server:valheim.myvalheim
/server action:stop server:valheim.myvalheim  
/server action:restart server:valheim.myvalheim
/server action:info server:valheim.myvalheim
```

### Using Server Interface

In a channel named `valheim-myvalheim`, use:

```
/peon
```

This gives you server-specific controls:

- 🚀 **Start** - Boot up the server
- 🛑 **Stop** - Shutdown server (with optional timer)
- 🔄 **Restart** - Quick restart
- 📊 **Info** - View server status
- ⬆️ **Update** - Update game files
- 📦 **Backup** - Download server backup

## Step 7: Connect to Your Server

### Find Server Details

Use the info command to get connection details:

```
/server action:info server:valheim.myvalheim
```

This shows:
- **Server IP**: Your host IP address
- **Port**: Assigned port (e.g., 2456)
- **Status**: Running/Stopped
- **Players**: Current player count

### Connect from Game Client

**Example for Valheim:**
1. Open Valheim
2. Go to "Join Game" → "Add server"
3. Enter: `your-server-ip:2456`
4. Connect and enjoy!

## Common Server Operations

### Scheduled Server Stops

Stop server in 30 minutes:
```
/server action:stop server:valheim.myvalheim timer:30m
```

Stop at specific time:
```
/server action:stop server:valheim.myvalheim timer:22:00
```

### Server Updates

Update game files:
```
/server action:update server:valheim.myvalheim mode:server
```

Full container update:
```
/server action:update server:valheim.myvalheim mode:full
```

### Backups

Create and download backup:
```
/server action:backup server:valheim.myvalheim
```

## Next Steps

### Create More Servers

You can run multiple servers of the same or different games:

```
/create minecraft survival-world
/create palworld pals-paradise  
/create ark dino-island
```

### Organize with Channels

Create dedicated Discord channels for each server:
- `#valheim-myvalheim`
- `#minecraft-survival-world`
- `#palworld-pals-paradise`

### Explore Advanced Features

- **[User Guide](../guides/index.md)** - Comprehensive feature documentation
- **[REST API](../guides/02_rest_api.md)** - Programmatic server management
- **[Web UI](../development/04_webui.md)** - Browser-based interface

## Troubleshooting

### Server Won't Start

1. Check available resources: `docker stats`
2. Verify ports aren't in use: `netstat -tulpn`
3. Review server logs in orchestrator

### Can't Connect to Server

1. Verify server is running: `/server action:info`
2. Check firewall settings on host
3. Confirm port forwarding if needed

### Discord Commands Not Working

1. Ensure bot has proper permissions
2. Check bot is online in Discord
3. Try re-inviting bot with updated permissions

### Need Help?

- 💬 [Discord Community](https://discord.gg/KJFVyayH8g)
- 🐛 [GitHub Issues](https://github.com/the-peon-project/peon/issues)
- 📖 [Full Documentation](../guides/index.md)
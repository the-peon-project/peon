# ❓ Frequently Asked Questions

Common questions and answers about the PEON project.

## 🚀 Getting Started

### What is PEON?
PEON is an open-source Game Server as a Service (GSaaS) platform that makes hosting and managing game servers incredibly simple. Instead of manually setting up complex server configurations, PEON lets you deploy game servers in minutes using Discord commands or a web interface.

### Is PEON free to use?
Yes! PEON is completely free and open source. You can download, modify, and use it however you want. There are no subscription fees, licensing costs, or hidden charges.

### What games does PEON support?
Currently PEON supports 20+ popular games including:
- **Survival Games**: Valheim, Palworld, Enshrouded, V Rising, Sons of the Forest
- **Shooters**: Counter-Strike 2, CS:GO  
- **Building**: Satisfactory
- **And many more!**

[View the complete game catalog →](games.md)

### How quickly can I get a server running?
Most game servers deploy in 90 seconds to 3 minutes. Simple games like Valheim typically take about 90 seconds, while more complex games might take up to 3 minutes for full deployment.

## 📋 Installation & Setup

### What do I need to run PEON?
**Minimum Requirements:**
- Linux server (Ubuntu 20.04+ recommended)
- 4GB RAM 
- 2 CPU cores
- 20GB available disk space
- Docker and Docker Compose

**For production use:**
- 8GB+ RAM
- 4+ CPU cores  
- 100GB+ SSD storage
- Stable internet connection

### Can I run PEON on Windows or macOS?
While PEON is designed for Linux, you can run it on Windows using:
- **WSL2 (Windows Subsystem for Linux)**
- **Docker Desktop for Windows**
- **VirtualBox/VMware** with Linux VM

macOS users can use:
- **Docker Desktop for Mac**
- **Lima** for containerized Linux environment

### How do I install PEON?
The easiest way is our one-command installer:
```bash
curl -sSL https://raw.githubusercontent.com/the-peon-project/peon/main/deploy_peon.sh | bash
```

For step-by-step installation: [Installation Guide →](quick-start/installation.md)

### Can I install PEON on shared hosting?
No, PEON requires full server access and Docker support, which shared hosting typically doesn't provide. You'll need:
- **VPS (Virtual Private Server)**
- **Dedicated server**
- **Cloud instance** (AWS, GCP, DigitalOcean, etc.)
- **Home server** with public IP

## 🎮 Using PEON

### How do I create my first game server?
1. **Install PEON** using the installation guide
2. **Add the Discord bot** to your Discord server
3. **Use a slash command**: `/create valheim MyServer`  
4. **Wait 90 seconds** for deployment
5. **Get connection details** and start playing!

[Detailed first server guide →](quick-start/first-server.md)

### Can I manage servers without Discord?
Yes! PEON offers multiple interfaces:
- **Discord Bot** - Easiest for most users
- **Web Interface** - Browser-based dashboard  
- **REST API** - For developers and automation
- **CLI Tools** - Command-line management

### How many servers can I run simultaneously?
This depends on your server resources:
- **4GB RAM**: 2-3 small game servers
- **8GB RAM**: 4-6 servers or 2-3 large servers
- **16GB RAM**: 10+ servers depending on games
- **32GB+ RAM**: Limited mainly by CPU and storage

Each game has different resource requirements listed in the [game catalog](games.md).

### Can I run multiple instances of the same game?
Absolutely! You can run multiple Valheim worlds, several CS2 servers, etc. Each gets a unique name and port automatically.

Example:
```
/create valheim Vikings-PvE
/create valheim Vikings-PvP  
/create valheim Test-World
```

## 🔧 Configuration & Management

### How do I configure server settings?
Each game has configurable options accessible through:

**Discord Commands:**
```
/config valheim_001 max_players 8
/config valheim_001 password secretword
/config valheim_001 world_name MyWorld
```

**Web Interface:**
- Navigate to server → Settings tab
- Modify configuration values
- Apply changes

**API:**
```bash
curl -X PUT /api/v1/servers/valheim_001/config \
  -d '{"max_players": 8, "password": "secret"}'
```

### How do I backup my game data?
PEON includes automatic backups:
- **Automatic**: Daily backups at 3 AM server time
- **Manual**: `/backup server_name` command  
- **Scheduled**: Configure custom backup intervals
- **Restore**: `/restore server_name backup_date`

Backups are stored in `/var/lib/peon/backups/` by default.

### Can I use custom game configurations?
Yes! PEON supports advanced customization:
- **Configuration files**: Edit server configs directly
- **Custom Docker images**: Use your own game server images  
- **War Plans**: Create custom game deployment recipes
- **Environment variables**: Pass custom settings

[Advanced configuration guide →](development/index.md#game-development)

### How do I update game servers?
**Automatic Updates (Recommended):**
- Enable in server settings
- Updates happen during maintenance windows
- Automatic backups before updates

**Manual Updates:**
```
/update server_name
```

**Bulk Updates:**
```
/update all
```

## 🔒 Security & Privacy

### Is PEON secure?
PEON implements multiple security layers:
- **Container Isolation**: Each game server runs in isolated Docker containers
- **Resource Limits**: Prevents any server from consuming excessive resources
- **Network Segmentation**: Servers can't access each other unless configured
- **Regular Updates**: Security patches applied automatically
- **Access Control**: Role-based permissions via Discord

### What data does PEON collect?
PEON is privacy-focused and collects minimal data:
- **Server Metadata**: Names, game types, creation dates
- **Performance Metrics**: CPU, RAM, and disk usage (local only)
- **User Commands**: Discord commands for functionality (not stored permanently)

**PEON Does NOT collect:**
- Personal information beyond Discord user IDs
- Game save data or content
- Chat logs or communications
- Financial information

### Can I run PEON completely offline?
PEON requires internet access for:
- **Initial setup**: Downloading Docker images
- **Discord integration**: Bot communication
- **Game updates**: Server software updates

However, once set up, game servers can run without internet (though players need internet to connect).

### How do I secure my PEON installation?
**Essential Security Steps:**
1. **Firewall Configuration**: Only expose necessary ports
2. **Strong API Keys**: Generate secure API tokens
3. **Regular Updates**: Keep PEON and Docker updated  
4. **Discord Permissions**: Restrict bot permissions appropriately
5. **Backup Encryption**: Encrypt backup storage
6. **Monitor Logs**: Check for suspicious activity

[Security best practices guide →](api/index.md)

## 🐛 Troubleshooting

### My server won't start. What should I check?
**Common Issues:**
1. **Insufficient Resources**: Check CPU/RAM/disk usage
2. **Port Conflicts**: Ensure ports aren't already in use
3. **Docker Issues**: Restart Docker service
4. **Corrupted Game Files**: Try recreating the server
5. **Network Problems**: Check firewall settings

**Debug Steps:**
```bash
# Check PEON logs
docker logs peon-orchestrator

# Check specific server logs  
docker logs game_server_container_name

# Test connectivity
/debug connectivity server_name
```

### Players can't connect to my server. Help!
**Connection Troubleshooting:**
1. **Port Forwarding**: Ensure router forwards the correct ports
2. **Firewall Rules**: Allow game ports through firewall
3. **Server Status**: Verify server is running with `/status server_name`
4. **IP Address**: Use external IP, not local/internal IP
5. **Game Version**: Ensure all players have compatible game versions

**Quick Diagnosis:**
```
/info server_name  # Shows connection details
/test connectivity server_name  # Tests external access
```

### PEON Discord bot is not responding
**Bot Troubleshooting:**
1. **Bot Online Status**: Check if bot appears online in Discord
2. **Permissions**: Ensure bot has necessary Discord permissions  
3. **Slash Commands**: Try `/help` to test basic functionality
4. **Bot Logs**: Check `docker logs peon-discord-bot`
5. **Restart Bot**: `docker restart peon-discord-bot`

### How do I reset a corrupted server?
```bash
# Stop the server
/stop server_name

# Remove corrupted server
/delete server_name  

# Restore from backup (if available)
/restore server_name backup_date

# Or create fresh server
/create game_name server_name
```

### My backups are taking up too much space
**Backup Management:**
```bash
# List all backups
/backup list

# Delete old backups (keeps last 7 days)
/backup cleanup 7d

# Configure backup retention
/config backup retention_days 14
```

## 💰 Cost & Performance

### How much does it cost to run PEON?
PEON itself is free, but you'll need hosting:

**Cloud Hosting Estimates (monthly):**
- **DigitalOcean Droplet** (4GB/2CPU): ~$24/month
- **AWS EC2 t3.medium**: ~$30/month  
- **Google Cloud e2-standard-2**: ~$35/month
- **Linode 4GB**: ~$24/month

**Home Hosting:**
- **Electricity**: ~$5-15/month depending on hardware
- **Internet**: Ensure adequate upload bandwidth

### How many players can my server handle?
This varies significantly by game:

| Game | Light Load | Medium Load | Heavy Load |
|------|------------|-------------|------------|
| **Valheim** | 2-4 players | 6-8 players | 10+ players |
| **Palworld** | 4-8 players | 12-16 players | 20+ players |
| **CS2** | 10 players | 20 players | 32+ players |
| **Satisfactory** | 2 players | 3-4 players | 4+ players |

### Can I run PEON on a Raspberry Pi?
While technically possible, it's not recommended for production use:
- **Raspberry Pi 4 (8GB)**: Can handle 1-2 very light servers
- **Performance**: Significantly slower than x86 systems
- **Compatibility**: Some game servers may not support ARM architecture

Better alternatives:
- **Mini PC**: Intel NUC or similar
- **Used Server**: Older enterprise hardware
- **Cloud Instance**: More predictable performance

## 🤝 Support & Community

### Where can I get help?
**Community Support:**
- **[Discord Server](https://discord.gg/KJFVyayH8g)** - Real-time chat and help
- **[GitHub Issues](https://github.com/the-peon-project/peon/issues)** - Bug reports and feature requests
- **[GitHub Discussions](https://github.com/the-peon-project/peon/discussions)** - Q&A and community chat
- **[Reddit](https://reddit.com/r/thepeonproject)** - Community showcase and discussions

**Documentation:**
- **[User Guides](guides/index.md)** - Comprehensive how-to guides
- **[API Reference](api/index.md)** - Developer documentation
- **[Troubleshooting](guides/50_bot_discord.md)** - Common issues and solutions

### How can I contribute to PEON?
**Ways to Contribute:**
- **[Report Bugs](https://github.com/the-peon-project/peon/issues/new?template=bug_report.md)** - Help us fix issues
- **[Request Features](https://github.com/the-peon-project/peon/issues/new?template=feature_request.md)** - Suggest improvements  
- **[Add Games](development/index.md#game-development)** - Create support for new games
- **[Improve Documentation](https://github.com/the-peon-project/peon-docs)** - Help others learn
- **[Write Code](development/index.md#contributing)** - Contribute features and fixes
- **[Join Discord](https://discord.gg/KJFVyayH8g)** - Help other users

### Is there commercial support available?
While PEON is open source, commercial support options include:
- **Priority Support**: Faster response times via Discord
- **Custom Development**: Paid feature development
- **Consulting Services**: Deployment and optimization help
- **Training Services**: Team training on PEON administration

Contact us in [Discord](https://discord.gg/KJFVyayH8g) for enterprise inquiries.

### Can I hire someone to set up PEON for me?
Yes! Several options:
- **Community Members**: Find experienced users in Discord
- **Freelance Platforms**: Hire Linux/Docker experts on Upwork, Fiverr
- **Managed Services**: Some community members offer managed PEON hosting
- **Professional Services**: Contact PEON team for enterprise deployment

## 🔮 Future & Development

### What's planned for future PEON versions?
**Upcoming Features:**
- **More Games**: Minecraft, Rust, Factorio, and others
- **Cluster Management**: Multi-server deployments
- **Advanced Monitoring**: Performance dashboards and alerting
- **Plugin System**: Community extensions and customizations
- **Mobile App**: iOS/Android management app

[View the roadmap →](https://github.com/the-peon-project/peon/projects)

### How often is PEON updated?
**Release Schedule:**
- **Major Versions**: Every 3-6 months with significant new features
- **Minor Versions**: Monthly with improvements and new games
- **Patch Versions**: Weekly or bi-weekly with bug fixes
- **Security Updates**: As needed, usually within 24-48 hours

### Can I use PEON in production/commercially?
Absolutely! PEON is licensed under Apache 2.0, which allows:
- **Commercial Use**: Build businesses around PEON
- **Modification**: Customize for your needs  
- **Distribution**: Share your customizations
- **Private Use**: Keep modifications private if desired

Many gaming communities and hosting providers already use PEON in production.

### How stable is PEON?
**Stability Status:**
- **Core Components**: Production-ready and stable
- **Popular Games**: Thoroughly tested (Valheim, Palworld, CS2)
- **API**: v1.0 is stable with backwards compatibility
- **Discord Bot**: v3.0 is modern and reliable
- **Breaking Changes**: Rare, with advance notice and migration guides

**Production Considerations:**
- Run regular backups
- Test updates in staging first
- Monitor server resources
- Keep documentation current

---

## 🎯 Still Have Questions?

**Can't find what you're looking for?**

1. **Search the docs** - Use the search bar above
2. **Check Discord** - [Join our community](https://discord.gg/KJFVyayH8g)
3. **Browse GitHub Issues** - [Existing questions](https://github.com/the-peon-project/peon/issues)
4. **Ask the community** - [GitHub Discussions](https://github.com/the-peon-project/peon/discussions)

**Ready to get started?** [Install PEON now →](quick-start/installation.md)
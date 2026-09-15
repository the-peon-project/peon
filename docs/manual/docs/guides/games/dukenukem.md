# Duke Nukem 3D (EDuke32)

![Duke Nukem 3D](../../images/game-logos/dukenukem.png)

## Before you start

### Game Data Required

You **must** provide a legal copy of `DUKE3D.GRP` from your Duke Nukem 3D installation. Place it in the server's `data/` directory before starting.

You can obtain `DUKE3D.GRP` from:

- [Duke Nukem 3D: 20th Anniversary World Tour](https://store.steampowered.com/app/434050/) on Steam
- An original Duke Nukem 3D CD-ROM

!!! warning "Legal Requirement"
    A legitimate copy of `DUKE3D.GRP` is required. The server will not start without it.

### Multiplayer Notes

- EDuke32 multiplayer is considered **experimental**. Network propagation of destructible walls and doors may not work perfectly.
- Default port is **23513/udp**.
- Clients must connect using [EDuke32](https://www.eduke32.com/) with matching game data.

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_NAME` | *None* | The name of your server |
| `MAX_PLAYERS` | `8` | Maximum number of players |
| `PORT` | `23513` | Server port (UDP) |
| `PASSWORD` | *None* | Server password (optional) |

## Stand-alone mode

[Guide on GitHub](https://github.com/the-peon-project/peon-warplans/tree/main/dukenukem#Guide)

> Or... just use PEON. It should do all the heavy lifting for you.

## Links

If you want to dig a bit deeper, here are the links:

- [Development Docs](../../development/games/dukenukem.md)
- [GitHub Project](https://github.com/the-peon-project/peon-warplans/tree/main/dukenukem)
- [EDuke32 Official Site](https://www.eduke32.com/)

## Credits

This war plan was contributed by [dman1901](https://github.com/dman1901). Thank you for your contribution to the PEON project! :tada:

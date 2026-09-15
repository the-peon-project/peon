# About

Welcome to the PEON project.

The easy-to-use GSaaS (Game Server as a Service) platform.

*Whether self-hosted or in the cloud, PEON aims to be efficient in resource consumption with modern tools for the management of **ANY** self-hostable game servers.*

Here you will find all of the official repositories for the PEON project's components.

![PEON Logo](./images/logo/PEON_R2L_medium.png)

## Story behind the name

We love all kinds of games (and want to support them all).

However, one of the many genres of game that we love to play is fantasy RTS.
We loved the strategy fantasy world of games like Warcraft 2 and thought the concept of the 'peon' worker fit our objectives fairly well.

The way we see it, a peon is the lowly lackey of any decent Orcish War Party, sent to do the work of tens of men.
They are often expected to raise War Camps with very little in the way of resources and even less time to do it in.
They must keep the War Camp stocked and running as battles commence at any time for any duration, and raise it to the ground when the War Chief demands it.

## Goals

That informs most of our project objectives:

1. **Easy** - We want non-coders to be able to deploy their servers and have their friends join them (no tinkering required).
`The War Chief needs only to tell the peon what to do, the peon must figure it out and do it`
2. **Any Game** - If a game is self-hostable, we want to support it.
`War Plans can be created very quickly for new War Camps so that Chiefs can battle anywhere they see fit`
3. **Cheap** - Extremely efficient (designed to reduce hosting costs in the cloud, or to use as few resources as possible if running on your server).
`A peon should not require much gold/wood to build his Warcamp`
4. **Fast** - The servers must deploy/start/stop in as small a timeframe as possible. We want to game now, not later.
`Battles do not wait`

## Terms

The project uses arbitratry names for certain concepts. Please see below for details

| Term | Description |
| - | - |
| War Party | A host server where you game servers are deployed. |
| War Camp | A containerized game server. |
| War Plan | A recipe used to automatically deploy the containerized game server. |
| Orc | The management container that orchestrates all of the deployment and management of the game servers on a host (required on each host)

## Documentation

We have some documentation to help you on your way.

### Installation/Deployment

How to [deploy](./guides/index.md) PEON for gaming server automation.

### Using PEON

How to [use](./guides/index.md) PEON gaming server automation services.

### Development

If you want to develop your recipes (or modify the source code for your objectives) go [here](./development/index.md)

## Frequently Asked Questions {#faq}

For common questions and detailed answers, please see our comprehensive [FAQ section](faq.md).

## License Information

Please feel free to look around and use whatever you wish. The project should only be of type MIT.

## Support the project

### Support through knowledge

Please log tickets if something is wrong, and we will try to address it.

### Getting involved

If you would like to get involved, please reach out. In most cases, the help would be greatly appreciated.

### Other methods of support

If you'd like to financially support the project, please feel free to donate.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K567ILJ)

## References

### Logo

The logo is a derivative of the art by [André Kent - Artstation](https://www.artstation.com/artwork/W2E0RQ)
*Please follow the link to his site and support him.*

## Scoreboard

| Builds | Description | Scores |
| - | - | - |
| [Orchestrator](./development/01_orchestrator.md) | This module manages all game servers and is interfaced with using REST. | [![Docker Pulls](https://img.shields.io/docker/pulls/umlatt/peon.orc.svg)](https://hub.docker.com/r/umlatt/peon.orc) [![Docker Stars](https://img.shields.io/docker/stars/umlatt/peon.orc.svg)](https://hub.docker.com/r/umlatt/peon.orc) |
| [Web UI](./development/04_webui.md) | This is the user friendlyness project. A website to manage various orchestrators. | [![Docker Pulls](https://img.shields.io/docker/pulls/umlatt/peon.ui.svg)](https://hub.docker.com/r/umlatt/peon.ui) [![Docker Stars](https://img.shields.io/docker/stars/umlatt/peon.ui.svg)](https://hub.docker.com/r/umlatt/peon.ui) |
| [Contained Steam](./development/02_wartable.md#projects) | Based on cm2networks steamcmd container, with basic PEON integration (can run stand-alone) | [![Docker Pulls](https://img.shields.io/docker/pulls/umlatt/steamcmd.svg)](https://hub.docker.com/r/umlatt/steamcmd) [![Docker Stars](https://img.shields.io/docker/stars/umlatt/steamcmd.svg)](https://hub.docker.com/r/umlatt/steamcmd) |
| [Steamed WINE](./development/02_wartable.md#projects) | The same as `Contained Steam` but with WINE to support Windows only servers. | [![Docker Pulls](https://img.shields.io/docker/pulls/umlatt/steamcmd-winehq.svg)](https://hub.docker.com/r/umlatt/steamcmd-winehq) [![Docker Stars](https://img.shields.io/docker/stars/umlatt/steamcmd-winehq.svg)](https://hub.docker.com/r/umlatt/steamcmd-winehq) |
| [Bot.Discord](./development/50_bot_discord.md) | A Discord bot to allow friends and groups of friends to manage the servers. | [![Docker Pulls](https://img.shields.io/docker/pulls/umlatt/peon.bot.discord.svg)](https://hub.docker.com/r/umlatt/peon.bot.discord) [![Docker Stars](https://img.shields.io/docker/stars/umlatt/peon.bot.discord.svg)](https://hub.docker.com/r/umlatt/peon.bot.discord) |

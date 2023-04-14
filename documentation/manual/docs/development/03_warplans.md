# War Plans

The **War Plan** module works in conjunction with the Orchestrator to deploy specific game servers upon request.

This project handles the unique game recipes.

## Projects

This list will grow over time (as requests come in, or other people contribute recipies to the project).

- [x] [CSGO](https://github.com/the-peon-project/peon-warplans/tree/main/csgo)
- [ ] [Starbound](https://github.com/the-peon-project/peon-warplans/tree/main/starbound)
- [x] [Valhiem](https://github.com/the-peon-project/peon-warplans/tree/main/valhiem)
- [x] [VRising](https://github.com/the-peon-project/peon-warplans/tree/main/vrising)

---

## Design Objectives

1. Define recipies with standardised `json` file.
2. Use the below *Image build hierarchy* definition to decide on the best course of action.

### Image build hierarchy

*\*Official container images are usually bespoke, so it may take some additional modification to the wider PEON app stack, which is not desirable.*

1. Use the official generic `steamcmd` container image *if exists*
2. Alternatively, use pre-existing generic PEON container image *if exists*
3. Use an official game server container image *if exists* \*
4. Alternatively Create a PEON compliant container

---

## Software Stack Diagram

*\*This may change as technologies & skills evolve.*

![Software Stack](./diagram_warplans.png)

---

## Navigation

Links to various project-related resources.

[![github](../../images/buttons/button_github.svg)](https://github.com/the-peon-project/peon-warplans)
[![github](../../images/buttons/button_bug.svg)](https://github.com/the-peon-project/peon-warplans/issues/new/choose)
[![github](../../images/buttons/button_changelog.svg)](./release_notes/02_warplans.md)

---

## Roadmap

Here you can see what the future holds.

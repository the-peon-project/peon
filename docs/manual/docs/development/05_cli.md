# CLI

A handy CLI to manage PEON services remotely (as well as to provide extended access/control)

## Installation

If not installed via installation script, the `peon-cli` can be installed manually.

1. Download & copy the `peon-cli` folder into your preferred path.
2. Create a folder/file `./config/peon_dir` in the root path of the `peon-cli` scripts folder.
3. Input the full path of the `peon` installation directory (e.g. `/home/myuser/peon`) into the `peon_dir` file in the `peon-cli` scripts folder.
4. Add your `peon-cli` script folder to your path (if you wish)

## Usage

### Interactive mode

The peon cli offers an interactive mode for administration services
Just run `./peon`

### Non-Interactive mode

Some standard peon-cli tools can be executed programmatically using flags.
Just run `./peon [flags]`

#### Supported Flags

```bash
    -h|--help       Display this (H)elp information.
    -t|--status     S(t)atus of all containers
    -l|--list       (L)ist running GAME containers.
    -m|--metrics    Performance statistics/(M)etrics for ALL running containers.
    -c|--capacity   Show storage space & (C)apacity usage for all docker components.
    -u|--update     (U)pdates infrastrcture containers.
    -d|--redeploy   Re(d)eploy the infrastructure containers. 
    -s|--start      (S)tarts infrastrcture conatiners.
    -p|--stop       Sto(p)s infrastrcture containers.
    -r|--restart    (R)estarts infrastrcture containers.
    -k|--kill       (K)ill ALL running containers.
```

## Roadmap

Here you can see what the future holds.

---

## Release Notes

**1.0.0**

- [x] CHANGE :tools: Removed `peon_dir` file from build. 
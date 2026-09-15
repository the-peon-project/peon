# CLI

A handy CLI to manage PEON services remotely (as well as to provide extended access/control)

## Installation

If not installed via the installation script, the CLI (`peon/cli/`) can be installed manually.

1. Copy the `cli/` folder from the `peon` monorepo into your preferred path.
2. Create a folder/file `./config/peon_dir` in the root path of that `cli/` folder.
3. Input the full path of the `peon` installation directory (e.g. `/home/myuser/peon`) into the `peon_dir` file in the `cli/` folder.
4. Add the `cli/bin` folder to your path (if you wish)

## Usage

### Interactive mode

The peon cli offers an interactive mode for administration services
Just run `./peon`

### Non-Interactive mode

Some standard CLI tools can be executed programmatically using flags.
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
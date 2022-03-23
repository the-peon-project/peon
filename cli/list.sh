#!/bin/bash
docker ps -a --format "table {{.Names}}\t{{.State}}"
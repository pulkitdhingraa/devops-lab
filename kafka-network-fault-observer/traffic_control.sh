#!/usr/bin/env bash
# traffic_control.sh
# Manage traffic control network emulator on a container's eth0 interface via docker exec.
# Usage: 
    # ./traffic_control.sh add <container> <delay>    # e.g. ./traffic_control.sh add kafka2 200ms
    # ./traffic_control.sh add "<netem-args>"         # e.g. "delay 200ms loss 1%"
    # ./traffic_control.sh show <container>
    # ./traffic_control.sh del <container>

set -eou pipefail

# :- means $1 i.e. first arg or DEFAULT i.e. ""
CMD="${1:-}"
CONTAINER="${2:-}"
ARG3="${3:-}"

usage() {
    cat <<EOF
Usage:
  $0 add  <container> <netem-args>   # e.g. $0 add kafka1 "delay 200ms"
  $0 add  <container> <delay>        # shorthand: "200ms" -> "delay 200ms"
  $0 show <container>                # show tc qdisc
  $0 del  <container>                # delete tc qdisc
Examples:
  $0 add kafka2 500ms
  $0 add kafka2 "delay 200ms loss 1%"
  $0 show kafka2
  $0 del kafka2
EOF
    exit 2
}

if [[ -z "$CMD" ]]; then
    usage
fi

case "$CMD" in
    add)
        if [[ -z "$CONTAINER" || -z "$ARG3" ]]; then
            echo "ERROR: add requires container and netem args" >&2
            usage
        fi

        if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
            echo "ERROR: Container doesn't exist or is not running." >&2
            exit 1
        fi

        if [[ "$ARG3" =~ ^[0-9]+(ms|s)$ ]]; then
            NETEM_ARGS="delay $ARG3"
        else
            NETEM_ARGS="$ARG3"
        fi

        if docker exec -u 0 "$CONTAINER" tc qdisc show dev eth0 root | grep -q netem; then
            echo "WARNING: A netem qdisc already exists on $CONTAINER; Use del first" >&2
            docker exec -u 0 "$CONTAINER" tc qdisc show dev eth0 root
            exit 1
        fi

        # Run the command to add delay
        docker exec -u 0 "$CONTAINER" tc qdisc add dev eth0 root netem $NETEM_ARGS
        echo "Done"
        ;;
    
    show)
        if [[ -z "$CONTAINER" ]]; then
            echo "ERROR: Show requires container name" >&2
            usage
        fi

        if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
            echo "ERROR: Container doesn't exist or is not running." >&2
            exit 1
        fi

        echo "Showing root qdisc on $CONTAINER"
        docker exec -u 0 "$CONTAINER" tc qdisc show dev eth0 root || true
        ;;

    del)
        if [[ -z "$CONTAINER" ]]; then
            echo "ERROR: Show requires container name" >&2
            usage
        fi

        if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
            echo "ERROR: Container doesn't exist or is not running." >&2
            exit 1
        fi

        echo "Deleting root disc on $CONTAINER"
        docker exec -u 0 "$CONTAINER" tc qdisc del dev eth0 root 2>/dev/null
        ;;
    *)
        usage
        ;;
    esac
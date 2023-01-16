#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/riyadh/Desktop/ezmile_ws/src/catvehicle"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/riyadh/Desktop/ezmile_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/riyadh/Desktop/ezmile_ws/install/lib/python3/dist-packages:/home/riyadh/Desktop/ezmile_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/riyadh/Desktop/ezmile_ws/build" \
    "/usr/bin/python3" \
    "/home/riyadh/Desktop/ezmile_ws/src/catvehicle/setup.py" \
     \
    build --build-base "/home/riyadh/Desktop/ezmile_ws/build/catvehicle" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/riyadh/Desktop/ezmile_ws/install" --install-scripts="/home/riyadh/Desktop/ezmile_ws/install/bin"

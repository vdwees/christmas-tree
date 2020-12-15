# USB Power Control over HTTP

A quick script to turn my USB christmas tree lights on and off. Runs on Raspberry Pi.

To use, clone and edit the service file as needed, copy it to `/lib/systemd/system`, refresh systemd and enable the service.

Its not elegant. All its doing is turning the usb ports on and off. On the other hand, this script works for any usb-powered device that needs to be turned on or off.

Note that an easy way to automate the trigger is to make a shortcut on an iOS device that requests the `/on`, `/off`, or `/toggle` endpoints

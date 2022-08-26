
Playscript Autoscroller
=======================

The **Script Scroller** is a utility permitting a play-script to scroll slowly
up the screen, with the speed and direction controllable via an external MIDI
controller.

Thus, a sound operator may make use of an expression pedal to keep their place
in the script, whilst keeping both hands on the faders of the sound desk. 


Dependencies
------------

As a baseline, you will need ``python`` 3.8 or better, along with ``pip`` for
that version.

All other dependencies are installed automatically by ``pip``; the full list of
run-time dependencies may be found in the ``setup.cfg`` file (build dependencies
in ``pyproject.toml``).


Installation
------------

From Source
"""""""""""

* Clone this repository locally,
* In its root directory, run ``pip install .``.

  - (You may need to use ``pip3`` on systems where that matters.)


From PyPI
"""""""""

Planned, but not yet available.


Running
-------

Once installed successfully, the program may be run by invoking
``script-scroller`` from a terminal window.

A linux ``.desktop`` file is planned for a later date.


Icon Credits
------------

The application icon is a combination of the ``x-office-address-book`` icon from
Gnome 3.2 and the ``mask`` icon from the Lucide_ iconset.

`Tango Project`_ (Public Domain) ::

  format-text-bold.svg
  format-text-italic.svg
  format-text-strikethrough.svg
  format-text-underline.svg

`Gnome Project (3.2)`_ (CC BY-SA 3.0) ::

  edit-clear.svg
  zoom-in.svg
  zoom-original.svg
  zoom-out.svg

Lucide_ (ISC) ::

  x.svg
  code.svg
  file-code.svg
  indent.svg
  outdent.svg
  pause.svg
  sidebar-close.svg
  sidebar-open.svg

`Simple Icons`_ (CC0 1.0) ::

  adobeacrobatreader.svg
  markdown.svg


.. _Gnome Project (3.2): https://github.com/GNOME/adwaita-icon-theme/tree/gnome-3-20/src/fullcolor
.. _Lucide: https://github.com/lucide-icons/lucide
.. _Simple Icons: https://simpleicons.org/
.. _Tango Project: https://www.tango-project.org/

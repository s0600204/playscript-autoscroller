
Playscript Autoscroller
=======================

The **Playscript Autoscroller** is a utility permitting a playscript to scroll
slowly up the screen, with the speed and direction controllable via an external
MIDI controller.

Thus, a sound operator may make use of an expression pedal to keep their place
in the script, freeing up their hands for other tasks such as operating the
faders of a sound desk.


Dependencies
------------

The dependencies fall roughly into two categories: those that can be installed
via ``pip``, and those that cannot.

The latter category currently comprises of the following:

* python (3.8 or better)
* either Qt5 or Qt6
* the matching Qt5/Qt6 SVG module

The program optionally supports the import and displaying of PDF documents
(except when running under PySide2). To use this functionality:

* If using Qt6 and...

  - *ArchLinux*: ``qt6-webengine``
  - *Debian*: either ``python3-pyqt6.qtpdf`` or ``python3-pyside6.qtpdf``
    depending on whether you intend to use the PyQt6 or PySide6 bindings
  - *MSys2*: ``qt6-pdf``
  - *Anything else*: determine which package(s) provide QtPdf and/or their
    PyQt6/PySide6 bindings (then report back, so it can be added to this list)

* If using PyQt5, then both ``Poppler`` and its Qt5 bindings (which might be
  installed as part of ``Poppler``) will be needed.

The dependencies that are installable via ``pip`` are installed through that
(if they are not already); the list of run-time dependencies may be found in
the ``setup.cfg`` file, and build dependencies in ``pyproject.toml``.

On the hardware side, it might be a good idea to have some form of MIDI
controller, a pedal capable of outputting MIDI, or a controller


Installation
------------

From Source
"""""""""""

* Clone this repository locally,
* In its root directory, run ``pip install .``.

  - (You may need to use ``pip3`` on systems where that matters.)


From PyPI
"""""""""

Planned, but not yet possible.


Running
-------

Once installed successfully, the program may be run by invoking
``playscript-autoscroller`` from a terminal window.

A linux ``.desktop`` file is planned for a later date.


Hardware support
----------------

This should work with any hardware capable of outputting MIDI Control Change
Messages. I myself use a `Midi Solutions`_ `Pedal Controller`_ monitoring a
Zoom `FP02 expression pedal`_, but I have previously used the output from a MIDI
strip on an Allen & Heath GLD80 sound desk.


Icon Credits
------------

The application icon is a combination of the ``x-office-address-book`` icon from
the `Gnome Project (3.2)`_ and the ``mask`` icon from the Lucide_ iconset.

Brand icons are provided by the `Simple Icons`_ project.

The UI icons are part of the Lucide_ iconset, or created by myself following the
Lucide style guidelines where a suitable icon was not available in the iconset.


Licencing
---------

The ``Palette Icon Engine``, originally written in C++ by Nick Korotysh, is
licenced under the terms of the GNU General Public license version 3 (GPL-v3).
The original source may be found at https://github.com/Kolcha/paletteicon.

Icons from the Lucide_ iconset are licenced under the `ISC license`_.

Icons from the `Simple Icons`_ iconset are licenced under the Creative Commons
Zero license version 1.0 (``CC0 1.0``).

The ``x-office-address-book`` icon from the `Gnome Project (3.2)`_ is licenced
under the Creative Commons Share-Alike 3.0 license (``CC BY-SA 3.0``).


.. _FP02 Expression Pedal: https://www.zoom.co.jp/products/fp02m-expression-pedal
.. _Gnome Project (3.2): https://github.com/GNOME/adwaita-icon-theme/tree/gnome-3-20/src/fullcolor
.. _ISC License: https://github.com/lucide-icons/lucide/blob/main/LICENSE
.. _Lucide: https://github.com/lucide-icons/lucide
.. _Midi Solutions: https://midisolutions.com/about.htm
.. _Pedal Controller: https://midisolutions.com/prodped.htm
.. _Simple Icons: https://simpleicons.org/

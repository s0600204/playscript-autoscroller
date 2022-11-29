
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
* Qt5
* Qt5 SVG module

Non-Windows systems also require:

* Poppler
* Poppler-Qt5 bindings (might be installed as part of Poppler)

(These are for importing of pdf files, a feature not working on Windows at this
time.)

The dependencies that are installable via ``pip`` are installed thusly (if not
already); the list of run-time dependencies may be found in the ``setup.cfg``
file, and build dependencies in ``pyproject.toml``.

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


.. _Midi Solutions: https://midisolutions.com/about.htm
.. _Pedal Controller: https://midisolutions.com/prodped.htm
.. _FP02 Expression Pedal: https://www.zoom.co.jp/products/fp02m-expression-pedal
.. _Gnome Project (3.2): https://github.com/GNOME/adwaita-icon-theme/tree/gnome-3-20/src/fullcolor
.. _Lucide: https://github.com/lucide-icons/lucide
.. _Simple Icons: https://simpleicons.org/
.. _Tango Project: https://www.tango-project.org/

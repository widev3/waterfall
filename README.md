# Whistle of Wind

This app is developed to control the Whistle of Wind radiotelescope connected to a RS spectrum analyzer.

# ui, ux
This app is developed from a custom implementation of a UI, UX toolchain with the goal of becoming a standard for implementing cross-platform applications.
* every `*.ui` file in `ui` package has its own corresponding `*.py` file in the same package which contains the code for the user interface. You can use Qt, PySide or any other library
* every `*.py` file in `ui` package has its own corresponding `*.py` file in `ux` package which contains the behaviour of the user interface
* to connect `*.py` in `ui` package (let call it `ui.py`) with `*.py` in `ux` package (let call it `ux.py`) you have just to pass the `ui` class in the `ux` constructor. Consider the following example:

The constructor of `ux` class is
```python
    def __init__(self, ui, dialog, args=None):
        self.ui = ui
        self.dialog = dialog
        self.args = args
        # ...
```
where:
* `ui` is the 
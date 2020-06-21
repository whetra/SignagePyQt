from enum import Enum
from .widgettimers import WidgetTimers


class CallbackType(Enum):
    NONE = 0
    FIRST_WIDGET = 1
    LAST_WIDGET = 2
    LAST_WIDGET_RESTART = 3
    CALLBACK_WIDGET = 4


class CombineWidget:

    def __init__(self, parentWidget, callback, widgets, callback_type=CallbackType.NONE, callback_widget=None):
        self.running = False
        self.parentWidget = parentWidget
        self.callback = callback
        self.timeout = 0
        self.widgets = widgets
        self.callback_type = callback_type
        self.callback_widget = callback_widget
        self.callbacks = set()
        for widget in self.widgets:
            widget.callback = self._widgetcallback
        self._timers = WidgetTimers(self._done, None, self._done)
        self._done_timeout = 100

    def start(self):
        self.running = True
        self.callbacks.clear()
        for widget in self.widgets:
            widget.start()

        if self.timeout > 0:
            self._timers.start_timeout_timer(self.timeout)

    def _done(self):
        self._timers.stop()
        self.callback(self)

    def stop(self):
        self.running = False
        self._timers.stop()
        for widget in self.widgets:
            widget.stop()

    def _widgetcallback(self, widget):
        if not self.running:
            return

        self.callbacks.add(widget)  # add widget to list of widget
        if self.callback_type is CallbackType.FIRST_WIDGET:
            if len(self.callbacks) == 1:  # if first one added
                self._timers.start_done_timer(self._done_timeout)
        elif self.callback_type is CallbackType.LAST_WIDGET:
            if len(self.callbacks) == len(self.widgets):  # if all are added
                self._timers.start_done_timer(self._done_timeout)
        elif self.callback_type is CallbackType.LAST_WIDGET_RESTART:
            if len(self.callbacks) == len(self.widgets):  # if all are added
                self._timers.start_done_timer(self._done_timeout)
            else:
                widget.stop()
                widget.start()
        elif self.callback_type is CallbackType.CALLBACK_WIDGET:
            if widget is self.callback_widget:
                self._timers.start_done_timer(self._done_timeout)

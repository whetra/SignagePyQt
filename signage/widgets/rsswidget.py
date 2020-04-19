from PyQt5 import QtWebKitWidgets
from datetime import datetime
from tools.timer import QTimerSingleShot
from lxml.html.clean import Cleaner
from lxml.etree import ParserError


class RssWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.rss_entry_provider = None
        self.timeout = 0
        self.entrytimeout = 5000
        self.darkmode = False
        self._timeout_timer = QTimerSingleShot(self._done)
        self._entry_timeout_timer = QTimerSingleShot(self._show_next_html)
        self._webEngineView1 = QtWebKitWidgets.QWebView(self.parentWidget)

    def start(self):
        self._webEngineView1.setGeometry(self.qrect)
        self._entries = self.rss_entry_provider.get_entries() if self.rss_entry_provider is not None else iter(())
        if self.timeout > 0:
            self._timeout_timer.start(self.timeout)
        self._show_next_html()
        self._webEngineView1.show()
        self._webEngineView1.raise_()

    def _show_next_html(self):
        try:
            entry = next(self._entries)
            html = self._calc_html(entry, self.qrect.height())
            self._show_html(html)
            self._entry_timeout_timer.start(self.entrytimeout)
        except StopIteration:
            self._done()

    def _show_html(self, html):
        self._webEngineView1.setHtml('')
        self._webEngineView1.setStyleSheet('background: transparent')
        self._webEngineView1.setHtml(html)

    def _done(self):
        self._entry_timeout_timer.stop()
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._entry_timeout_timer.stop()
        self._timeout_timer.stop()
        self._webEngineView1.setHtml('')
        self._webEngineView1.hide()

    def _calc_html(self, entry, widget_height):
        max_description_height = widget_height - 84 - 50  # - .title - .footer
        description = self._sanitize(entry.description)
        title_color = '#a1cfdf' if self.darkmode else '2b4b56'
        entry_background_color = 'rgba(0,0,0,0.6)' if self.darkmode else 'white'
        entry_color = '#EEEEEE' if self.darkmode else 'black'
        a_color = 'CCCC00' if self.darkmode else '0000FF'
        if entry.image:
            description += f'<div style="margin-top: 10px"><img src="{entry.image}" /></div>'
            entry.image = ''
        return (
            f"<html>"
            f"<head>"
            f"    <link href='https://fonts.googleapis.com/css?family=Open+Sans+Condensed:700|Source+Sans+Pro' rel='stylesheet' type='text/css'>"
            f"    <style>"
            f"        html {{ width: 100%; height: 100%; font-family: 'Source Sans Pro', sans-serif; font-size: 24px; }}"
            f"        body {{ width: 100%; height: 100%; margin: 0px; padding: 0px; overflow: hidden; }}"
            f"        .entry {{ display: block; margin: 0px; padding: 10px; "
            f"                  -webkit-border-radius: 8px; max-height: {widget_height}px; overflow: hidden; "
            f"                  background-color: {entry_background_color}; color: {entry_color}; font-family: 'Source Sans Pro', sans-serif; }}"
            f"        .title {{ display: block; min-height: 25px; max-height: 76px; margin-bottom: 8px; overflow: hidden; "
            f"                  color: {title_color}; font-family: 'Open Sans Condensed', sans-serif; font-size: 28px; font-weight:bold; }}"
            f"        .description {{ display: block; max-height: {max_description_height}px; overflow: hidden; }}"
            f"        img {{ max-width:100%; max-height:100%; }}"
            f"        .footer {{ display: block; max-height: 42px; margin-top: 8px; font-size: 18px; }}"
            f"        .date {{ margin: 0px 10px 0px 0px; }}"
            f"        .moreinfo {{ margin: 0px 0px 0px 10px; }}"
            f"        a {{ color: {a_color}; }}"
            f"    </style>"
            f"</head>"
            f"<body>"
            f"    <div class='entry'>"
            f"        <div class='title'>{entry.title}</div>"
            f"        <div class='description'>{description}</div>"
            f"        <div class='footer'>"
            f"           <span class='date'>{entry.published_datetime.strftime('%c')}</span>"
            f"           <span class='moreinfo'><a href='{entry.link}' target='_blank'>{entry.short_link}</a></span>"
            f"        </div>"
            f"    </div>"
            f"</body>"
            f"</html>")

    def _sanitize(self, dirty_html):
        if not dirty_html or dirty_html.isspace():
            return ''

        html = dirty_html.replace('<p>&nbsp;</p>', '')
        try:
            cleaner = Cleaner(
                page_structure=True,
                meta=True,
                embedded=True,
                links=True,
                style=True,
                processing_instructions=True,
                inline_style=True,
                scripts=True,
                javascript=True,
                comments=True,
                frames=True,
                forms=True,
                annoying_tags=True,
                remove_unknown_tags=True,
                safe_attrs_only=True,
                safe_attrs=frozenset(['src', 'color', 'href', 'title', 'class', 'name', 'id']),
                remove_tags=('span', 'font', 'div'))
            return cleaner.clean_html(html)

        except ParserError as e:
            print(f'{datetime.now()} RssWidget ParserError {e} ({dirty_html})')
            return ''

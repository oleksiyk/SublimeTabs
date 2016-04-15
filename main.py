import sublime, sublime_plugin, os, time

settings = {}

MAX_VIEWS = 20
MIN_WORD_SIZE = 3
MAX_WORD_SIZE = 50

def plugin_loaded():
    global settings
    settings = sublime.load_settings("Tabs.sublime-settings")


def filter_completions(completions):
    result = []
    used_words = []
    for w, v in completions:
        if w not in used_words and MIN_WORD_SIZE <= len(w) <= MAX_WORD_SIZE:
            used_words.append(w)
            result.append((w, v))
    return result

class Tabs(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        if ( settings.get("filename_in_statusbar") ):
            home = os.path.expanduser("~")
            filename = view.file_name()
            if filename:
                view.set_status('zTabs-FilePath', filename.replace(home, '~'))

    def on_new(self, view):
        if ( settings.get("close_tabs") ):
            modifiedTTL = int(settings.get('keep_modified_in'))
            accessedTTL = int(settings.get('keep_accessed_in'))
            keep_tabs   = int(settings.get('keep_tabs'))
            window = sublime.active_window()

            now = time.time()
            active_view = window.active_view()
            outdated_views = []

            for oView in window.views():
                path = oView.file_name()

                if (
                    oView != active_view
                    and not oView.is_loading()
                    and not oView.is_scratch()
                    and not oView.is_dirty()
                    and path
                    and os.path.exists(path)
                    and now - os.path.getatime(path) > accessedTTL
                ):
                    mtime = os.path.getmtime(path)
                    if (now - mtime > modifiedTTL):
                        outdated_views.append((mtime, oView))

            outdated_views = sorted(outdated_views, key=lambda view: view[0])
            num_to_close = len(window.views()) - keep_tabs + 1 # add 1 for the newly opened tab

            if num_to_close > 0:
                for mtime, oView in outdated_views[0:num_to_close]:
                    window.focus_view(oView)
                    window.run_command('close_file')

    def on_query_completions(self, view, prefix, locations):
        if ( settings.get("autocomplete_open_files") ):
            words = []
            views = sublime.active_window().views()
            views = [view] + views
            views = views[0:MAX_VIEWS]
            for oView in views:
                if( oView.settings().get('syntax') == view.settings().get('syntax')):
                    if len(locations) > 0 and oView.id == view.id:
                        words += [(item, oView) for item in oView.extract_completions(prefix, locations[0])]
                    else:
                        words += [(item, oView) for item in oView.extract_completions(prefix)]

            # words = list(set(words)) # unique
            words = filter_completions(words)

            completions = []
            for w, v in words:
                trigger = w
                contents = w.replace('$', '\\$')
                if v.id != view.id and v.file_name():
                    trigger += '\t(%s)' % os.path.basename(v.file_name())
                completions.append((trigger, contents))

            # print(completions)
            return completions


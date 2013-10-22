import sublime, sublime_plugin, os, time

settings = {}

def plugin_loaded():
    global settings
    settings = sublime.load_settings("Tabs.sublime-settings")

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
            completions = []
            for oView in sublime.active_window().views():
                if( oView.settings().get('syntax') == view.settings().get('syntax') and oView != view):
                    completions += [(item, item) for item in oView.extract_completions(prefix) if len(item) > 3 and len(item) < 50]

            completions = list(set(completions)) # unique
            return completions


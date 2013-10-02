import sublime, sublime_plugin, json, os
from pprint import pprint
from os import path
from Scanner import Scanner

print 'Init Filepath completion'




class FilePathComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        

        # get the open project folders
        pdirs = view.window().folders()

        pline = self._get_pointer_line(view)

        sc = Scanner(pline)

        completions = sc.get_comp_list()
        print 'Got Completions: ' + repr(completions) + ' in ' + os.getcwd()

        #completions = ['hello', 'blub']

        return (completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS)

    def _get_pointer_line(self, view):
        point = view.sel()[0].begin()
        line_point = view.rowcol(point)[1]
        line_region = view.line(point)
        line_string = view.substr(line_region)
        return line_string[:line_point]

    def get_autocomplete_list(self, word):
        print 'called get get_autocomplete_list'

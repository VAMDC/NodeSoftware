# -*- coding: utf-8 -*-
from django.http import QueryDict

class SearchForm:
    def __init__(self, post_data):
        self.valid = False
        try:
            if post_data.get('numin') == '':
                self.numin = 0.
            else:
                self.numin = float(post_data.get('numin'))
            self.numax = float(post_data.get('numax'))
            if post_data.get('Smin') == '':
                self.Smin = 0.
            else:
                self.Smin = float(post_data.get('Smin'))
            if self.Smin < 0.:
                # negative Smin is silly but OK
                self.Smin = 0.
        except ValueError:
            return
        if self.numin > self.numax:
            # numin must be <= numax
            return

        selected_molecIDs = post_data.getlist('molecule')
        if not selected_molecIDs:
            # no molecules selected!
            return
        # make sure the selected_molecIDs are integers
        for molecID in selected_molecIDs:
            try:
                dummy = int(molecID)
            except ValueError:
                return
        self.selected_molecIDs = selected_molecIDs

        self.valid = True
        return

    def is_valid(self):
        if self.valid:
            return True
        return False


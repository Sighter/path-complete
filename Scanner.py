from os import path
import os


PSEP = '/'

class Scanner:

    def __init__(self, line, pdirs=[]):
        self.line = line.strip()

        # parse the stripped line
        
        self.absolute_candidate, self.relative_candidate, self.base = self._get_last_valid_tuple(self.line, pdirs)

    def get_comp_list(self):
        a = self.get_absolute_prefix()
        r = self.get_relative_prefix()
        b = self.get_basename()

        p = self.smart_choose(a, r)

        matches = self._get_matching_dir_contents(p, b)

        formatted = []

        for m in matches:
            formatted.append((m + '\tFC', m))

        return formatted

    def get_absolute_prefix(self):
        return self.absolute_candidate

    def get_relative_prefix(self):
        return self.relative_candidate

    def get_basename(self):
        return self.base

    def smart_choose(self, p1, p2):
        if p1 == None:
            return p2

        if p2 == None:
            return p1

        if p1.find(p2) != -1:
            return p1

        if p2.find(p1) != -1:
            return p2

        raise ErrorSmartChoose('Something went wrong in smart_choose. Values: ' + repr((p1, p2)))

    def _get_matching_dir_contents(self, dpath, prefix):
        matches = []

        if (dpath == ''):
            dpath = '.'

        if not path.exists(dpath):
            return None
        
        entries = os.listdir(dpath)
        #print ('path entries: ' + repr(entries))
        #print ('prefix: ' + repr(prefix))

        if prefix == '' or prefix == None:
            return entries

        for e in entries:
            if e.find(prefix) != -1:
                matches.append(e)


        return matches

    def _get_last_valid_tuple(self, line, pdirs):
        current_longest = ""
        absolute_candidate = None
        relative_candidate = None

        tup = line.rpartition(PSEP)
        #print repr(tup)
        
        # if first two bits of the tuple are empty, we can at least
        # use the last words for relative completion
        
        if tup[0] == '' and tup[1] == '':
            return (None, '', line)

        # if condition there does not met, we have to get the longest
        # valid path and basename
        basename = tup[2]
        lpart = tup[0] + PSEP

        # return on only slash
        #if basename.strip() == '' and lpart.strip() == '':
        #    return (PSEP, basename)

        #print 'handling lpart ' + lpart

        idx = len(lpart) - 1

        # check if we find a lpart path
        while idx >= -1:
            tmp = ""

            # handle beginning of line
            if idx == -1:
                char = ' '
            else:
                char = lpart[idx]

            if char == PSEP or not char.isalnum():
                if path.exists(current_longest):
                    tmp = current_longest

            if tmp.startswith(PSEP) == True:
                absolute_candidate = tmp
            elif len(tmp) != 0:
                relative_candidate = tmp

            current_longest = char + current_longest

            if char == PSEP or not char.isalnum():
                if path.exists(current_longest):
                    tmp = current_longest

            if tmp.startswith(PSEP) == True:
                absolute_candidate = tmp
            elif len(tmp) != 0:
                relative_candidate = tmp

            idx = idx - 1

        if basename == '':
            basename = None

        r = (absolute_candidate, relative_candidate, basename)

        return r


class ErrorSmartChoose(Exception):
    """docstring for  ErrorConfigPathWrong"""
    def __init__(self, message):
        Exception.__init__(self,message)


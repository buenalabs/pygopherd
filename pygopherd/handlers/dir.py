import SocketServer
import re
import os, stat, os.path, mimetypes, protocols
import handlers, handlers.base

class DirHandler(handlers.base.BaseHandler):
    def canhandlerequest(self):
        """We can handle the request if it's for a file."""
        return os.path.isdir(self.getfspath())

    def getentry(self):
        if not self.entry:
            self.entry = entry.GopherEntry(self.selector, self.config)
            self.entry.populatefromfs(self.getfspath())
        return self.entry

    def write(self, wfile):
        files = os.listdir(self.path)
        files.sort()

        selectorbase = self.selector
        if selectorbase == '/':
            selectorbase = ''           # Avoid dup slashes
        fsbase = self.getfspath()
        if fsbase == '/':
            fsbase = ''                 # Avoid dup slashes

        for file in files:
            entry = entry.GopherEntry(selectorbase + '/' + file,
                                      self.config)
            self.entry.populatefromfs(self.getfspath())
            wfile.write(self.protocol.renderobjinfo(self))
            
#!/usr/bin/env python

import os
import readline
import logging
import sys


class CommandLine(object):

    def __init__(self):
        self.keywords = {}
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.tab_complete)
        self.running = True
        self.preprompt = "Exp sh"
        self.prompt = ""
        self.postprompt = ":> "


    def shutdown(self):
        self.running = False


    def tab_complete(self, text, state):
        response = None
        if state == 0:
            # this is the first time for this text, so build a match list

            origline = readline.get_line_buffer()   # the full command line
            begin = readline.get_begidx()           # begin of word being completed
            end = readline.get_endidx()             # end of word being completed
            being_completed = origline[begin:end]   # word being completed
            words = origline.split()
            if len(words) < 1:
                completed_words = []
            elif being_completed:
                completed_words = words[0:-1]
            else:
                completed_words = words

            if not words:
                # command line is empty
                self.cur_complete_candidates = sorted(self.keywords.keys())

            else:
                try:
                    if begin == 0:
                        # first word
                        candidates = self.keywords.keys()
                    else:
                        # later word
                        first = words[0]
                        cmd = self.keywords[first]
                        candidates = cmd.complete_cmd(completed_words)

                    if being_completed:
                        # filter candidates that match the already given portion
                        self.cur_complete_candidates = [
                            x for x in candidates if x.startswith(being_completed)
                            ]
                    else:
                        # being_completed is empty, so use all candidates
                        self.cur_complete_candidates = candidates
                except (KeyError, IndexError), err:
                    self.cur_complete_candidates = []
        if state >= len(self.cur_complete_candidates):
            response = None
        else:
            response = self.cur_complete_candidates[state]

        return response

    def set_prompt(self, msg):
        logging.debug("changing prompt to '%s'", msg)
        self.prompt = msg

    def get_full_prompt(self):
        if self.prompt:
            return "%s %s %s" % (self.preprompt, self.prompt, self.postprompt)
        return "%s %s" % (self.preprompt, self.postprompt)

    def start(self):
        logging.debug("starting command line")
        line = ''
        while self.running:
            try:
                raw_line = raw_input(self.get_full_prompt())
                line = raw_line.strip()
                if len(line) == 0:
                    continue

                token = line.split()
                cmd = token[0]
                args = token[1:]

                if cmd == "help":
                    logging.debug("help command")
                    self.show_help(args)

                elif cmd in self.keywords:
                    klass = self.keywords[cmd]
                    logging.debug("running command '%s' with args: %s", cmd,
                            args)
                    klass.run(args)
                    logging.debug("command '%s' ended", cmd)

                else:
                    print "unknown command '%s'" % cmd

            except (KeyboardInterrupt, EOFError):
                print "use 'quit' to exit"

            except:
                print "unexpected error: (%s) %s" % (
                        sys.exc_info()[0], sys.exc_info()[1])


    def register(self, command):
        keyword = command.get_keyword()
        if keyword == None:
            raise NameError("command %s has no keyword defined" % command.__class__)
        elif keyword in self.keywords:
            raise NameError("error: keyword %s already defined" % keyword)

        self.keywords[keyword] = command

    def show_help(self, args):
        print "availible commands:"
        for i in self.keywords.keys():
            print " %s: %s" % (i, self.keywords[i].desctiption())





class Command(object):

    def __init__(self):
        pass

    def get_keyword(self):
        """
        command be which this Command instance should be identified and called
        (single word string)
        """
        return None

    def complete_cmd(self, args):
        """
        return a list of words which can be used to complete the entered command.
        args contains all already entered and completed words (including the
        command itself)
        """
        return []

    def desctiption(self):
        """
        return a one line help string
        """
        return ""

    def help(self, args = None):
        """
        return a help string. if args == None, print a full command summay
        otherwise print help for the given arguments
        """
        return ""

    def set_mgr(self, mgr):
        """
        call this method in your constructor
        """
        self.mgr = mgr

    def yes_no_question(self, msg):
        """
        print msg with additional '? [y/n]' and waits for a 'y' or 'n'
        if 'y' True is returned, otherwise false
        """
        line = raw_input("%s [y/n] " % msg)
        line = line.lower()
        while line not in ['y', 'n']:
            line = raw_input("answer 'y' or 'n': ").lower()

        return (line.lower() == 'y')

    def run(self, args):
        """
        called if user entered the keyword for this command.
        args contains a list of all arguments (without the command keyword itself)
        """
        raise NotImplementedError("this is the abstract command")


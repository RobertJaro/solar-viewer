import pkgutil

import pip
import wx


class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class InstallUtil:
    @staticmethod
    def checkPackage(pkg_name):
        pkg = pkgutil.find_loader(pkg_name)
        if pkg is not None:
            return True
        dlg = wx.MessageDialog(None,
                               "This action request additional python modules. Do you want to install them now?",
                               style=wx.YES_NO | wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            bi = wx.BusyInfo("Installing " + pkg_name)
            cmd_name, cmd_args = pip.parseopts(['install', pkg_name])
            command = pip.commands_dict[cmd_name](isolated=pip.check_isolated(cmd_args))
            command.main(cmd_args)
            del bi
            return True
        else:
            return False

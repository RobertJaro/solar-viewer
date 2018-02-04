import os

import wx

import sunpyviewer.resources


def saveFigure(parent, figure):
    canvas = figure.canvas
    filetypes, exts, filter_index = canvas._get_imagesave_wildcards()
    default_file = canvas.get_default_filename()
    f_dlg = wx.FileDialog(parent, "Save to file", "", default_file,
                          filetypes,
                          wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    f_dlg.SetFilterIndex(filter_index)
    if f_dlg.ShowModal() != wx.ID_OK:
        return
    dirname = f_dlg.GetDirectory()
    filename = f_dlg.GetFilename()
    format = exts[f_dlg.GetFilterIndex()]
    basename, ext = os.path.splitext(filename)
    if ext.startswith('.'):
        ext = ext[1:]
    if ext in ('svg', 'pdf', 'ps', 'eps', 'png') and format != ext:
        # looks like they forgot to set the image type drop
        # down, going with the extension.
        format = ext
    dpi_dlg = wx.TextEntryDialog(parent, 'Select DPI (leave blank for default):', 'DPI selection')
    if dpi_dlg.ShowModal() == wx.ID_OK:
        try:
            dpi = int(dpi_dlg.GetValue())
        except ValueError:
            dpi = None
    figure.savefig(os.path.join(dirname, filename), format=format, dpi=dpi)

    f_dlg.Destroy()
    dpi_dlg.Destroy()


def saveFits(parent, content):
    dir, file = "", ""
    if hasattr(content, "path"):
        dir, file = os.path.split(content.path)
    dlg = wx.FileDialog(parent, "Save to file", dir, file, "FITS files (*.fits)|*.fits",
                        wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dlg.ShowModal() == wx.ID_OK:
        content.save(dlg.GetPath(), overwrite=True)


def getMapName(map):
    try:
        return map.name
    except:
        return "Map"


resources_dir = os.path.dirname(sunpyviewer.resources.__file__)

import os
from src.file_handler.file_handler import combine_paths, ensure_remove_file, get_absolute_path, read_from_file, write_to_file
from src.graphical_interface.common import EVT_CHANGE_PANEL_EVENT, ImageSize
import wx
from src.graphical_interface.recognition_panel import RecognitionPanel
from src.graphical_interface.synthesis_panel import SynthesisPanel


class Frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title, position, size):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=position, size=size)

        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Recognition Mode")

        main_color = wx.Colour(228, 228, 228)
        second_color = wx.Colour(161, 183, 168)

        font = wx.Font(20, wx.MODERN, wx.NORMAL,
                       wx.NORMAL, False, 'Arial')

        self.synthesis_panel = SynthesisPanel(
            self, self.statusBar, main_color, second_color, self.find_models(), font)
        self.recognition_panel = RecognitionPanel(
            self, self.statusBar, main_color, second_color, font)
        self.panel = "recognition"
        self.synthesis_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.synthesis_panel, 1, wx.EXPAND)
        self.sizer.Add(self.recognition_panel, 1, wx.EXPAND)
        self.sizer.SetMinSize(1050, 550)
        self.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(EVT_CHANGE_PANEL_EVENT, self.on_switch_panels)

        menuBar = wx.MenuBar()
        # ------------------ menu - File ------------------ #

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_SAVE, "S&ave\tAlt-S", helpString="Save result")
        file_menu.Append(wx.ID_OPEN, "L&oad\tAlt-L", helpString="Load text")
        menuBar.Append(file_menu, "&File")

        # ------------------ menu - File ------------------ #

        # ------------------ menu - Options ------------------ #

        self.option_menu = wx.Menu()
        size_menu = wx.Menu()
        size_menu.Append(108, "900px",
                         "900px line width", wx.ITEM_RADIO)
        size_menu.Append(107, "675px",
                         "675px line width", wx.ITEM_RADIO)
        size_menu.Append(106, "450px",
                         "450px line width", wx.ITEM_RADIO)

        self.option_menu.Append(105, 'Line width', size_menu)
        self.option_menu.Check(107, True)
        self.option_menu.Enable(105, False)

        self.option_menu.Append(
            104, 'Use GPU', 'Use GPU in synthesize', wx.ITEM_CHECK)
        self.option_menu.Enable(104, False)

        self.option_menu.Append(
            103, 'Disable Synthesis', 'Disables the synthesis and uses only original images', wx.ITEM_CHECK)
        self.option_menu.Enable(103, False)

        self.option_menu.AppendSeparator()

        advanced_option_menu = wx.Menu()

        filters_menu = wx.Menu()
        filters_menu.Append(113, "Original",
                            "The control points are not filterd", wx.ITEM_RADIO)
        filters_menu.Append(114, "Consecutive",
                            "The consecutive filter is applied to the control points", wx.ITEM_RADIO)
        filters_menu.Append(115, "Random",
                            "The random filter is applied to the control points", wx.ITEM_RADIO)
        filters_menu.Append(116, "BS",
                            "The binary search filter is applied to the control points", wx.ITEM_RADIO)

        advanced_option_menu.Append(112, 'Filters', filters_menu)

        advanced_option_menu.Append(
            111, "Filter options", helpString="Filter options")

        self.synthesize_menu = wx.Menu()
        self.match_with_other = False

        advanced_option_menu.Append(
            121, "Use matching", "Match with other instance of the letter in generation", wx.ITEM_CHECK)

        self.option_menu.Append(110, 'Advanced', advanced_option_menu)
        self.option_menu.Enable(110, False)

        self.option_menu.AppendSeparator()

        self.option_menu.Append(98, "E&xit\tAlt-X",
                                "Exit the application")

        menuBar.Append(self.option_menu, "&Options")
        # ------------------ menu - Options ------------------ #

        # ------------------ menu - About ------------------ #
        about_menu = wx.Menu()
        about_menu.Append(99, "A&bout the project\tAlt-A",
                          "Show informations about the application")

        about_menu.Append(100, "Au&thors\tAlt-U",
                          "Show informations about the application authors")

        menuBar.Append(about_menu, "&About")
        # ------------------ menu - About ------------------ #
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.menuhandler)

        path = get_absolute_path("resources/Bachelor_Thesis.ico")
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def find_models(self):
        entries = [name for name in os.listdir(
            './data/synthesis_models') if not name.startswith('.')]
        return sorted(entries, key=lambda x: int(os.path.splitext(x)[0]))

    def menuhandler(self, event):  # noqa: C901
        id = event.GetId()
        if id == 98:
            self.menu_close(event)
        elif id == 99:
            self.show_information(event)
        elif id == wx.ID_SAVE:
            self.save(event)
        elif id == 100:
            self.show_authors(event)
        elif id == wx.ID_OPEN:
            self.load_text(event)
        elif id == 106:
            self.synthesis_panel.change_image_size(ImageSize.Small)
        elif id == 107:
            self.synthesis_panel.change_image_size(ImageSize.Medium)
        elif id == 108:
            self.synthesis_panel.change_image_size(ImageSize.Large)
        elif id == 104:
            if self.synthesis_panel.use_gpu:
                self.synthesis_panel.use_gpu = False
            else:
                self.synthesis_panel.use_gpu = True
            self.statusBar.SetStatusText(
                'Use GPU set to ' + str(self.synthesis_panel.use_gpu))
        elif id == 103:
            if self.synthesis_panel.use_synthesis:
                self.synthesis_panel.use_synthesis = False
                self.statusBar.SetStatusText('Synthesis disabled')
            else:
                self.synthesis_panel.use_synthesis = True
                self.statusBar.SetStatusText('Synthesis enabled')
        elif id == 111:
            self.synthesis_panel.on_advanced_options()
        elif id == 113:
            self.synthesis_panel.change_filter_type('Original')
        elif id == 114:
            self.synthesis_panel.change_filter_type('Consecutive')
        elif id == 115:
            self.synthesis_panel.change_filter_type('Random')
        elif id == 116:
            self.synthesis_panel.change_filter_type('BS')
        elif id == 121:
            self.synthesis_panel.change_match_flag()

    def load_text(self, event):
        with wx.FileDialog(self, 'Load file', wildcard='Text files (*.txt)|*.txt', style=wx.FD_OPEN) as fd:
            if fd.ShowModal() == wx.ID_OK:
                filename = fd.GetPath()
                txt = read_from_file(filename)
                if self.panel == "synthesis":
                    self.synthesis_panel.editname.SetValue(txt)
                else:
                    self.recognition_panel.editname.SetValue(txt)

    def show_information(self, event):
        wx.MessageBox('This is the application created for Bachelor Thesis at Warsaw University of Technology Faculty of Mathematics and Information Science.', 'Information', wx.OK)

    def show_authors(self, event):
        wx.MessageBox(
            'The authors of the application are: \n - Martin Mrugała \n - Patryk Walczak \n - Bartłomiej Żyła \n\n Thesis supervisor: \n - Agnieszka Jastrzębska, Ph.D. Eng', 'Authors', wx.OK)

    def menu_close(self, event):
        self.Close()

    def on_close(self, event):
        dlg = wx.MessageDialog(
            None, "Do you want to exit?", 'See you later?', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()

        if result == wx.ID_YES:
            event.Skip()

    def on_switch_panels(self, event):
        if self.synthesis_panel.IsShown():
            self.recognition_panel.editname.SetValue(
                self.synthesis_panel.editname.GetValue())
            self.synthesis_panel.Hide()
            self.recognition_panel.Show()
            self.statusBar.SetStatusText("Recognition Mode")
            self.panel = "recognition"
            self.option_menu.Enable(105, False)
            self.option_menu.Enable(104, False)
            self.option_menu.Enable(110, False)
            self.option_menu.Enable(103, False)
        else:
            self.synthesis_panel.editname.SetValue(
                self.recognition_panel.editname.GetValue())
            self.synthesis_panel.Show()
            self.recognition_panel.Hide()
            self.statusBar.SetStatusText("Synthesis Mode")
            self.panel = "synthesis"
            self.option_menu.Enable(105, True)
            self.option_menu.Enable(104, True)
            self.option_menu.Enable(110, True)
            self.option_menu.Enable(103, True)
        self.Layout()

    def save(self, event):
        """
        Saves created image
        """
        if self.panel == "synthesis":
            with wx.FileDialog(self, 'Save image', wildcard='PNG files (*.png)|*.png', style=wx.FD_SAVE) as fd:
                if fd.ShowModal() == wx.ID_OK:
                    filename = fd.GetPath()
                    img = self.synthesis_panel.imageCtrl.GetBitmap()
                    if len(filename) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        img.SaveFile(filename, wx.BITMAP_TYPE_PNG)
                        print('Image is saved in file \'' + filename)
                        self.statusBar.SetStatusText('File saved')
                    txt = self.synthesis_panel.editname.GetValue()
                    if len(txt) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        filename = str.replace(filename, '.png', '.txt')
                        write_to_file(filename, txt)
                        print('Text \'' + txt +
                              '\' is written in file \'' + filename)
                        self.statusBar.SetStatusText('File saved')
        elif self.panel == "recognition":
            with wx.FileDialog(self, 'Save text', wildcard='text files (*.txt)|*.txt', style=wx.FD_SAVE) as fd:
                if fd.ShowModal() == wx.ID_OK:
                    filename = fd.GetPath()
                    txt = self.recognition_panel.editname.GetValue()
                    if len(txt) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        write_to_file(filename, txt)
                        print('Text \'' + txt +
                              '\' is written in file \'' + filename)
                        self.statusBar.SetStatusText('File saved')


class Application(wx.App):
    def OnInit(self):
        frame = Frame(None, "Scripturam", (150, 150), (1100, 720))
        frame.Show()
        return True


if __name__ == '__main__':
    path_to_logs = get_absolute_path('.')
    path_to_logs = combine_paths(path_to_logs, "application_logs.txt")
    ensure_remove_file(path_to_logs)
    app = Application(redirect=True, filename=path_to_logs)
    app.MainLoop()

import wx
import wx.wizard
import wx.lib.mixins.listctrl as listmix
from logging import getLogger

import pkg_resources

from sync.controllers import localbox_ctrl
from sync.controllers.account_ctrl import AccountController
from sync.controllers.localbox_ctrl import SyncsController
from sync.controllers.login_ctrl import LoginController, InvalidPassphraseError
from sync.controllers.preferences_ctrl import ctrl as preferences_ctrl
from sync.controllers.shares_ctrl import SharesController, ShareItem
from sync.defaults import DEFAULT_LANGUAGE
from sync.gui import gui_utils
from sync.gui.gui_utils import MAIN_FRAME_SIZE, MAIN_PANEL_SIZE, \
    MAIN_TITLE, DEFAULT_BORDER, PASSPHRASE_DIALOG_SIZE, PASSPHRASE_TITLE
from sync.gui.wizard import NewSyncWizard
from sync.language import LANGUAGES
from sync.localbox import LocalBox, InvalidLocalBoxPathError


class LocalBoxApp(wx.App):
    """
    class that extends wx.App and only permits a single running instance.
    """

    def OnInit(self):
        """
        wx.App init function that returns False if the app is already running.
        """
        self.name = "LocalBoxApp-%s".format(wx.GetUserId())
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox(
                "An instance of the application is already running",
                "Error",
                wx.OK | wx.ICON_WARNING
            )
            return False
        return True


class Gui(wx.Frame):
    def __init__(self, parent, event, main_syncing_thread):
        super(Gui, self).__init__(parent,
                                  title=MAIN_TITLE,
                                  size=MAIN_FRAME_SIZE,
                                  style=wx.CLOSE_BOX | wx.CAPTION)

        # Attributes
        self._main_syncing_thread = main_syncing_thread
        self.event = event
        self.toolbar_panels = dict()
        self.panel_syncs = SyncsPanel(self, event, main_syncing_thread)
        self.panel_shares = SharePanel(self)
        self.panel_account = AccountPanel(self)
        self.panel_preferences = PreferencesPanel(self)
        self.panel_bottom = BottomPanel(self)
        self.panel_line = wx.Panel(self)

        line_sizer = wx.BoxSizer(wx.VERTICAL)
        line_sizer.Add(wx.StaticLine(self.panel_line, -1), 0, wx.ALL | wx.EXPAND, border=10)
        self.panel_line.SetSizer(line_sizer)

        self.ctrl = self.panel_syncs.ctrl

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.panel_line, 0, wx.EXPAND, border=10)
        bSizer1.Add(self.panel_syncs, 0, wx.EXPAND, 10)
        bSizer1.Add(self.panel_shares, 0, wx.EXPAND, 10)
        bSizer1.Add(self.panel_account, 0, wx.EXPAND, 10)
        bSizer1.Add(self.panel_preferences, 0, wx.EXPAND, 10)
        bSizer1.Add(self.panel_bottom, 0, wx.ALIGN_BOTTOM, 10)

        self.SetSizer(bSizer1)

        self.InitUI()

        self.show_first_panels()

        self.SetAutoLayout(True)
        self.SetSizer(bSizer1)
        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.on_close)

        # ask passphrase for each label
        map(lambda i: PassphraseDialog(self, username=i.user, label=i.label, site=i.url).Show(),
            SyncsController().load())

    def InitUI(self):

        self.add_toolbar()

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(gui_utils.iconpath(), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def on_close(self, event):
        self.Hide()
        event.Veto(True)

    def add_toolbar(self):
        self.toolbar = self.CreateToolBar(style=wx.TB_TEXT)

        self.toolbar.AddStretchableSpace()
        stream = pkg_resources.resource_stream('sync.resources.images', 'sync.png')
        bt_toolbar_localboxes = self.toolbar.AddLabelTool(wx.ID_ANY, _('Syncs'), wx.BitmapFromImage(
            wx.ImageFromStream(
                stream,
                wx.BITMAP_TYPE_PNG
            )
        ))
        stream = pkg_resources.resource_stream('sync.resources.images', 'share.png')
        bt_toolbar_shares = self.toolbar.AddLabelTool(wx.ID_ANY, _('Shares'), wx.BitmapFromImage(
            wx.ImageFromStream(
                stream,
                wx.BITMAP_TYPE_PNG
            )
        ))
        stream = pkg_resources.resource_stream('sync.resources.images', 'user.png')
        bt_toolbar_account = self.toolbar.AddLabelTool(wx.ID_ANY, _('Account'), wx.BitmapFromImage(
            wx.ImageFromStream(
                stream,
                wx.BITMAP_TYPE_PNG
            )
        ))
        stream = pkg_resources.resource_stream('sync.resources.images', 'preferences.png')
        bt_toolbar_preferences = self.toolbar.AddLabelTool(wx.ID_ANY, _('Preferences'), wx.BitmapFromImage(
            wx.ImageFromStream(
                stream,
                wx.BITMAP_TYPE_PNG
            )
        ))
        self.toolbar.AddStretchableSpace()

        self.toolbar.Realize()

        self.toolbar.EnableTool(bt_toolbar_localboxes.Id, False)

        self.toolbar_panels[bt_toolbar_localboxes.Id] = self.panel_syncs
        self.toolbar_panels[bt_toolbar_shares.Id] = self.panel_shares
        self.toolbar_panels[bt_toolbar_account.Id] = self.panel_account
        self.toolbar_panels[bt_toolbar_preferences.Id] = self.panel_preferences

        self.Bind(wx.EVT_TOOL, self.OnToolbarLocalboxesClick, id=bt_toolbar_localboxes.Id)
        self.Bind(wx.EVT_TOOL, self.OnToolbarLocalboxesClick, id=bt_toolbar_shares.Id)
        self.Bind(wx.EVT_TOOL, self.OnToolbarLocalboxesClick, id=bt_toolbar_account.Id)
        self.Bind(wx.EVT_TOOL, self.OnToolbarLocalboxesClick, id=bt_toolbar_preferences.Id)

    def show_first_panels(self):
        self.panel_syncs.Show()
        self.panel_shares.Hide()
        self.panel_account.Hide()
        self.panel_preferences.Hide()

    def hide_before_login(self):
        self.toolbar.Hide()

        self.panel_line.Hide()
        self.panel_syncs.Hide()
        self.panel_account.Hide()
        self.panel_preferences.Hide()

    def on_successful_login(self):
        self.toolbar.Show()

        self.ctrl = self.panel_syncs.ctrl

        self.panel_line.Show()
        self.panel_syncs.Show()

    def OnQuit(self, e):
        self.Close()

    def OnToolbarLocalboxesClick(self, event):
        for i in range(0, self.toolbar.GetToolsCount()):
            tool = self.toolbar.GetToolByPos(i)
            if tool.Id == event.Id:
                self.toolbar.EnableTool(tool.Id, False)
            else:
                self.toolbar.EnableTool(tool.Id, True)

        for item in self.toolbar_panels.items():
            if item[0] == event.Id:
                item[1].Show()
                self.ctrl = item[1].ctrl
            else:
                item[1].Hide()

        self.Layout()


# ----------------------------------- #
# ----       MAIN PANELS         ---- #
# ----------------------------------- #
class SyncsPanel(wx.Panel):
    """
    Custom Panel containing a ListCtrl to list the syncs/localboxes
    """

    def __init__(self, parent, event, main_syncing_thread):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=MAIN_PANEL_SIZE)

        # Attributes
        self._main_syncing_thread = main_syncing_thread
        self.event = event
        self.ctrl = LocalboxListCtrl(self)
        self.btn_add_localbox = wx.Button(self, label=_('Add'), size=(70, 30))
        self.btn_delete = wx.Button(self, label=_('Delete'), size=(70, 30))

        # Layout
        self._DoLayout()

        # Bind events
        self.Bind(wx.EVT_BUTTON, self.newSyncDialog, self.btn_add_localbox)
        self.Bind(wx.EVT_BUTTON, self.delete_localbox, self.btn_delete)

        # Setup
        self.ctrl.populate_list()

    def _DoLayout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.ctrl, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.btn_add_localbox)
        hbox4.Add(self.btn_delete)
        vbox.Add(hbox4, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        vbox.Add((-1, 25))

        self.SetSizer(vbox)

    def newSyncDialog(self, wx_event):
        NewSyncWizard(self.ctrl, self.event)

    def delete_localbox(self, wx_event):
        map(lambda l: self._main_syncing_thread.stop(l), self.ctrl.delete())


class SharePanel(wx.Panel):
    """
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=MAIN_PANEL_SIZE)

        # Attributes
        self.ctrl = SharesListCtrl(self)
        self.btn_add = wx.Button(self, label=_('Add'), size=(70, 30))
        self.btn_delete = wx.Button(self, label=_('Delete'), size=(70, 30))

        # Layout
        self._DoLayout()

        # Bind events
        self.Bind(wx.EVT_BUTTON, self.create_share, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.delete_share, self.btn_delete)
        self.Bind(wx.EVT_SHOW, self.on_show)

    def _DoLayout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.ctrl, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.btn_add)
        hbox4.Add(self.btn_delete)
        vbox.Add(hbox4, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        vbox.Add((-1, 25))

        self.SetSizer(vbox)

    def create_share(self, wx_event):
        NewShareDialog(self, self.ctrl)

    def delete_share(self, wx_event):
        question = _('This will also delete the directory in your LocalBox and for all users. Continue?')
        if gui_utils.show_confirm_dialog(self, question):
            self.ctrl.delete()

    def on_show(self, wx_event):
        if self.IsShown():
            self.ctrl.populate()


class AccountPanel(wx.Panel):
    """

    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=MAIN_PANEL_SIZE)

        # Attributes
        self.ctrl = AccountController()
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label=_("Hi, User!!!")),
                  1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=DEFAULT_BORDER)

        self.SetSizer(sizer)


class PreferencesPanel(wx.Panel):
    """

    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=MAIN_PANEL_SIZE)

        # Attributes
        self.ctrl = preferences_ctrl
        self.language_choice = wx.Choice(self, choices=LANGUAGES.keys())

        self.language_choice.SetSelection(self.language_choice.FindString(
            self.ctrl.prefs.language if (self.ctrl.prefs.language is not None) else DEFAULT_LANGUAGE))

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label=_("Language")),
                  flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.language_choice, flag=wx.EXPAND | wx.ALL, border=10)

        sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)

        self.language_choice.Bind(wx.EVT_CHOICE, self.OnChoice)

    def OnChoice(self, event):
        language_selected = self.language_choice.GetString(self.language_choice.GetSelection())
        getLogger(__name__).debug(
            "You selected " + language_selected + " from Choice")
        self.ctrl.prefs.language = language_selected


# ----------------------------------- #
# ----       OTHER Panels        ---- #
# ----------------------------------- #
class LoginPanel(wx.Panel):
    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent)

        # Attributes
        self.parent = parent
        self._username = wx.TextCtrl(self)
        self._password = wx.TextCtrl(self, style=wx.TE_PASSWORD)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        input_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer.Add(wx.StaticText(self, label=_("Username:")),
                        0, wx.ALL | wx.ALIGN_LEFT)
        input_sizer.Add(self._username, 0, wx.ALL | wx.EXPAND)
        input_sizer.Add(wx.StaticText(self, label=_("Password:")),
                        0, wx.ALL | wx.ALIGN_LEFT, border=DEFAULT_BORDER)
        input_sizer.Add(self._password, 0, wx.ALL | wx.EXPAND)

        main_sizer.Add(input_sizer, 1, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)

        self.SetSizer(main_sizer)

    def get_username(self):
        return self._username.GetValue()

    def get_password(self):
        return self._password.GetValue()


class FirstLoginPanel(wx.Panel):
    def __init__(self, parent):
        super(FirstLoginPanel, self).__init__(parent)

        # Attributes
        self.parent = parent
        self._ctrl = LoginController()
        self.login_panel = LoginPanel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.welcome_sizer = wx.BoxSizer(wx.VERTICAL)
        self.welcome_sizer.Add(wx.StaticText(self, label=_("WELCOME")), 0, wx.ALL | wx.ALIGN_CENTER)

        self.main_sizer.Add(self.welcome_sizer, 0, wx.ALL | wx.EXPAND)
        self.main_sizer.Add(self.login_panel, 0, wx.ALL | wx.EXPAND)

        self.SetSizer(self.main_sizer)

    @property
    def ctrl(self):
        return self._ctrl


class BottomPanel(wx.Panel):
    """
    Custom Panel containing buttons: "Ok", "Apply" and "Cancel"
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, size=(MAIN_PANEL_SIZE[0], 500))

        # Attributes
        self.parent = parent
        self.btn_ok = wx.Button(self, id=wx.ID_OK, label=_('Ok'))
        self.btn_apply = wx.Button(self, id=wx.ID_APPLY, label=_('Apply'))
        self.btn_close = wx.Button(self, id=wx.ID_CLOSE, label=_('Close'))

        # Layout
        self._DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnClickOk, id=self.btn_ok.Id)
        self.Bind(wx.EVT_BUTTON, self.ApplyOnClick, id=self.btn_apply.Id)
        self.Bind(wx.EVT_BUTTON, self.CloseOnClick, id=self.btn_close.Id)

    def _DoLayout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_szr = wx.StdDialogButtonSizer()

        btn_szr.AddButton(self.btn_ok)
        btn_szr.AddButton(self.btn_apply)
        btn_szr.AddButton(self.btn_close)

        btn_szr.Realize()

        main_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        main_sizer.Add(btn_szr)  # , border=DEFAULT_BORDER)
        self.SetSizer(main_sizer)

    def OnClickOk(self, event):
        getLogger(__name__).debug('OkOnClick')
        self.parent.ctrl.save()
        self.parent.Hide()

    def ApplyOnClick(self, event):
        getLogger(__name__).debug('ApplyOnClick')
        self.parent.ctrl.save()

    def CloseOnClick(self, event):
        getLogger(__name__).debug('CloseOnClick')
        self.parent.Hide()


# ----------------------------------- #
# ----     GUI Controllers       ---- #
# ----------------------------------- #
class LocalboxListCtrl(wx.ListCtrl):
    """
    This class behaves like a bridge between the GUI components and the real syncs controller.
    """

    def __init__(self, parent):
        super(LocalboxListCtrl, self).__init__(parent,
                                               style=wx.LC_REPORT)

        self.ctrl = SyncsController()

        # Add three columns to the list
        self.InsertColumn(0, _("Label"))
        self.InsertColumn(1, _("Path"))
        self.InsertColumn(2, _("URL"))

        self.SetColumnWidth(0, 100)
        self.SetColumnWidth(1, 250)
        self.SetColumnWidth(2, 200)

    def populate_list(self):
        """
        Read the syncs list from the controller
        """
        for item in self.ctrl.load():
            self.Append((item.label, item.path, item.url))

    def add(self, item):
        getLogger(__name__).debug('%s: Add item %s' % (self.__class__.__name__, item))
        self.Append((item.label, item.path, item.url))
        self.ctrl.add(item)

    def delete(self):
        idx = 0
        labels_removed = []
        while idx > -1:
            idx = self.GetNextSelected(-1)

            if idx > -1:
                getLogger(__name__).debug('%s: Delete item #%d' % (self.__class__.__name__, idx))
                self.DeleteItem(idx)
                label = self.ctrl.delete(idx)
                labels_removed.append(label)

        map(lambda l: SharesController().delete_for_label(l), labels_removed)
        self.save()
        return labels_removed

    def save(self):
        getLogger(__name__).info('%s: ctrl save()' % self.__class__.__name__)
        SharesController().save()
        self.ctrl.save()


class LoxListCtrl(wx.ListCtrl):
    """
    This class behaves like a bridge between the GUI components and the real controller.
    """

    def __init__(self, parent, cklass, iklass):
        super(LoxListCtrl, self).__init__(parent,
                                          style=wx.LC_REPORT)

        self.ctrl = cklass()

    def add(self, item):
        getLogger(__name__).debug('%s: Add item %s' % (self.__class__.__name__, item))
        self.Append(self.item_attrs(item).values())
        self.ctrl.add(item)

    def delete(self):
        idx = 0
        removed = []
        while idx > -1:
            idx = self.GetNextSelected(-1)

            if idx > -1:
                getLogger(__name__).debug('%s: Delete item #%d' % (self.__class__.__name__, idx))
                self.DeleteItem(idx)
                label = self.ctrl.delete(idx)
                removed.append(label)

        self.save()
        return removed

    def save(self):
        getLogger(__name__).info('%s: ctrl save()' % self.__class__.__name__)
        self.ctrl.save()

    def populate(self):
        self.DeleteAllItems()


class SharesListCtrl(LoxListCtrl):
    """
    This class behaves like a bridge between the GUI components and the real syncs controller.
    """

    def __init__(self, parent):
        super(SharesListCtrl, self).__init__(parent,
                                             SharesController,
                                             ShareItem)

        self.InsertColumn(0, _("Label"))
        self.InsertColumn(1, _("User"))
        self.InsertColumn(2, _("Path"))
        self.InsertColumn(3, _("URL"))

        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 150)
        self.SetColumnWidth(2, 200)
        self.SetColumnWidth(3, 400)

    def populate(self):
        """
        Read the syncs list from the controller
        """
        super(SharesListCtrl, self).populate()
        map(lambda i: self.Append([i.label, i.user, i.path, i.url]), self.ctrl.load())


# ----------------------------------- #
# ----         Dialogs           ---- #
# ----------------------------------- #
class LoginDialog(wx.Dialog):
    def __init__(self, parent):
        super(LoginDialog, self).__init__(parent=parent)

        # Attributes
        self.panel = LoginPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()


class PasshphrasePanel(wx.Panel):
    def __init__(self, parent, username, label):
        super(PasshphrasePanel, self).__init__(parent=parent)

        self.parent = parent
        self._username = username
        self._label = label
        self._label_template = _('Hi {0}, please provide the passphrase for unlocking {1}')
        label_text = self._label_template.format(username, label)
        self.label = wx.StaticText(self, label=label_text)
        self.label.Wrap(parent.Size[0] - 50)
        self._passphrase = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self._btn_ok = wx.Button(self, id=wx.ID_OK, label=_('Ok'))
        self._btn_close = wx.Button(self, id=wx.ID_CLOSE, label=_('Close'))

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        sizer.Add(self._passphrase, 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)

        btn_szr = wx.StdDialogButtonSizer()

        btn_szr.AddButton(self._btn_ok)
        btn_szr.AddButton(self._btn_close)

        btn_szr.Realize()

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        main_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        main_sizer.Add(btn_szr, border=DEFAULT_BORDER)
        main_sizer.Add(wx.StaticText(self, label=''), 0, wx.ALL | wx.EXPAND)

        # Event Handlers

        self.Bind(wx.EVT_BUTTON, self.OnClickOk, id=self._btn_ok.Id)
        self.Bind(wx.EVT_BUTTON, self.OnClickClose, id=self._btn_close.Id)
        self._passphrase.Bind(wx.EVT_KEY_DOWN, self.OnEnter)

        self.SetSizer(main_sizer)

    def OnClickOk(self, event):
        if event.Id == self._btn_ok.Id:
            try:
                LoginController().store_passphrase(passphrase=self._passphrase.Value,
                                                   user=self._username,
                                                   label=self._label)
                self.parent.Destroy()
            except InvalidPassphraseError:
                gui_utils.show_error_dialog(message=_('Wrong passphase'), title=_('Error'))
            except Exception as err:
                getLogger(__name__).exception(err)
                gui_utils.show_error_dialog(message=_('Could not authenticate. Please contact the administrator'),
                                            title=_('Error'))

    def OnEnter(self, event):
        """"""
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            event.Id = self._btn_ok.Id
            return self.OnClickOk(event)
        event.Skip()

    def OnClickClose(self, event):
        self.parent.OnClickClose(event)


class PassphraseDialog(wx.Dialog):
    def __init__(self, parent, username, label, site):
        super(PassphraseDialog, self).__init__(parent=parent,
                                               title=PASSPHRASE_TITLE,
                                               size=PASSPHRASE_DIALOG_SIZE,
                                               style=wx.CLOSE_BOX | wx.CAPTION)

        # Attributes
        self.panel = PasshphrasePanel(self, username, label)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.passphrase_continue = False

        self.InitUI()

        self.Bind(wx.EVT_CLOSE, self.OnClickClose)

    def InitUI(self):
        self.main_sizer.Add(self.panel)

        self.Layout()
        self.Center()
        self.Show()

    def OnClickClose(self, wx_event):
        self.Destroy()
        import sys
        sys.exit(0)

    @staticmethod
    def show(username, label):
        PassphraseDialog(None, username=username, label=label)


class NewShareDialog(wx.Dialog):
    def __init__(self, parent, ctrl):
        super(NewShareDialog, self).__init__(parent=parent,
                                             title=_('Create Share'),
                                             size=(500, 600),
                                             style=wx.CLOSE_BOX | wx.CAPTION)

        self.ctrl = ctrl
        # Attributes
        self.panel = NewSharePanel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.InitUI()

        self.Bind(wx.EVT_CLOSE, self.OnClickClose)

    def InitUI(self):
        self.main_sizer.Add(self.panel)

        self.Layout()
        self.Center()
        self.Show()

    def OnClickClose(self, wx_event):
        self.Destroy()


class NewSharePanel(wx.Panel):
    def __init__(self, parent):
        super(NewSharePanel, self).__init__(parent=parent)

        self.parent = parent

        self.list = TestListCtrl(self, style=wx.LC_REPORT)
        self._selected_dir = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.btn_select_dir = wx.Button(self, label=_('Select'), size=(95, 30))
        self.btn_select_dir.Disable()
        self.choice = wx.Choice(self, choices=self.get_localboxes())

        self._btn_ok = wx.Button(self, id=wx.ID_OK, label=_('Ok'))
        self._btn_close = wx.Button(self, id=wx.ID_CLOSE, label=_('Close'))

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_sel_dir = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label=_('Select your LocalBox:')), 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        sizer.Add(self.choice, 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        sizer.Add(wx.StaticText(self, label=_('Select directory to share:')), 0, wx.ALL | wx.EXPAND,
                  border=DEFAULT_BORDER)
        sizer_sel_dir.Add(self._selected_dir, 1)
        sizer_sel_dir.Add(self.btn_select_dir, 0)
        sizer.Add(sizer_sel_dir, 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        sizer.Add(wx.StaticText(self, label=_('Choose the users you want to share with:')), 0, wx.ALL | wx.EXPAND,
                  border=DEFAULT_BORDER)
        sizer.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL, border=DEFAULT_BORDER)

        btn_szr = wx.StdDialogButtonSizer()

        btn_szr.AddButton(self._btn_ok)
        btn_szr.AddButton(self._btn_close)

        btn_szr.Realize()

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        main_sizer.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, border=DEFAULT_BORDER)
        main_sizer.Add(btn_szr, border=DEFAULT_BORDER)
        main_sizer.Add(wx.StaticText(self, label=''), 0, wx.ALL | wx.EXPAND)

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.select_dir, self.btn_select_dir)
        self.Bind(wx.EVT_BUTTON, self.OnClickOk, id=self._btn_ok.Id)
        self.Bind(wx.EVT_BUTTON, self.OnClickClose, id=self._btn_close.Id)
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

        self.SetSizer(main_sizer)

    def OnClickOk(self, event):
        path = self._selected_dir.GetValue()
        lox_label = self.choice.GetString(self.choice.GetSelection())
        if gui_utils.is_valid_input(path) and self.list.GetSelectedItemCount() > 0:
            user_list = self.list.get_users()
            share_path = path.replace(self.localbox_path, '', 1)

            if self.localbox_client.create_share(localbox_path=share_path,
                                                 passphrase=LoginController().get_passphrase(
                                                     self.localbox_client.label),
                                                 user_list=user_list):
                item = ShareItem(user=self.localbox_client.username, path=share_path, url=self.localbox_client.url,
                                 label=lox_label)
                SharesController().add(item)
                self.parent.ctrl.populate()
            else:
                gui_utils.show_error_dialog(_('Server error creating the share'), _('Error'))
            self.parent.Destroy()

    def OnClickClose(self, event):
        self.parent.OnClickClose(event)

    def OnChoice(self, event):
        self.btn_select_dir.Enable()
        self.list.populate()

    def get_localboxes(self):
        return map(lambda x: x.label, localbox_ctrl.ctrl.load())

    def select_dir(self, wx_event):
        try:
            path = gui_utils.select_directory(cwd=self.localbox_path)
            if path:
                self.localbox_client.get_meta(path)
                self._selected_dir.SetValue(path)
        except InvalidLocalBoxPathError:
            gui_utils.show_error_dialog(_(
                'Invalid LocalBox path. Please make sure that you are selecting a directory inside LocalBox and '
                'that the directory has been uploaded. Or try a different directory.'), 'Error')

    @property
    def localbox_client(self):
        localbox_item = localbox_ctrl.ctrl.get(self.choice.GetString(self.choice.GetSelection()))
        return LocalBox(url=localbox_item.url, label=localbox_item.label,
                        path=localbox_item.path)

    @property
    def localbox_path(self):
        return localbox_ctrl.ctrl.get(self.localbox_client.label).path


class TestListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(2)

        self.parent = args[0]

        self.InsertColumn(0, "No.")
        self.InsertColumn(1, "Username")

        self.Arrange()

    def OnCheckItem(self, index, flag):
        print(index, flag)

    def GetSelectedItemCount(self):
        count = 0
        for i in range(0, self.GetItemCount()):
            if self.IsChecked(i):
                count += 1

        return count

    def populate(self):
        self.DeleteAllItems()

        localbox_client = self.parent.localbox_client
        self.users = localbox_client.get_all_users()
        tmp_users = []

        for i in range(len(self.users)):
            user = self.users[i]
            if localbox_client.username != user['username']:
                self.Append(["", user['username']])
                tmp_users.append(user)

        self.users = tmp_users

    def get_users(self):
        """
        Get the list of users to send the invite to
        :return:
        """
        result = list()
        for i in range(0, self.GetItemCount()):
            if self.IsChecked(i):
                result.append(self.users[i])

        return result


def ask_passphrase(username, site):
    app = wx.App()
    PassphraseDialog.show(username=username, label=site)
    app.MainLoop()

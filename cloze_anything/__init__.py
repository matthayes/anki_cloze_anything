# Copyright 2019 Matthew Hayes

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re

from aqt import gui_hooks
from anki.consts import MODEL_CLOZE
from anki.hooks import addHook, wrap
from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import tooltip


def get_cloze_nums(content):
    """
    Search content for cloze references and return as a set.

    For example, for the content

        ((c1::I)) ((c2::am)) hungry.

    This would return {1, 2}.
    """
    match = re.findall(r"\(\(c(\d+)::.+?\)\)", content)
    if match:
        cloze_nums = {int(x) for x in match}
    else:
        cloze_nums = set()

    return cloze_nums


def get_set_fields_command(editor, *, field_overrides=None):
    """
    Get data for note fields and create JavaScript command that will set the fields in the UI.

    This is based on editor.loadNote, however it only sets the fields, rather than everything
    else.

    field_overrides can be set to override the current value for a field, thus ignoring whatever
    value is found in the note.  This is needed in some cases because the note data may be stale
    compared to the UI.  The UI has the most up to date field value, which may not yet be persisted
    in the note.
    """

    data = []
    for fld, val in editor.note.items():
        if field_overrides and fld in field_overrides:
            val = field_overrides[fld]
        data.append((fld, editor.mw.col.media.escape_media_filenames(val)))

    return "setFields({});".format(
        json.dumps(data)
    )


def update_cloze_fields(self, *, cloze_nums, cloze_field_name, model) -> int:
    """
    Updates the numeric cloze fields for a particular note based on the content of the cloze field.

    The cloze_field_name is the name of the note that has a cloze string.  For example, suppose there
    is a cloze field named ClozeExpression with content:

        ((c1::I)) ((c2::am)) hungry.

    cloze_nums in this case would be {1, 2}.

    This method would then update fields ClozeExpression1 and ClozeExpression2 with value 1 to generate
    the cloze cards.  If there are any other fields with cloze numbers not in this set, such as ClozeExpression3,
    then these will be set to empty so that no cloze card is generated.

    Arguments:
    - cloze_nums:       The set of cloze numbers present int the cloze field.
    - cloze_field_name: The name of the field with the clozed content.
    - model:            The model for the note.

    Returns: A set of the clozes that were found.  For example, if ((c1::blah)) and ((c2::blah)) were in the string
             then this would return {1, 2}.
    """

    cloze_field_regex = re.compile("^" + re.escape(cloze_field_name) + r"(\d+)$")
    found_cloze_nums = set()
    for f in model["flds"]:
        match = cloze_field_regex.match(f["name"])
        if match:
            cloze_num = int(match.group(1))
            found_cloze_nums.add(cloze_num)
            field_content = "1" if cloze_num in cloze_nums else "<br>"

            if self.note.fields[f["ord"]].strip() in {"1", ""}:
                self.note.fields[f["ord"]] = self.mungeHTML(field_content)

    return found_cloze_nums


def onCloze(editor):
    model = editor.note.model()
    # This should do nothing for the standard cloze note type.
    if not re.search('{{(.*:)*cloze:', model['tmpls'][0]['qfmt']):
        # Check if field is non-empty, in which case it can be clozed.
        if editor.note.fields[editor.currentField]:
            current_field_name = model["flds"][editor.currentField]["name"]
            if current_field_name.endswith("Cloze"):
                content = editor.note.fields[editor.currentField]
                cloze_nums = get_cloze_nums(content)

                # Determine what cloze number the currently highlighted text should get.
                if cloze_nums:
                    next_cloze_num = max(cloze_nums)
                    # Unless we are reusing, then increment to the next greatest cloze number.
                    if not editor.mw.app.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
                        next_cloze_num += 1
                else:
                    next_cloze_num = 1

                wrap_command = "wrap('((c{}::', '))');".format(next_cloze_num)

                cloze_nums.add(next_cloze_num)

                found_cloze_nums = update_cloze_fields(editor, cloze_nums=cloze_nums, cloze_field_name=current_field_name,
                                                       model=model)

                if not editor.addMode:
                    editor._save_current_note()

                missing_cloze_num = cloze_nums - found_cloze_nums

                def callback(arg):
                    editor.saveNow(lambda: None)

                editor.web.evalWithCallback(wrap_command, callback)

                if missing_cloze_num:
                    tooltip("Not enough cloze fields.  Missing: {}".format(", ".join(
                        current_field_name + str(n) for n in sorted(missing_cloze_num))))
            else:
                tooltip("Cannot cloze unless field ends in name Cloze")
        else:
            # If the field is empty, then to be helpful we can check if it ends in Cloze and in that case
            # copy from another field without Cloze.  For example, when ExpressionCloze is the current
            # field and it is empty, we will copy from the Expression field.

            current_field_name = model["flds"][editor.currentField]["name"]
            if current_field_name.endswith("Cloze"):
                other_field_name = current_field_name[:-len("Cloze")]
                other_field_name_ord = next((f["ord"] for f in model["flds"] if f["name"] == other_field_name), None)
                if other_field_name_ord is not None:
                    content = editor.note.fields[other_field_name_ord]
                    editor.web.eval("setFormat('inserthtml', {});".format(json.dumps(content)))
                else:
                    tooltip("Cannot populate empty field {} because other field {} was not found to copy from".format(
                            current_field_name, other_field_name))
            else:
                tooltip("Cannot populate empty field {} because name does not end in Cloze".format(current_field_name))


def onBridgeCmd(*args, **kwargs):
    """
    Wrapper for Anki's onBridgeCmd that ensures that the numeric cloze fields are updated to be consistent
    with the cloze field.
    """

    self = args[0]
    old = kwargs['_old']
    cmd = args[1]

    try:
        # Update the numeric cloze fields to be consisent with the current state of the clozed expression whenever
        # a blur or key event occurs on the clozed expression field.
        # - A "blur" command happens when the field loses focus.
        # - A "key" command happens when the field still has focus but some seconds elapsed since the last key press.
        if self.note and (cmd.startswith("blur:") or cmd.startswith("key:")):
            _, field_idx, nid, content = cmd.split(":", 3)
            field_idx = int(field_idx)
            try:
                nid = int(nid)
            except ValueError:
                nid = None

            # TODO This doesn't work when adding a note because the new note won't have a note ID.  This means that we can't
            # ensure consistency between the clozed expression and numeric cloze fields when blur or key events occur.

            if nid and nid == self.note.id:
                model = self.note.model()
                current_field_name = model["flds"][field_idx]["name"]
                if current_field_name.endswith("Cloze"):
                    cloze_nums = get_cloze_nums(content)

                    update_cloze_fields(self, cloze_nums=cloze_nums, cloze_field_name=current_field_name,
                                        model=model)

                    # Update the numeric cloze fields in the UI by executing a setFields JavaScript command with the note's field values.
                    # This makes the UI consistent with the note field values we just set above.
                    # We need to provide the current content when getting the command to set the field names due to a possible a race condition.
                    # Typing in the field updates the note after a delay.  But losing focus causes a blur event without delay.
                    # If you type in a field and then immediately hit tab to have the field lose focus, the timing of these two events would result
                    # in an inconsistent state.
                    # get_set_fields_command uses the current value of the fields when generating the command.  Due to the field update being delayed,
                    # this data can be out of date.  The blur command has the most current value, so we override with it.
                    # We can only execute this command for blur events, not key events.  The reason is that setting the fields causes the editor
                    # to lose focus, which would be annoying while typing.  We need a way to selectively update fields, but at the moment Anki
                    # only provides a way to update them all together.
                    if cmd.startswith("blur:"):
                        self.web.eval(get_set_fields_command(self, field_overrides={current_field_name: content}))
    except Exception:
        # Suppress any exceptions so we don't break Anki.
        pass

    old(self, cmd)


def auto_cloze(browser):
    """
    Checks for Cloze fields that are empty and fills each from its corresponding source field.  This is useful
    for content where you want the entire field to be a cloze.  It is easier to select many cards and cloze them
    in batch in this way rather than doing it individually.
    """

    nids = browser.selectedNotes()
    if nids:
        update_count = 0
        browser.mw.checkpoint("{} ({} {})".format(
            "Auto-cloze", len(nids),
            "notes" if len(nids) > 1 else "note"))
        browser.model.beginReset()
        for nid in nids:
            note = browser.mw.col.getNote(nid)
            model = note.model()
            for f in model["flds"]:
                field_name = f["name"]
                field_ord = f["ord"]
                # Fields ending with Cloze that are empty can be automatically filled in
                if field_name.endswith("Cloze") and not note.fields[field_ord].strip():
                    other_field_name = field_name[:-len("Cloze")]
                    other_field_name_ord = next((f["ord"] for f in model["flds"] if f["name"] == other_field_name),
                                                None)
                    field_name1_ord = next((f["ord"] for f in model["flds"] if f["name"] == field_name + "1"),
                                           None)
                    # Automatically copy from other field without the Cloze suffix
                    if other_field_name_ord is not None and field_name1_ord is not None and \
                            not note.fields[field_name1_ord].strip():
                        content = note.fields[other_field_name_ord]
                        note.fields[field_ord] = "((c1::" + content + "))"
                        note.fields[field_name1_ord] = "1"
                        note.flush()
                        update_count += 1
        if update_count:
            browser.mw.requireReset()
        tooltip("Updated {} {}".format(update_count, "notes" if update_count != 1 else "note"))
        browser.model.endReset()
    else:
        tooltip("You must select some cards first")


def create_missing(browser):
    """
    Fills in the apropriate cloze-card-generating fields based on cloze deletions present in a Cloze field.
    For example, if ExpressionCloze has content "((c1::Foo)) ((c2::Bar))" then this will ensure ExpressionCloze1
    and ExpressionCloze2 each have the value 1 so that the two cards are generated, but ExpressionCloze3 would
    be made empty.

    This generally should not be necessary as we ensure the fields are updated as the cloze content is changed.
    It would only be needed if cards are edited manually before the plugin is installed.  This action can be used
    to ensure the fields are in sync.
    """

    nids = browser.selectedNotes()
    if nids:
        update_count = 0
        browser.mw.checkpoint("{} ({} {})".format(
            "Create Missing Cloze Cards", len(nids),
            "notes" if len(nids) > 1 else "note"))
        browser.model.beginReset()
        for nid in nids:
            note = browser.mw.col.getNote(nid)
            model = note.model()
            for f in model["flds"]:
                field_name = f["name"]
                field_ord = f["ord"]
                # Fields ending with Cloze that are empty can be automatically filled in
                if field_name.endswith("Cloze"):
                    cloze_nums = get_cloze_nums(note.fields[field_ord])
                    cloze_field_regex = re.compile("^" + re.escape(field_name) + r"(\d+)$")
                    updated = False
                    for f in model["flds"]:
                        match = cloze_field_regex.match(f["name"])
                        if match:
                            cloze_num = int(match.group(1))
                            field_content = "1" if cloze_num in cloze_nums else ""
                            if note.fields[f["ord"]] != field_content:
                                note.fields[f["ord"]] = field_content
                                updated = True
                    if updated:
                        note.flush()
                        update_count += 1
        if update_count:
            browser.mw.requireReset()
        tooltip("Updated {} {}".format(update_count, "notes" if update_count != 1 else "note"))
        browser.model.endReset()
    else:
        tooltip("You must select some cards first")


def setup_menus(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    submenu = menu.addMenu("Cloze Anything")
    action = submenu.addAction("Auto-cloze Full Field")
    action.triggered.connect(
        lambda _: auto_cloze(browser))
    action = submenu.addAction("Create Missing Cards")
    action.triggered.connect(
        lambda _: create_missing(browser))


def setup_editor_buttons(buttons, editor):
    # TODO find a way to hide the button if the note hasn't been set up for Cloze Anything

    def on_activated():
        onCloze(editor)

    shortcut_key_seq ="Ctrl+Shift+W"
    alt_shortcut_key_seq ="Ctrl+Alt+Shift+W"

    new_button = editor.addButton(
        func=onCloze,
        icon="text_cloze",
        cmd="cloze_anything",
        tip=f"Cloze Anything ({shortcut_key_seq})")

    # cloze shortcut
    QShortcut(  # type: ignore
        QKeySequence(shortcut_key_seq),   # type: ignore
        editor.widget,
        activated=on_activated,
    )

    # cloze shortcut, reusing highest cloze number
    QShortcut(  # type: ignore
        QKeySequence(alt_shortcut_key_seq),   # type: ignore
        editor.widget,
        activated=on_activated,
    )

    return buttons + [new_button]

def setup():
    Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridgeCmd, "around")

    addHook("browser.setupMenus", setup_menus)
    addHook("setupEditorButtons", setup_editor_buttons)

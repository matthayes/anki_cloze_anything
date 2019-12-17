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

from anki.hooks import wrap
from aqt.editor import Editor
from aqt.qt import Qt
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


def update_cloze_fields(self, *, cloze_nums, cloze_field_name, model):
    """
    Updates the numeric cloze fields for a particular note based on the content of the cloze field.

    The cloze_field_name is the name of the note that has a cloze string.  For example, suppose there
    is a cloze field named ClozeExpression with content:

        ((c1::I)) ((c2::am)) hungry.

    cloze_nums in this case would be {1, 2}.

    This method would then update fields ClozeExpression1 and ClozeExpression2 with value 1 to generate
    the cloze cards.  If there are any other fields with cloze numbers not in this set, such as ClozeExpression3,
    then these will be set to empty so that no cloze card is generated.

    In addition this also returns the JavaScript commands to update the UI so as to be consistent with the note.

    Arguments:
    - cloze_nums:       The set of cloze numbers present int the cloze field.
    - cloze_field_name: The name of the field with the clozed content.
    - model:            The model for the note.

    Returns: tuple of JavaScript commands to update UI and the cloze numbers found in cloze fields.
    """

    commands = []
    cloze_field_regex = re.compile("^" + re.escape(cloze_field_name) + r"(\d+)$")
    found_cloze_nums = set()
    for f in model["flds"]:
        match = cloze_field_regex.match(f["name"])
        if match:
            cloze_num = int(match.group(1))
            found_cloze_nums.add(cloze_num)
            field_content = "1" if cloze_num in cloze_nums else "<br>"

            # The note and the UI both need to be updated so they are consistent with one another.  We check
            # that the content is either empty or "1" to avoid accidentally overwriting something unintended,
            # as an extra safety precaution.
            if self.note.fields[f["ord"]].strip() in {"1", ""}:
                self.note.fields[f["ord"]] = self.mungeHTML(field_content)
                commands.append("""$("#f" + %d).html(%s)""" % (f["ord"], json.dumps(field_content)))

    return (commands, found_cloze_nums)


def onCloze(self, _old):
    model = self.note.model()
    # If the model is set up for cloze deletion, then defer to Anki's implementation.
    if re.search('{{(.*:)*cloze:', model['tmpls'][0]['qfmt']):
        return _old(self)
    else:
        # Check if field is non-empty, in which case it can be clozed.
        if self.note.fields[self.currentField]:
            current_field_name = model["flds"][self.currentField]["name"]
            if current_field_name.endswith("Cloze"):
                content = self.note.fields[self.currentField]
                cloze_nums = get_cloze_nums(content)

                # Determine what cloze number the currently highlighted text should get.
                if cloze_nums:
                    next_cloze_num = max(cloze_nums)
                    # Unless we are reusing, then increment to the next greatest cloze number.
                    if not self.mw.app.keyboardModifiers() & Qt.AltModifier:
                        next_cloze_num += 1
                else:
                    next_cloze_num = 1

                commands = [
                    "wrap('((c{}::', '))')".format(next_cloze_num)
                ]

                cloze_nums.add(next_cloze_num)

                cloze_field_update_commands, found_cloze_nums = \
                    update_cloze_fields(self, cloze_nums=cloze_nums, cloze_field_name=current_field_name, model=model)

                commands.extend(cloze_field_update_commands)

                missing_cloze_num = cloze_nums - found_cloze_nums

                self.web.eval(";".join(commands) + ";")

                if missing_cloze_num:
                    tooltip("Not enough cloze fields.  Missing: {}".format(", ".join(
                        current_field_name + str(n) for n in sorted(missing_cloze_num))))
            else:
                tooltip("Cannot cloze unless field ends in name Cloze")
        else:
            # If the field is empty, then to be helpful we can check if it ends in Cloze and in that case
            # copy from another field without Cloze.  For example, when ExpressionCloze is the current
            # field and it is empty, we will copy from the Expression field.

            current_field_name = model["flds"][self.currentField]["name"]
            if current_field_name.endswith("Cloze"):
                other_field_name = current_field_name[:-len("Cloze")]
                other_field_name_ord = next((f["ord"] for f in model["flds"] if f["name"] == other_field_name), None)
                if other_field_name_ord is not None:
                    content = self.note.fields[other_field_name_ord]
                    self.web.eval("setFormat('inserthtml', {});".format(json.dumps(content)))
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
        if self.note and (cmd.startswith("blur:") or cmd.startswith("key:")):
            _, field_idx, nid, content = cmd.split(":", 3)
            field_idx = int(field_idx)
            try:
                nid = int(nid)
            except ValueError:
                nid = None

            if nid and nid == self.note.id:
                model = self.note.model()
                current_field_name = model["flds"][field_idx]["name"]
                if current_field_name.endswith("Cloze"):
                    cloze_nums = get_cloze_nums(content)
                    commands, _ = \
                        update_cloze_fields(self, cloze_nums=cloze_nums, cloze_field_name=current_field_name,
                                            model=model)
                    self.web.eval(";".join(commands) + ";")
    except Exception:
        # Suppress any exceptions so we don't break Anki.
        pass

    old(self, cmd)


def setup():
    # Note: cannot wrap onCloze because it is referenced within Anki by _links before the wrap here
    # takes effect, so the wrap won't work.
    Editor._onCloze = wrap(Editor._onCloze, onCloze, "around")
    Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridgeCmd, "around")

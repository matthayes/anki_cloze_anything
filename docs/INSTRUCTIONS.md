# Instructions

This guide walks you through how to setup the fields and card templates for the Cloze Anything approach.  Alternatively you can download one of the shared decks, for which I've already done this for you.

First, decide on the name for your field that will hold your cloze content.  If you would like to use the plugin at some point to help you edit your notes then the name should end in *Cloze*, out of convention.  Otherwise there is no requirement for the field name.  For the remainder I'll assume you're using `ExpressionCloze` as the field name.  Create this field.

**Note:** You can have more than one field with cloze content per note.  For example, you could have fields `Example1Cloze` and `Example2Cloze`.  Each can be used to generate cards.

Next, create the fields that are used to enable each of the cloze deletion cards.  You need as many fields as the number of cloze deletions you want to support.  For example, for the cloze content `((c1::Ik)) ((c2::heb)) ((c3::honger)).` there are three cloze deletions.  If three is the maximum number of deletions you want to support then out of convention you should create fields `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3`. These fields are used to generate cloze cards via Anki's [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  The only requirement is that the number the field ends with corresponds to the number in the cloze content.  That is, for `ExpressionCloze1`, the number `1` corresponds to `c1` in the cloze content.  However out of convention the plugin will expect the names of these fields to be based on the name of the field containing the cloze content.

Create a card type named `ExpressionCloze1` (the same name as the first cloze deletion field).  For the Front Template enter the following content.  This assumes you also have a field named `Meaning`.  You can of course edit this template as needed to include your own fields.

```
{{#ExpressionCloze}}
{{#ExpressionCloze1}}
<div id="cloze" data-card="{{Card}}" data-cloze-show-before="all" data-cloze-show-after="all">
{{ExpressionCloze}}
</div>

{{Meaning}}

<script>
/*
Copyright 2019 Matthew Hayes

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

function wrap_span(content, classes) {
  return "<span class=\"" + classes + "\">" + content + "</span>";
}

var expEl = document.getElementById("cloze");
var card = expEl.getAttribute("data-card");

var showBeforeValue = expEl.getAttribute("data-cloze-show-before") || "all";
var showAfterValue = expEl.getAttribute("data-cloze-show-after") || "all";

var cardMatch = card.match(/[^\d]+(\d+)$/);
var isBack = !!document.getElementById("back");
if (cardMatch) {
  var currentClozeNum = parseInt(cardMatch[1]);
  var expContent = expEl.innerHTML;
  expEl.innerHTML = expContent.replace(/\(\(c(\d+)::([^)]+)\)\)/g,function(match, clozeNum, content) {
    var contentSplit = content.split(/::/)
    var contentHint = null;
    clozeNum = parseInt(clozeNum);
    if (contentSplit.length == 2) {
      contentHint = contentSplit[1];
      content = contentSplit[0]
    }
    var contentReplacement = contentHint ? "[" + contentHint + "]" : "[...]";
    var result = null;
    if (isBack) {
      result = content;
    }
    else {
      if (clozeNum == currentClozeNum) {
        result = wrap_span(contentReplacement, "current-cloze");
      }
      else if (clozeNum < currentClozeNum) {
        if (showBeforeValue == "all") {
          result = content;
        }
        else if (showBeforeValue.match(/^\d+$/)) {
          var showBeforeNum = parseInt(showBeforeValue);
          if (currentClozeNum - clozeNum <= showBeforeNum) {
            result = content;
          }
          else {
            result = wrap_span(contentReplacement, "other-cloze");
          }
        }
        else {
          result = wrap_span(contentReplacement, "other-cloze");
        }
      }
      else if (clozeNum > currentClozeNum) {
        if (showAfterValue == "all") {
          result = content;
        }
        else if (showAfterValue.match(/^\d+$/)) {
          var showAfterNum = parseInt(showAfterValue);
          if (clozeNum - currentClozeNum <= showAfterNum) {
            result = content;
          }
          else {
            result = wrap_span(contentReplacement, "other-cloze");
          }
        }
        else {
          result = wrap_span(contentReplacement, "other-cloze");
        }
      }
      else {
        result = content;
      }
    }

    return result;
  });
}
</script>

{{/ExpressionCloze1}}
{{/ExpressionCloze}}
```

For the Back Template:

```
<div id="back">
{{FrontSide}}
</div>
```

For the styling, add the additonal content to whatever is already present:

```
.current-cloze {
  color: blue;
}

.other-cloze {
  color: grey;
}
```

Now repeat this for the remaining cloze fields.  That is, if you have field `ExpressionCloze2`, then create a card template named `ExpressionCloze2` with the same content as `ExpressionCloze1` except with `{{#ExpressionCloze1}}` replaced with `{{#ExpressionCloze2}}` and `{{//ExpressionCloze1}}` replaced with `{{//ExpressionCloze2}}`.  Do the same for `ExpressionCloze3`, and so on.

At this point you're done.

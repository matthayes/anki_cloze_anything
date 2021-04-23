# Instructions

This guide walks you through how to setup the fields and card templates for the Cloze Anything approach.  Alternatively you can download one of the shared decks, for which I've already done this for you.

First, decide on the name for your field that will hold your cloze content.  If you would like to use the plugin at some point to help you edit your notes then the name should end in *Cloze*, out of convention.  Otherwise there is no requirement for the field name.  For the remainder I'll assume you're using `ExpressionCloze` as the field name.  Create this field.

**Note:** You can have more than one field with cloze content per note.  For example, you could have fields `Example1Cloze` and `Example2Cloze`.  Each can be used to generate cards.

Next, create the fields that are used to enable each of the cloze deletion cards.  You need as many fields as the number of cloze deletions you want to support.  For example, for the cloze content `((c1::Ik)) ((c2::heb)) ((c3::honger)).` there are three cloze deletions.  If three is the maximum number of deletions you want to support then out of convention you should create fields `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3`. These fields are used to generate cloze cards via Anki's [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  The only requirement is that the number the field ends with corresponds to the number in the cloze content.  That is, for `ExpressionCloze1`, the number `1` corresponds to `c1` in the cloze content.  However out of convention the plugin will expect the names of these fields to be based on the name of the field containing the cloze content.

Copy the contents of [cloze_anything.js](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/examples/cloze_anything.js) to a file named `_cloze_anything_0.3.js` (or use whatever the current version is).  Then copy this file to the `collections.media` folder for your user.  You can find information about how to locate this path [here](https://docs.ankiweb.net/#/files?id=file-locations).  The underscore prefix is important, as this prevents Anki from deleting the script when checking for unused media, as documented [here](https://docs.ankiweb.net/#/templates/styling?id=installing-fonts).

**Note:** The version is included in the file name for a couple reasons: 1) It enables multiple versions of the script to be used by different note types, and 2) It ensures that if you update to a newer version of the script that your cards will use that newer version.  Changing an existing file in `collections.media` may not result in that change being synced.

Create a card type named `ExpressionCloze1` (the same name as the first cloze deletion field).  For the Front Template enter the following content.  This assumes you also have a field named `Meaning`.  You can of course edit this template as needed to include your own fields.

```
{{#ExpressionCloze}}
{{#ExpressionCloze1}}

<script defer src="_cloze_anything_0.3.js"></script>

<div class="clozed-content">
<div id="cloze" data-card="{{Card}}">
{{ExpressionCloze}}
</div>

{{Meaning}}
</div>

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
  font-weight: bold;
}

.other-cloze {
  color: grey;
}

#cloze {
  visibility: hidden;
}

#cloze.show {
  visibility: visible;
}
```

The `clozed-content` div is initially not displayed to give the JavaScript a chance to run and render the content.

Now repeat this for the remaining cloze fields.  That is, if you have field `ExpressionCloze2`, then create a card template named `ExpressionCloze2` with the same content as `ExpressionCloze1` except with `{{#ExpressionCloze1}}` replaced with `{{#ExpressionCloze2}}` and `{{//ExpressionCloze1}}` replaced with `{{//ExpressionCloze2}}`.  Do the same for `ExpressionCloze3`, and so on.

At this point you're done.

Please refer to the top-level README for configuration options.

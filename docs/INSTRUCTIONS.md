# Instructions

This guide walks you through how to set up the fields and card templates for the Cloze Anything approach.  Alternatively you can download [the shared deck](https://ankiweb.net/shared/info/1637056056) as a starting point, which was set up using these instructions.

**Note:** These instructions guide you through creating very basic front and back card templates that leverage the Cloze Anything system.  The JavaScript library does not impose many requirements on how you set up these templates.  You actually have a lot of freedom in how you customize them.  The key requirements of the JavaScript library will be called out as we go.

First, decide on the name for your field that will hold your cloze content.  If you would like to use the plugin to help you edit your notes (strongly recommended) then the name should end in *Cloze*.  If you don't care to use the plugin then there is no requirement for the field name (you can always rename later if you want).  For the remainder I'll assume you're using `ExpressionCloze` as the field name.  Create this field.

**Note:** You can have more than one field with cloze content per note.  For example, you could have fields `Example1Cloze` and `Example2Cloze`.  Each can be used to generate cards.

Next, create the fields that will be used to enable each of the cloze deletion cards through [Selective Card Generation](https://docs.ankiweb.net/#/templates/generation?id=selective-card-generation).  You need as many fields as the number of cloze deletions you want to support.  For example, for the cloze content `((c1::Ik)) ((c2::heb)) ((c3::honger)).` there are three cloze deletions.  If three is the maximum number of deletions you want to support then you should create fields `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3`. These fields are used to generate cloze cards via Anki's [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  The only requirement is that the number the field ends with corresponds to the number in the cloze content.  That is, for `ExpressionCloze1`, the number `1` corresponds to `c1` in the cloze content.  However out of convention the plugin will expect the names of these fields to be based on the name of the field containing the cloze content.

Download the JavaScript file from the most recent release in the [releases page](https://github.com/matthayes/anki_cloze_anything/releases).  The JavaScript files have the file name format `_cloze_anything_x.y.js` (where `x.y` is a version like `0.3`).  Copy this file to the `collections.media` folder for your user.  You can find information about how to locate this path [here](https://docs.ankiweb.net/#/files?id=file-locations).  The underscore prefix is important, as this prevents Anki from deleting the script when checking for unused media, as documented [here](https://docs.ankiweb.net/#/templates/styling?id=installing-fonts).

**Note:** The version is included in the file name for a couple reasons: 1) It enables multiple versions of the script to be used by different note types, and 2) It ensures that if you update to a newer version of the script that your cards will use that newer version.  Changing an existing file in `collections.media` may not result in that change being synced.

Create a card type named `ExpressionCloze1` (the same name as the first cloze deletion field).  For the Front Template enter the following content, but be sure to replace `x.y` with the version of the JavaScript file.  This assumes you also have a field named `Meaning`.  You can of course edit this template as needed to include your own fields and change the content as needed.

```
{{#ExpressionCloze}}
{{#ExpressionCloze1}}

<script defer src="_cloze_anything_x.y.js"></script>

<div id="cloze" data-card="{{Card}}">
{{ExpressionCloze}}
</div>

{{Meaning}}

{{/ExpressionCloze1}}
{{/ExpressionCloze}}
```

For the Back Template you can simply do the following, which will wrap the front-side content with a div having id `back`:

```
<div id="back">
{{FrontSide}}
</div>
```

Note for the Back Template you could alternatively make a copy of the Front Template, rather than referencing it through `{{FrontSide}}`, and then customize the Back Template to be totally different:

```
{{#ExpressionCloze}}
{{#ExpressionCloze1}}
<div id="back">
<script defer src="_cloze_anything_x.y.js"></script>

<div id="cloze" data-card="{{Card}}">
{{ExpressionCloze}}
</div>

{{Meaning}}
</div>
{{/ExpressionCloze1}}
{{/ExpressionCloze}}
```

Now is a good point to call out some requirements of the JavaScript library and how they manifest here.

1. There must be an element with `id="cloze"`, which contains the cloze content to be processed, like `{{ExpressionCloze}}` above.
2. The back template must have an element with `id="back"` somewhere in the document, in order to identify this as the back card, and the front template must not.
3. The `id="cloze"` element must have an attribute `data-card` with value that ends in a numeric value representing which cloze this is.  Typically you'd use `data-card="{{Card}}"` and name your card templates something like `ExpressionCloze1`, `ExpressionCloze2`, etc. which would be interpreted as being cloze number `1`, `2`, etc. corresponding to `c1`, `c2`, etc.

If the above requirements are met, then the content of the `id="cloze"` element will be replaced by the JavaScript library with either the front- or back-side version of the cloze-rendered content.

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

With the CSS rules above, the `cloze` div is initially not displayed in order to give the JavaScript time to render the content.  The JavaScript library adds the `show` class after it is done rendering.  This avoids temporarily flasshing the non-rendered cloze content before the JavaScript has a chance to run.

Now repeat this for the remaining cloze fields.  That is, if you have field `ExpressionCloze2`, then create a card template named `ExpressionCloze2` with the same content as `ExpressionCloze1` except with `{{#ExpressionCloze1}}` replaced with `{{#ExpressionCloze2}}` and `{{//ExpressionCloze1}}` replaced with `{{//ExpressionCloze2}}`.  Do the same for `ExpressionCloze3`, and so on.

At this point you're done.

Please refer to the top-level README for configuration options.

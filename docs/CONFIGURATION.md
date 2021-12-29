# Configuration

The template has several settings for controlling how the cloze deletions are rendered.  All settings are added to the `div` as shown below for `data-cloze-show-before`.

```
<div id="cloze" data-card="{{Card}}" data-cloze-show-before="all">
{{ExpressionCloze}}
</div>
```

## data-cloze-replace-char

This controls what character to replace clozed values with.  The default is a period, `.`, which is the same as Anki.  If instead you would like to use underscores:

```
data-cloze-replace-char="_"
```

## data-cloze-replace-same-length

This is a `true` or `false` value that controls whether clozed values should be replaced with a fixed 3-character replacement or with an equal number of replacement characters as exist in the content.  The default is `false`, which is the same as Anki's cloze behavior.

If set to `true`, then `((c1::abcd))` would be replaced with `[....]`.

Note that setting this to true will cause it to preserve spaces.  So then `((c1::abc def))` would become `___ ___`.  That is, only the non-space characters are replaced.

## data-cloze-always-show-blanks

This is a `true` or `false` value that controls whether blanks should be shown even if there is a hint.  The default is `false`, which is the same behavior as Anki.  That is, `((c1::abc))` would become `[...]`, but `((c1::abc::hint))` would become `[hint]`.  When set to `true`, then the latter becomes `[...|hint]`.

This setting tends to be more useful when used with `data-cloze-replace-same-length`, `data-cloze-replace-char`, and the formatting settings below.

## data-cloze-blanks-format, data-cloze-hint-format, and data-cloze-blanks-and-hint-format

These control the cloze format for three different scenarios:

* `data-cloze-blanks-format`: Format used when only blanks are displayed.  The default format is `[{blanks}]`.
* `data-cloze-hint-format`: Format used when only the hint is displayed.  The default format is `[{hint}]`.
* `data-cloze-blanks-and-hint-format`: Format used when blanks and the hint are displayed.  The default format is `[{blanks}|{hint}]`.

Suppose you want more of a fill in the blanks style for your cloze cards.  But, you still want to display the hints if available.

```
data-cloze-always-show-blanks="true" data-cloze-blanks-format="{blanks}" data-cloze-hint-format="[{hint}]" data-cloze-blanks-and-hint-format="{blanks} [{hint}]" data-cloze-replace-char="_"
```

This would result in the following transformatings:

* `((c1::abc))` => `___`
* `((c1::abc:hint))` => `___ [hint]`

## data-cloze-show-before and data-cloze-show-after

The `data-cloze-show-before` and `data-cloze-show-after` settings can be added to the template as shown in the snippet below.  These control whether other clozed values before and after the current cloze are shown.

```
data-cloze-show-before="all" data-cloze-show-after="all"
```

In the snippet above, both of these have the value `all`, which is the default.  This means that all cloze deletions before and after the current cloze will be displayed.  For example, suppose that the content is:

```
((c1::Ik)) ((c2::heb)) ((c3::honger)).
I am hungry.
```

The second card, corresponding to `c2`, would be rendered as below.

![Ik ... honger](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/images/ik_heb_honger.png)

Aside from the value `all`, other possible values for these settings are:

* `none`, which causes none of the cloze deletions to be displayed before/after.
* A numeric value greater than 0.  For example, if you set this to 1 for both settings, then the first cloze deletions before and after the current cloze will be shown, but no others.

For example, suppose that you have set `data-cloze-show-before="1"` and `data-cloze-show-after="1"`.  You create a card with the following cloze content:

```
((c1::To be, or not to be, that is the question:))
((c2::Whether 'tis nobler in the mind to suffer))
((c3::The slings and arrows of outrageous fortune,))
((c4::Or to take Arms against a Sea of troubles,))
((c5::And by opposing end them: to die, to sleep;))
```

The third card, corresponding to `c3`, would be rendered like this:

![hamlet](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/images/hamlet.png)

Notice that the current cloze is highlighted in blue and the others are grey.  This is controlled by the CSS provided in the instructions.

Alternatively, for `data-cloze-show-before="all"` and `data-cloze-show-after="none"` the third card would be rendered as:

![hamlet2](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/images/hamlet2.png)

## data-cloze-keep-regex

This contains a regular expression that determines what parts of the text should not be replaced with blanks, as if they were surrounded with backticks.  By default it contains basic Latin-script punctuation marks, which most users would want to show in the cloze.  A more comprehensive set of punctuation marks from different scripts can be set by using:

```
data-cloze-keep-regex="[!()+,./:;?{}¡«»¿׃‒–—‘’‚“”„‥…‧‹›♪⟨⟩ ⸮、。〈〉《》「」『』【】〝〟〽﹁﹂！（），：；？［］｛｝～\[\]]"
```

Thanks to the fact that this field is a regular expression, you can use it for all kinds for special scenarios.  For example, if you want to show the text from the beginning of the clause until the first colon, in addition to basic Latin-script punctuation, but hide everything else you can use:

```
data-cloze-keep-regex="^.*?:|[!,.:;?—–]"
```

This option has an effect only if `data-cloze-replace-same-length` is set.

# Overriding Configuration

If you'd like to override any default configuration values for certain cards, one way to achieve this is
to add a field to hold configuration:

```
<div id="cloze" data-card="{{Card}}" {{ExpressionClozeConfig}}>
{{ExpressionCloze}}
</div>
```

Then for `ExpressionClozeConfig` you could fill in this for a card:

```
data-cloze-show-before="all"
```
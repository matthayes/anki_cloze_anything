# Anki Cloze Anything

[![Build Status](https://travis-ci.org/matthayes/anki_cloze_anything.svg?branch=master)](https://travis-ci.org/matthayes/anki_cloze_anything)
[![Release](https://img.shields.io/badge/release-v0.2-brightgreen.svg)](https://github.com/matthayes/anki_cloze_anything/releases/tag/v0.1)

This project provides a template-based cloze implementation that:

* is completely independent from Anki's [Cloze Deletion](https://apps.ankiweb.net/docs/manual.html#cloze-deletion),
* does not require any modifications to Anki (via a plugin) for it to work,
* and provides more flexibility in cloze card generation

This is achieved purely through JavaScript in the card template and a novel application of Anki's built-in (awesome) [Selective Card Generation](https://docs.ankiweb.net/templates/generation.html#selective-card-generation) feature.  The big benefit of this is that you can generate cloze cards from existing notes, for which you may already have cards.  It has no dependency on Anki's Cloze note type nor any other note types, which means you don't have to migrate your cards to a new note type.  It is compatible with Anki Desktop, AnkiMobile, and AnkiDroid.

Getting started is easy.  You can either download the [shared deck](https://ankiweb.net/shared/info/1637056056) or follow the [instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) for setting up the templates manually.

## Features

Replicating Anki functionality with JavaScript and card templates is not the goal however.  The goal is endless flexibility.  You can add cloze cards to any existing note type ("cloze anything") simply by adding new fields and card templates based on the instructions found here.  You can also modify the templates completely, using them simply as a guide.

With the default settings this replicates Anki's cloze functionality.  However the template is highly configurable and lets you do things you can't otherwise easily do.  Below is a summary of some useful features of the templates and this approach.

* **Control the visibility of other cloze deletions**.  Normally Anki will show the other cloze deletions besides the one currently being tested for a particular card.  The approach here lets you customize this, similar to the functionality provided by [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).
* **Customize the cloze format**.  Anki replaces each clozed value with either `[...]` or `[hint]` in the case of a hint.  The templates let you customize this.  For example, you could use underscores and have the format be `___`.  Or you could always include the hint, as in `___ [hint]`.  Also instead of a fixed number of 3 characters you could have each non-space character replaced.  So you could have `((c1::ab cdef::hint))` become `__ ____ [hint]`.
* **Selectively reveal characters as a hint**.  Sometimes due to ambiguity you may need a hint at what a word starts with.  The template has a simple syntax to support this.  Simply surround the characters you want to keep with backticks.  For example, ``((c1::`a`bc `d`ef))`` could be rendered as `a__ d__`.  You can selectively reveal any part of the content, not just at the beginning.  Note that you could also do ``a((c1::bc)) d((c1::ef))``, however the backtick syntax may be more convenient.
* **Add cloze deletion to an existing note**.  Suppose you already have a note with fields *Expression* and *Meaning* and a card that tests you on Expression -> Meaning.  Now suppose you want a version of *Expression* with cloze deletions.  Normally with Anki you'd have to copy the text to a completely separate note based on the *Cloze* note type.  This is a big headache to manage.  Instead with the Cloze Anything approach you copy the text to an *ExpressionCloze* field in the same note.  This makes it much easier to manage the content.  You can easily find notes that don't have a cloze through a simple search in the browser.
* **Add multiple cloze deletion fields to an existing note**.  Suppose that you have a note type that tests you on vocabulary with fields *VocabItem* and *Meaning*.  Suppose that you have added some example fields *ExampleA* and *ExampleB* to provide examples of how the vocabulary item is used.  With the Cloze Anything approach you can create cloze versions for each of these examples as *ExampleACloze* and *ExampleBCloze* and render cards from each of them.

An optional [plugin](https://ankiweb.net/shared/info/330680661) is also provided that automates some of the otherwise (minimal) manual work that would be required when following this approach.

## Getting Started

There are two options for getting started:

1. Download the [shared deck](https://ankiweb.net/shared/info/1637056056) I've already prepared for you and use the note type (and card templates) as the basis for your cards.
2. Follow my [detailed instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) on how to set up the fields and card templates.  This is the best choice when you want to add cloze to an existing note type.

Installing the [plugin](https://ankiweb.net/shared/info/330680661) is also recommended to make it easier for you to edit the cloze cards, but it isn't required.

## How the Template Works

Similar to Anki's [Cloze Templates](https://apps.ankiweb.net/docs/manual.html#cloze-templates), you need a field to contain the cloze content.  Out of convention it's a good idea to have the field name end in *Cloze* in case you want to use the plugin later.  Suppose you name it `ExpressionCloze`, as suggested in the instructions.  Cloze content is entered in this field in a similar way as with Anki's Cloze Templates.  The only difference is that instead of the format `{{c1::text}}` you use `((c1::text))`.  You then need fields to enable each of the cloze cards.  So, suppose you want to support three clozes.  You would add fields `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3`.  You enter any text you want into these fields to enable the corresponding cloze card.  Out of convention the plugin uses `1`.

For example, suppose you want to create cloze cards for each of the words in the expression *Ik heb honger*.  You would write the fields like so:

![Ik heb honger fields](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/images/ik_heb_honger_fields.png)

For an HTML rendering of this example, see [front](https://htmlpreview.github.io/?https://github.com/matthayes/anki_cloze_anything/blob/master/examples/front.html) and [back](https://htmlpreview.github.io/?https://github.com/matthayes/anki_cloze_anything/blob/master/examples/back.html) card examples.

Because each of the cloze fields has a non-empty value of `1`, a card will be generated for each of `c1` through `c3`.  If you deleted the `1` from `ExpressionCloze3` then a card will be generated for `c1` and `c2` only.

Let's dig into how this all works.  The [instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) referenced earlier have the following template for the first cloze card.  Notice that the entire content of the front of the card is surrounded by conditional tags based on `ExpressionCloze` and `ExpressionCloze1`.  This means that both fields must be non-empty for the card to be created, due to the way Anki card generation works.  So if either of these fields is empty, the corresponding card isn't generated.  The ommitted script simply looks at the number the value for `data-card` ends with and then updates the content within the cloze `<div>` accordingly.  So if the value of `data-card` is `ExpressionCloze2` then it knows to hide the `((c2::text))` and show the others.

```
{{#ExpressionCloze}}
{{#ExpressionCloze1}}
<div id="cloze" data-card="{{Card}}" data-cloze-show-before="all" data-cloze-show-after="all">
{{ExpressionCloze}}
</div>

{{Meaning}}

<script>
// .. ommitted ...
</script>

{{/ExpressionCloze1}}
{{/ExpressionCloze}}
```

The templates also support hints in the cloze deletions, as in Anki's system.  For example, for the example below, `heb` would be replaced with `[verb]` instead of `[...]`.

```
((c1::Ik)) ((c2::heb::verb)) ((c3::honger)).
```

For the full details on how to set up your card templates manually, see the [instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md).
Alternatively, you can use the [shared deck](https://ankiweb.net/shared/info/1637056056) as a starting point and use the instructions as reference in how to modify it to meet your needs.

### Configuration

The template has several settings for controlling how the cloze deletions are rendered.  See [Configuration](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/CONFIGURATION.md) for details.

## How the Plugin Works

The plugin does two things to make it easier for you to edit cloze deletions when following this approach:

* Hooks into Anki's `[...]` button in the editor so that you can use it on other notes besides those based on Anki's Cloze type.
* Synchronizes edits from the `ExpressionCloze` field (or similarly named field) to the other fields `ExpressionCloze1`, `ExpressionCloze2`, etc. that enable the corresponding cloze cards.

The `[...]` button behaves the same when used on one of the note types based on Anki's Cloze type.  Otherwise however, if the field name ends in *Cloze*, like `ExpressionCloze`, then it will wrap the selected text, such as in `((c1::text))`.  This is the same as Anki's normal behavior with clozes except it uses parentheses instead of curly braces.

The `[...]` button has an additonal useful feature where if you press it while an empty field ending in *Cloze* has focus, it will copy the text from another field with the same name minus the *Cloze* suffix.  For example, if you click the button while focusing on `ExpressionCloze` then it will copy the text from `Expression`.

You can also modify the cloze field without using the `[...]` button.  The plugin monitors changes and identifies patterns like `((c1::text))`.  It makes the corresponding cloze fields to be either empty or contain `1` depending on the presence of cloze deletions.  For example, if you fill in `ExpressionCloze` with `((c1::Ik)) ((c2::heb)) ((c3::honger)).` then it will fill in `1` for each of `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3`.  If you edit it to become `((c1::Ik)) ((c2::heb)) honger.` then it will make `ExpressionCloze3` empty.

### Menu Actions

The plugin adds two actions in the browser under Edit -> Cloze Anything.  Both of them operate on whatever notes
are selected in the browser.

#### Auto-cloze Full Field

This automatically makes a cloze from an entire field.  For example, suppose you have a field named `ExpressionCloze` and `Expression`.  If `ExpressionCloze` is empty, then this action causes the content of `Expression` to be copied to `ExpressionCloze` and made into a cloze like `((c1::content))`.  It also updates `ExpressionCloze1` to cause the cloze card to be generated.  This is useful when you have a lot of notes with short content where you want to cloze the entire content.  It's much more efficient to cloze these in bulk than one by one.

Note that this essentially is using cloze to make a Production card (i.e. given the meaning in your native language, produce the expression in the language you are learning).  So why not just make a Production card template instead of using cloze?  In some cases this may be more effective than using cloze.  However there are a couple reasons why cloze could be useful:

* Your notes may be a mixture of simple expressions where you want to have a single cloze for the entire content and more complex expressions where you want two or more clozes.  With this action you can pick the simple expressions in the browser and cloze them in bulk.
* Your notes may overall be simple expressions.  But you may find that for some notes upon review they are more complex than you thought.  Instead of one cloze you may want to change it to two or more.  By using cloze you have the flexibility to change your mind in the future without having to migrate to a different note type.

#### Create Missing Cards

This basically just makes sure the Cloze field is in sync with the corresponding fields responsible for card generation.  For example, if `ExpressionCloze` has `((c1::Ik)) ((c2::heb)) ((c3::honger)).` then this would ensure `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3` are each filled in with a `1`.  But `ExpressionCloze4` would be made blank, if it exists.  This action isn't generally necessary to use while using the plugin because the plugin ensures that these fields are updated as you change content.  But if you do an import or if you edit notes before using the plugin, this can be used to fix up the fields to be in sync.

## Pros and Cons

Anki already has built-in support for Cloze.  So why use Cloze Anything?

Pros:

* Cloze cards can be added to existing note types without any modifications other than adding new fields and card templates.
* Compared to Anki's built-in Cloze type, you have more flexibility in how the cloze cards are rendered.  You can choose how many of the other cloze values to show, instead of always showing them all.  This functionality is similar to that provided by [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).
* Relies on JavaScript and built-in Anki features such as [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  As cloze functionality is implemented in the templates no modifications to Anki via a plugin are required for it to work.  This greatly reduces the chance that future Anki updates will break this approach.
* No external JavaScript required.  All necessary JavaScript exists in the templates.

Cons:

* Relies on JavaScript, which works because Anki cards are treated like webpages. However, the Anki author notes that [Javascript functionality is provided without any support or warranty](https://apps.ankiweb.net/docs/manual.html#javascript).  So there is a very small chance that a future Anki update could impact card rendering and require changes in the template, which would be promptly carried out by me given my dependence on this approach working.
* Because cloze functionality is implemented in templates, rather than Anki, the same template effectively needs to be copied to each card template.  Also if you make an edit to one of the cloze templates you need to copy the contents to the others as well.
* Adding the `type:` prefix to enable type in the answer is not supported.

## Compatibility

### Anki Versions

The card templates are compatible with Anki Desktop, AnkiMobile, and AnkiDroid.

The plugin works with Anki Desktop 2.1.  I have no plans to add 2.0 support.

### Other Plugins

I have not yet tested interactions of the plugin with other cloze plugins such as [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).  If you encounter a problem please file an issue and I will do my best to fix it.

The following plugins have been reported as having compatibility issues with this plugin:

* [Customize Keyboard Shortcuts](https://ankiweb.net/shared/info/24411424) (Ctrl+Shift+C may not work correctly)
* [Resize images in editor](https://ankiweb.net/shared/info/1103084694)

## Inspiration

In addition to inspiration drawn from Anki's cloze system itself, there are a couple related Anki cloze plugins that provided some inspiration for features found here.  Thanks to all authors for the thought put into Anki and these plugins that have helped develop new ideas.

* [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686)
* [Cloze Overlapper](https://ankiweb.net/shared/info/969733775)

## Plugin Releases

* 0.1 - Initial release (2019-12-17)
* 0.2 - Add menu actions Auto-cloze Full Field and Create Missing Cards (2019-12-29)
* 0.4 - Update to work with Anki 2.1.49 (2021-12-08).

## Template Releases

* (2019-12-17) Initial release
* (2019-12-24) Template now allows numbers within field names.
* (2020-01-03) Additional configuration options.  Backticks to retain characters as hints.
* (2020-05-31) Add CSS for current cloze to highlight it on the back side of card.  Change font weight for current cloze to bold.  See <a href="https://github.com/matthayes/anki_cloze_anything/issues/7">Issue #7</a>

## License

Copyright 2019-2021 Matthew Hayes

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

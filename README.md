# Anki Cloze Anything

This project provides a JavaScript-based cloze implementation that is completely independent from Anki's [Cloze Deletion](https://apps.ankiweb.net/docs/manual.html#cloze-deletion) and does not require any modifications to Anki (via a plugin) for it to work.  This is achieved purely through JavaScript in the card template and a novel application of Anki's built-in (awesome) [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  It has no dependency on Anki's Cloze note type nor any other note types.  It works on both Anki Desktop and Mobile.

Replicating Anki functionality with JavaScript and card templates is not the goal however.  The goal is endless flexibility.  You can add cloze cards to any existing note type ("cloze anything") simply by adding new fields and card templates based on the instructions found here.  You can also modify the templates completely, using them simply as a guide.

An optional [plugin](https://ankiweb.net/shared/info/330680661) is also provided that automates some of the otherwise (minimal) manual work that would be required when following this approach.

Here are more details about some cool things you can do with this approach:

* **Add cloze deletion to an existing note**.  Suppose you already have a note with fields *Expression* and *Meaning* and a card that tests you on Expression -> Meaning.  Now suppose you want a version of *Expression* with cloze deletions.  Normally with Anki you'd have to copy the text to a completely separate note based on the *Cloze* note type.  This is a big headache to manage.  Instead with the Cloze Anything approach you copy the text to a *ExpressionCloze* field in the same note.  This makes it much easier to manage the content.  You can easily find notes that don't have a cloze through a simple search in the browser.
* **Add multiple cloze deletion fields to an existing note**.  Suppose that you have a note type that tests you on vocabulary with fields *VocabItem* and *Meaning*.  Suppose that you have added some example fields *ExampleA* and *ExampleB* to provide examples of how the vocabulary item is used.  With the Cloze Anything approach you can create cloze versions for each of these examples as *ExampleACloze* and *ExampleBCloze* and render cards from each of them.  (Note: the template does not currently support numbers within the field name).
* **Control the visibility of other close deletions**.  Normally Anki will show the other cloze deletions besides the one currently being tested for a particular card.  The approach here let's you customize this, similar to the functionality provided by [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).

## Getting Started

There are two options for getting started:

1. Download one of the shared decks I've already prepared for you and use the note type (and card templates) as the basis for your cards.
2. Follow my [detailed instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) on how to set up the fields and card templates.  This is the best choice when you want to add cloze to an existing note type.

Shared decks can be found here:

* [Cloze Anything Sample](https://ankiweb.net/shared/info/1637056056)

## How the Template Works

Similar to Anki's [Cloze Templates](https://apps.ankiweb.net/docs/manual.html#cloze-templates), you need a field to contain the cloze content.  Out of convention it's a good idea to have the field name end in *Cloze* in case you want to use the plugin later.  Suppose you name it `ClozeExpression`, as suggested in the instructions.  Cloze content is entered in this field in a similar way as with Anki's Cloze Templates.  The only difference is that instead of the format `{{c1::text}}` you use `((c1::text))`.  You then need fields to enable each of the cloze cards.  So, suppose you want to support three clozes.  You would add fields `ClozeExpression1`, `ClozeExpression2`, and `ClozeExpression3`.  You enter any text you want into these fields to enable the corresponding cloze card.  Out of convention the plugin uses `1`.

For example, suppose you want to create cloze cards for each of the words in the expression *Ik heb honger*.  You would write the fields like so:

![Ik heb honger fields](https://raw.githubusercontent.com/matthayes/anki_cloze_anything/master/images/ik_heb_honger.png)

For an HTML rendering of this example, see [here](https://htmlpreview.github.io/?https://github.com/matthayes/anki_cloze_anything/blob/master/examples/front.html).

Because each of the cloze fields has a non-empty value of `1`, a card will be generated for each of `c1` through `c3`.  If you deleted the `1` from `ClozeExpression3` then a card will be generated for `c1` and `c2` only.

Let's dig into how this all works.  The [instructions](https://github.com/matthayes/anki_cloze_anything/blob/master/docs/INSTRUCTIONS.md) referenced earlier have the following template for the first cloze card.  Notice that the entire content of the front of the card is surrounded by conditional tags based on `ExpressionCloze` and `ExpressionCloze1`.  This means that both fields must be non-empty for the card to be created, due to the way Anki card generation works.  So if either of these fields is empty, the corresponding card isn't generated.  The ommitted script simply looks at the number the value for `data-card` ends with and then updates the content within the cloze `<div>` accordingly.  So if the value of `data-card` is `ClozeExpression2` then it knows to hide the `((c2::text))` and show the others.

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

* **Auto-cloze Full Field:** This automatically makes a cloze from an entire field.  For example, suppose you have a field named `ExpressionCloze` and `Expression`.  If `ExpressionCloze` is empty, then this action causes the content of Expression to be copied to `ExpressionCloze` and made into a cloze like `((c1::content))`.  It also updates `ExpressionCloze1` to cause the cloze card to be generated.  This is useful when you have a lot of notes with short content where you want to cloze the entire content.  It's much more efficient to cloze these in bulk than one by one.
* **Create Missing Cards:** This basically just makes sure the Cloze field is in sync with the corresponding fields responsible for card generation.  For example, if `ExpressionCloze` has `((c1::Ik)) ((c2::heb)) ((c3::honger)).` then this would ensure `ExpressionCloze1`, `ExpressionCloze2`, and `ExpressionCloze3` are each filled in with a `1`.  But `ExpressionCloze4` would be made blank, if it exists.  This action isn't generally necessary to use while using the plugin because the plugin ensures that these fields are updated as you change content.  But if something goes wrong or if you edit notes before using the plugin, this can be used to fix up the fields to be in sync.

## Configuration

The template has a couple settings for controlling how the cloze deletions are rendered.  These are `data-cloze-show-before` and `data-cloze-show-after`, as shown in the snippet from the template below.

```
<div id="cloze" data-card="{{Card}}" data-cloze-show-before="all" data-cloze-show-after="all">
{{ExpressionCloze}}
</div>
```

In the snippet above, both of these have the value `all`.  This means that all cloze deletions before and after the current cloze will be displayed.  For example, suppose that the content is:

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

## Pros and Cons

Pros:

* Cloze cards can be added to existing note types without any modifications other than adding new fields and card templates.
* Compared to Anki's built-in Cloze type, you have more flexibility in how the cloze cards are rendered.  You can choose how many of the other cloze values to show, instead of always showing them all.  This functionality is similar to that provided by [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).
* Relies on JavaScript and built-in Anki features such as [Selective Card Generation](https://apps.ankiweb.net/docs/manual.html#selective-card-generation).  As cloze functionality is implemented in the templates no modifications to Anki via a plugin are required for it to work.  This greatly reduces the chance that future Anki updates will break this approach.
* No external JavaScript required.  All necessary JavaScript exists in the templates.

Cons:

* Relies on JavaScript, which works because Anki cards are treated like webpages. However, the Anki author notes that [Javascript functionality is provided without any support or warranty](https://apps.ankiweb.net/docs/manual.html#javascript).  So there is a very small chance that a future Anki update could impact card rendering and require changes in the template, which would be promptly carried out by me given my dependence on this approach working.
* Because cloze functionality is implemented in templates, rather than Anki, the same template effectively needs to be copied to each card template.  The good news is you only need to do this setup once if you are setting up the templates manually.  If you use one of the shared decks then this doesn't impact you.
* Adding the `type:` prefix to enable type in the answer is not supported.

## Compatibility

The card templates have been tested with Anki Desktop 2.1 and the latest version of Anki Mobile.  The card templates probably work with Anki Desktop 2.0, however I have not tried it yet.

The plugin works with Anki Desktop 2.1.  I have no plans to add 2.0 support.

I have not yet tested interactions of the plugin with other cloze plugins such as [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686) and [Cloze Overlapper](https://ankiweb.net/shared/info/969733775).  If you encounter a problem please file an issue and I will do my best to fix it.

## Inspiration

In addition to inspiration drawn from Anki's cloze system itself, there are a couple related Anki cloze plugins that provided some inspiration for features found here.  Thanks to all authors for the thought put into Anki and these plugins that have helped develop new ideas.

* [Cloze (Hide All)](https://ankiweb.net/shared/info/1709973686)
* [Cloze Overlapper](https://ankiweb.net/shared/info/969733775)

## Releases

* 0.1 - Initial release (2019-12-17)
* 0.2 - Add menu actions Auto-cloze Full Field and Create Missing Cards (2019-12-29)

## License

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

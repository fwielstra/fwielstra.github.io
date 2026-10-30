# Building Assistants using Google Assistant actions and Dialogflow

* History (vague)
  * Dialogflow was originally built by a company called Speaktoit, who used it in their own app called Assistant for Android, iOS and Windows Phone in 2012.
  * Bought in 2016 by Google and the tool was rebranded as API.AI, allowing people to create custom Actions for the Google Assistant

* How to
  * Building a custom Assistant is an er, interesting dance between Actions on Google, Dialogflow, and your custom web hook handler (if any) running - for example - on Firebase Functions.
  * You define 'entrypoints' of sorts, called Intents, in Dialogflow
    * For these you provide a number of example inputs, which Dialogflow will analyze and grab Entities from - numbers, dates, colors, locations, durations, etc.
    * You can create your own Entities as well, mostly hardcoded ones.
    * pretty sure (TODO) you can pass whole phrases to your web hook and have it figure out entites from programmatically.
  * If an Intent is triggered, you can either have it stay 'inside' Dialogflow by e.g. creating follow-up questions, or pass it on to your web hook
    * serverless lambda, so, woot
  * The relevant intent handler is called with just the relevant parameters
    * from the handler you can store the data and ask follow-up questions, or output richly formatted responses, etc.
    * chapter on its own
  * something something blaat.

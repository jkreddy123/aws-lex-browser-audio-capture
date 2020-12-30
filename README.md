# Speech<->Text NLP on browser using Google API
- Record audio using HTML5 media `audioControl` browser API
- Playback recorded audio on browser
- send recorded 16KHz WAV audio to cloud storage
- Transcribe Speech -> text
- Transcribe text -> speech back, MP3 audio
- Play the Mp3 audio buffer on browser


## Setup

## Demo
https://aqueous-dawn-66602.herokuapp.com/example/index.html

## Usage


### Conversation
The `conversation` object provides an abstraction on top of the GCP API and makes it easy to manage conversation state (Passive, Listening, Recording, Speaking) and perform silence detection.

#### Create the `conversation` object 
```
var conversation = new LexAudio.conversation({lexConfig:{botName: 'BOT_NAME'}}, 
function (state) { // Called on each state change.
}, 
function (data) { // Called with the LexRuntime.PostContent response.
},
function (error){ // Called on error.
},
function (timeDomain) { // Called with audio time domain data (useful for rendering the recorded audio levels).
});
```
#### Start the conversation
```
conversation.advanceConversation();
```
Advances the conversation from Passive to Listening. By default, silence detection will be used to transition to Sending and the conversation will continue Listenting, Sending, and Speaking until the Dialog state is [Fulfilled] Here are the conversation state transitions. 

```
                                       onPlaybackComplete and ElicitIntent | ConfirmIntent | ElicitSlot
                                         +--------------------------------------------------------+
                                         |                                                        |
   +---------+                     +-----v-----+                     +---------+            +----------+
   |         | advanceConversation |           | advanceConversation |         | onResponse |          |
   | Passive +-------------------> | Listening +-------------------> | Sending +----------> | Speaking |
   |         |                     |           | onSilence           |         |            |          |
   +----^----+                     +-----------+                     +---------+            +----------+
        |                                                                                         |
        +-----------------------------------------------------------------------------------------+
           onPlaybackComplete and Fulfilled | ReadyForFulfillment | Failed | no silence detection
```

Setting silence detection to false allows you to manually transition out of the Passive and Listening states by calling `conversation.advanceConversation()`.

```
var conversation = new LexAudio.conversation({silenceDetection: false, lexConfig:{botName: 'BOT_NAME'}}, ... );
```

You can pass silence detection configuration values to tune the silence detection algorithm. The `time` value is the amount of silence to wait for (in milliseconds). The `amplitude` is a threshold value (between 1 and -1). Above the `amplitude` threshold value is considered "noise". Below the `amplitude` threshold value is considered "silence". Here is the complete configuration object. Everything except `botName` has a default value.

```
{
  silenceDetection: true, 
  silenceDetectionConfig: {
    time: 1500,
    amplitude: 0.2
  },
  lexConfig:{
    botName: 'BOT_NAME',
    botAlias: '$LATEST',
    contentType: 'audio/x-l16; sample-rate=16000',
    userId: 'userId',
    accept: 'audio/mpeg'
  }
}
```
## Browser support
This example code has been tested in the latest versions of:
* Chrome
* Firefox
* Safari (on macOS)

Title: Create a Message - Anthropic

URL Source: http://docs.anthropic.com/en/api/messages

Markdown Content:
Create a Message - Anthropic
===============
  

   

[Anthropic home page![Image 3: light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![Image 4: dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](http://docs.anthropic.com/)

English

Search...

*   [Go to claude.ai](https://claude.ai/)
*   [Research](https://www.anthropic.com/research)
*   [News](https://www.anthropic.com/news)
*   [Go to claude.ai](https://claude.ai/)

Search...

Navigation

Messages

Create a Message

[Welcome](http://docs.anthropic.com/en/home)[User Guides](http://docs.anthropic.com/en/docs/welcome)[API Reference](http://docs.anthropic.com/en/api/getting-started)[Prompt Library](http://docs.anthropic.com/en/prompt-library/library)[Release Notes](http://docs.anthropic.com/en/release-notes/overview)[Developer Newsletter](http://docs.anthropic.com/en/developer-newsletter/overview)

*   [Developer Console](https://console.anthropic.com/)
*   [Developer Discord](https://www.anthropic.com/discord)
*   [Support](https://support.anthropic.com/)

##### Using the API

*   [Getting started](http://docs.anthropic.com/en/api/getting-started)
*   [IP addresses](http://docs.anthropic.com/en/api/ip-addresses)
*   [Versions](http://docs.anthropic.com/en/api/versioning)
*   [Errors](http://docs.anthropic.com/en/api/errors)
*   [Rate limits](http://docs.anthropic.com/en/api/rate-limits)
*   [Client SDKs](http://docs.anthropic.com/en/api/client-sdks)
*   [Supported regions](http://docs.anthropic.com/en/api/supported-regions)
*   [Getting help](http://docs.anthropic.com/en/api/getting-help)

##### Anthropic APIs

*   Messages
    
    *   [POST Create a Message](http://docs.anthropic.com/en/api/messages)
    *   [POST Count Message tokens (beta)](http://docs.anthropic.com/en/api/messages-count-tokens)
    *   [Streaming Messages](http://docs.anthropic.com/en/api/messages-streaming)
    *   [Migrating from Text Completions](http://docs.anthropic.com/en/api/migrating-from-text-completions-to-messages)
    *   [Messages examples](http://docs.anthropic.com/en/api/messages-examples)
*   Message Batches (beta)
    
*   Text Completions (Legacy)
    
*   Admin API
    

##### Amazon Bedrock API

*   [Amazon Bedrock API](http://docs.anthropic.com/en/api/claude-on-amazon-bedrock)

##### Vertex AI

*   [Vertex AI API](http://docs.anthropic.com/en/api/claude-on-vertex-ai)

Messages

Create a Message
================

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

POST

/

v1

/

messages

#### Headers

anthropic-beta

string\[\]

Optional header to specify the beta version(s) you want to use.

To use multiple betas, use a comma separated list like `beta1,beta2` or specify the header multiple times for each beta.

anthropic-version

string

required

The version of the Anthropic API you want to use.

Read more about versioning and our version history [here](https://docs.anthropic.com/en/api/versioning).

x-api-key

string

required

Your unique API key for authentication.

This key is required in the header of all API requests, to authenticate your account and access Anthropic's services. Get your API key through the [Console](https://console.anthropic.com/settings/keys). Each key is scoped to a Workspace.

#### Body

application/json

model

string

required

The model that will complete your prompt.

See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

messages

object\[\]

required

Input messages.

Our models are trained to operate on alternating `user` and `assistant` conversational turns. When creating a new `Message`, you specify the prior conversational turns with the `messages` parameter, and the model then generates the next `Message` in the conversation. Consecutive `user` or `assistant` turns in your request will be combined into a single turn.

Each input message must be an object with a `role` and `content`. You can specify a single `user`\-role message, or you can include multiple `user` and `assistant` messages.

If the final message uses the `assistant` role, the response content will continue immediately from the content in that message. This can be used to constrain part of the model's response.

Example with a single `user` message:

```json
[{"role": "user", "content": "Hello, Claude"}]
```

Example with multiple conversational turns:

```json
[
  {"role": "user", "content": "Hello there."},
  {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
  {"role": "user", "content": "Can you explain LLMs in plain English?"},
]
```

Example with a partially-filled response from Claude:

```json
[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("},
]
```

Each input message `content` may be either a single `string` or an array of content blocks, where each block has a specific `type`. Using a `string` for `content` is shorthand for an array of one content block of type `"text"`. The following input messages are equivalent:

```json
{"role": "user", "content": "Hello, Claude"}
```

```json
{"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}]}
```

Starting with Claude 3 models, you can also send image content blocks:

```json
{"role": "user", "content": [
  {
    "type": "image",
    "source": {
      "type": "base64",
      "media_type": "image/jpeg",
      "data": "/9j/4AAQSkZJRg...",
    }
  },
  {"type": "text", "text": "What is in this image?"}
]}
```

We currently support the `base64` source type for images, and the `image/jpeg`, `image/png`, `image/gif`, and `image/webp` media types.

See [examples](https://docs.anthropic.com/en/api/messages-examples#vision) for more input examples.

Note that if you want to include a [system prompt](https://docs.anthropic.com/en/docs/system-prompts), you can use the top-level `system` parameter — there is no `"system"` role for input messages in the Messages API.

Show child attributes

max\_tokens

integer

required

The maximum number of tokens to generate before stopping.

Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

Different models have different maximum values for this parameter. See [models](https://docs.anthropic.com/en/docs/models-overview) for details.

metadata

object

An object describing metadata about the request.

Show child attributes

stop\_sequences

string\[\]

Custom text sequences that will cause the model to stop generating.

Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

stream

boolean

Whether to incrementally stream the response using server-sent events.

See [streaming](https://docs.anthropic.com/en/api/messages-streaming) for details.

system

System prompt.

A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.anthropic.com/en/docs/system-prompts).

temperature

number

Amount of randomness injected into the response.

Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

tool\_choice

object

How the model should use the provided tools. The model can use a specific tool, any available tool, or decide by itself.

*   Auto
*   Any
*   Tool

Show child attributes

tools

object\[\]

Definitions of tools that the model may use.

If you include `tools` in your API request, the model may return `tool_use` content blocks that represent the model's use of those tools. You can then run those tools using the tool input generated by the model and then optionally return results back to the model using `tool_result` content blocks.

Each tool definition includes:

*   `name`: Name of the tool.
*   `description`: Optional, but strongly-recommended description of the tool.
*   `input_schema`: [JSON schema](https://json-schema.org/) for the tool `input` shape that the model will produce in `tool_use` output content blocks.

For example, if you defined `tools` as:

```json
[
  {
    "name": "get_stock_price",
    "description": "Get the current stock price for a given ticker symbol.",
    "input_schema": {
      "type": "object",
      "properties": {
        "ticker": {
          "type": "string",
          "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
        }
      },
      "required": ["ticker"]
    }
  }
]
```

And then asked the model "What's the S&P 500 at today?", the model might produce `tool_use` content blocks in the response like this:

```json
[
  {
    "type": "tool_use",
    "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
    "name": "get_stock_price",
    "input": { "ticker": "^GSPC" }
  }
]
```

You might then run your `get_stock_price` tool with `{"ticker": "^GSPC"}` as an input, and return the following back to the model in a subsequent `user` message:

```json
[
  {
    "type": "tool_result",
    "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
    "content": "259.75 USD"
  }
]
```

Tools can be used for workflows that include running client-side tools and functions, or more generally whenever you want the model to produce a particular JSON structure of output.

See our [guide](https://docs.anthropic.com/en/docs/tool-use) for more details.

*   Tool
*   ComputerUseTool\_20241022
*   BashTool\_20241022
*   TextEditor\_20241022

Show child attributes

top\_k

integer

Only sample from the top K options for each subsequent token.

Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

Recommended for advanced use cases only. You usually only need to use `temperature`.

top\_p

number

Use nucleus sampling.

In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

Recommended for advanced use cases only. You usually only need to use `temperature`.

#### Response

200 - application/json

id

string

required

Unique object identifier.

The format and length of IDs may change over time.

type

enum<string\>

default: messagerequired

Object type.

For Messages, this is always `"message"`.

Available options:

`message`

role

enum<string\>

default: assistantrequired

Conversational role of the generated message.

This will always be `"assistant"`.

Available options:

`assistant`

content

object\[\]

required

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

```json
[{"type": "text", "text": "Hi, I'm Claude."}]
```

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

```json
[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]
```

Then the response `content` might be:

```json
[{"type": "text", "text": "B)"}]
```

*   Text
*   Tool Use

Show child attributes

model

string

required

The model that handled the request.

stop\_reason

enum<string\> | null

required

The reason that we stopped.

This may be one the following values:

*   `"end_turn"`: the model reached a natural stopping point
*   `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
*   `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
*   `"tool_use"`: the model invoked one or more tools

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

Available options:

`end_turn`,

`max_tokens`,

`stop_sequence`,

`tool_use`

stop\_sequence

string | null

required

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

usage

object

required

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Show child attributes

Was this page helpful?

YesNo

[Getting help](http://docs.anthropic.com/en/api/getting-help)[Count Message tokens (beta)](http://docs.anthropic.com/en/api/messages-count-tokens)

[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)
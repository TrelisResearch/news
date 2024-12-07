Title: Chat Completions - Perplexity

URL Source: http://docs.perplexity.ai/api-reference/chat-completions

Markdown Content:
#### Authorizations

Bearer authentication header of the form `Bearer <token>`, where `<token>` is your auth token.

#### Body

The name of the model that will complete your prompt. Refer to [Supported Models](https://docs.perplexity.ai/docs/model-cards) to find all the models offered.

A list of messages comprising the conversation so far.

The maximum number of completion tokens returned by the API. The total number of tokens requested in max\_tokens plus the number of prompt tokens sent in messages must not exceed the context window token limit of model requested. If left unspecified, then the model will generate tokens until either it reaches its stop token or the end of its context window.

The amount of randomness in the response, valued between 0 inclusive and 2 exclusive. Higher values are more random, and lower values are more deterministic.

Required range: `0 < x < 2`

The nucleus sampling threshold, valued between 0 and 1 inclusive. For each subsequent token, the model considers the results of the tokens with top\_p probability mass. We recommend either altering top\_k or top\_p, but not both.

Required range: `0 < x < 1`

Given a list of domains, limit the citations used by the online model to URLs from the specified domains. Currently limited to only 3 domains for whitelisting and blacklisting. For **blacklisting** add a `-` to the beginning of the domain string. This filter is in [closed beta](https://perplexity.typeform.com/apiaccessform)

Determines whether or not a request to an online model should return images. Images are in [closed beta](https://perplexity.typeform.com/apiaccessform)

Determines whether or not a request to an online model should return related questions. Related questions are in [closed beta](https://perplexity.typeform.com/apiaccessform)

Returns search results within the specified time interval - does not apply to images. Values include `month`, `week`, `day`, `hour`.

The number of tokens to keep for highest top-k filtering, specified as an integer between 0 and 2048 inclusive. If set to 0, top-k filtering is disabled. We recommend either altering top\_k or top\_p, but not both.

Required range: `0 < x < 2048`

Determines whether or not to incrementally stream the response with [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format) with `content-type: text/event-stream`.

A value between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Incompatible with `frequency_penalty`.

Required range: `-2 < x < 2`

A multiplicative penalty greater than 0. Values greater than 1.0 penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. A value of 1.0 means no penalty. Incompatible with `presence_penalty`.

Required range: `x > 0`

#### Response

An ID generated uniquely for each response.

The model used to generate the response.

The object type, which always equals `chat.completion`.

The Unix timestamp (in seconds) of when the completion was created.

Citations for the generated answer.

The list of completion choices the model generated for the input prompt.

Usage statistics for the completion request.
Images
Given a prompt and/or an input image, the model will generate a new image. Related guide: Image generation

Create image
post
 
https://api.openai.com/v1/images/generations
Creates an image given a prompt.

Request body
prompt
string

Required
A text description of the desired image(s). The maximum length is 1000 characters for dall-e-2 and 4000 characters for dall-e-3.

model
string

Optional
Defaults to dall-e-2
The model to use for image generation.

n
integer or null

Optional
Defaults to 1
The number of images to generate. Must be between 1 and 10. For dall-e-3, only n=1 is supported.

quality
string

Optional
Defaults to standard
The quality of the image that will be generated. hd creates images with finer details and greater consistency across the image. This param is only supported for dall-e-3.

response_format
string or null

Optional
Defaults to url
The format in which the generated images are returned. Must be one of url or b64_json. URLs are only valid for 60 minutes after the image has been generated.

size
string or null

Optional
Defaults to 1024x1024
The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024 for dall-e-2. Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models.

style
string or null

Optional
Defaults to vivid
The style of the generated images. Must be one of vivid or natural. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images. This param is only supported for dall-e-3.

user
string

Optional
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.

Returns
Returns a list of image objects.

Example request

from openai import OpenAI
client = OpenAI()

client.images.generate(
  model="dall-e-3",
  prompt="A cute baby sea otter",
  n=1,
  size="1024x1024"
)
Response

{
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}
Create image edit
post
 
https://api.openai.com/v1/images/edits
Creates an edited or extended image given an original image and a prompt.

Request body
image
file

Required
The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask is not provided, image must have transparency, which will be used as the mask.

prompt
string

Required
A text description of the desired image(s). The maximum length is 1000 characters.

mask
file

Optional
An additional image whose fully transparent areas (e.g. where alpha is zero) indicate where image should be edited. Must be a valid PNG file, less than 4MB, and have the same dimensions as image.

model
string

Optional
Defaults to dall-e-2
The model to use for image generation. Only dall-e-2 is supported at this time.

n
integer or null

Optional
Defaults to 1
The number of images to generate. Must be between 1 and 10.

size
string or null

Optional
Defaults to 1024x1024
The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.

response_format
string or null

Optional
Defaults to url
The format in which the generated images are returned. Must be one of url or b64_json. URLs are only valid for 60 minutes after the image has been generated.

user
string

Optional
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.

Returns
Returns a list of image objects.

Example request

from openai import OpenAI
client = OpenAI()

client.images.edit(
  image=open("otter.png", "rb"),
  mask=open("mask.png", "rb"),
  prompt="A cute baby sea otter wearing a beret",
  n=2,
  size="1024x1024"
)
Response

{
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}
Create image variation
post
 
https://api.openai.com/v1/images/variations
Creates a variation of a given image.

Request body
image
file

Required
The image to use as the basis for the variation(s). Must be a valid PNG file, less than 4MB, and square.

model
string

Optional
Defaults to dall-e-2
The model to use for image generation. Only dall-e-2 is supported at this time.

n
integer or null

Optional
Defaults to 1
The number of images to generate. Must be between 1 and 10. For dall-e-3, only n=1 is supported.

response_format
string or null

Optional
Defaults to url
The format in which the generated images are returned. Must be one of url or b64_json. URLs are only valid for 60 minutes after the image has been generated.

size
string or null

Optional
Defaults to 1024x1024
The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.

user
string

Optional
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.

Returns
Returns a list of image objects.

Example request

from openai import OpenAI
client = OpenAI()

response = client.images.create_variation(
  image=open("image_edit_original.png", "rb"),
  n=2,
  size="1024x1024"
)
Response

{
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}
The image object
Represents the url or the content of an image generated by the OpenAI API.

b64_json
string

The base64-encoded JSON of the generated image, if response_format is b64_json.

url
string

The URL of the generated image, if response_format is url (default).

revised_prompt
string

The prompt that was used to generate the image, if there was any revision to the prompt.

OBJECT The image object

{
  "url": "...",
  "revised_prompt": "..."
}
Models
List and describe the various models available in the API. You can refer to the Models documentation to understand what models are available and the differences between them.

List models
get
 
https://api.openai.com/v1/models
Lists the currently available models, and provides basic information about each one such as the owner and availability.

Returns
A list of model objects.

Example request

from openai import OpenAI
client = OpenAI()

client.models.list()
Response

{
  "object": "list",
  "data": [
    {
      "id": "model-id-0",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    },
    {
      "id": "model-id-1",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner",
    },
    {
      "id": "model-id-2",
      "object": "model",
      "created": 1686935002,
      "owned_by": "openai"
    },
  ],
  "object": "list"
}
Retrieve model
get
 
https://api.openai.com/v1/models/{model}
Retrieves a model instance, providing basic information about the model such as the owner and permissioning.

Path parameters
model
string

Required
The ID of the model to use for this request

Returns
The model object matching the specified ID.

Example request

from openai import OpenAI
client = OpenAI()

client.models.retrieve("gpt-4o")
Response

{
  "id": "gpt-4o",
  "object": "model",
  "created": 1686935002,
  "owned_by": "openai"
}
Delete a fine-tuned model
delete
 
https://api.openai.com/v1/models/{model}
Delete a fine-tuned model. You must have the Owner role in your organization to delete a model.

Path parameters
model
string

Required
The model to delete

Returns
Deletion status.

Example request

from openai import OpenAI
client = OpenAI()

client.models.delete("ft:gpt-4o-mini:acemeco:suffix:abc123")
Response

{
  "id": "ft:gpt-4o-mini:acemeco:suffix:abc123",
  "object": "model",
  "deleted": true
}
The model object
Describes an OpenAI model offering that can be used with the API.

id
string

The model identifier, which can be referenced in the API endpoints.

created
integer

The Unix timestamp (in seconds) when the model was created.

object
string

The object type, which is always "model".

owned_by
string

The organization that owns the model.

OBJECT The model object

{
  "id": "gpt-4o",
  "object": "model",
  "created": 1686935002,
  "owned_by": "openai"
}
Moderations
Given text and/or image inputs, classifies if those inputs are potentially harmful across several categories. Related guide: Moderations

Create moderation
post
 
https://api.openai.com/v1/moderations
Classifies if text and/or image inputs are potentially harmful. Learn more in the moderation guide.

Request body
input
string or array

Required
Input (or inputs) to classify. Can be a single string, an array of strings, or an array of multi-modal input objects similar to other models.


Show possible types
model
string

Optional
Defaults to omni-moderation-latest
The content moderation model you would like to use. Learn more in the moderation guide, and learn about available models here.

Returns
A moderation object.


Single string

Image and text
Example request

from openai import OpenAI
client = OpenAI()

moderation = client.moderations.create(input="I want to kill them.")
print(moderation)
Response

{
  "id": "modr-AB8CjOTu2jiq12hp1AQPfeqFWaORR",
  "model": "text-moderation-007",
  "results": [
    {
      "flagged": true,
      "categories": {
        "sexual": false,
        "hate": false,
        "harassment": true,
        "self-harm": false,
        "sexual/minors": false,
        "hate/threatening": false,
        "violence/graphic": false,
        "self-harm/intent": false,
        "self-harm/instructions": false,
        "harassment/threatening": true,
        "violence": true
      },
      "category_scores": {
        "sexual": 0.000011726012417057063,
        "hate": 0.22706663608551025,
        "harassment": 0.5215635299682617,
        "self-harm": 2.227119921371923e-6,
        "sexual/minors": 7.107352217872176e-8,
        "hate/threatening": 0.023547329008579254,
        "violence/graphic": 0.00003391829886822961,
        "self-harm/intent": 1.646940972932498e-6,
        "self-harm/instructions": 1.1198755256458526e-9,
        "harassment/threatening": 0.5694745779037476,
        "violence": 0.9971134662628174
      }
    }
  ]
}
The moderation object
Represents if a given text input is potentially harmful.

id
string

The unique identifier for the moderation request.

model
string

The model used to generate the moderation results.

results
array

A list of moderation objects.


Show properties
OBJECT The moderation object

{
  "id": "modr-0d9740456c391e43c445bf0f010940c7",
  "model": "omni-moderation-latest",
  "results": [
    {
      "flagged": true,
      "categories": {
        "harassment": true,
        "harassment/threatening": true,
        "sexual": false,
        "hate": false,
        "hate/threatening": false,
        "illicit": false,
        "illicit/violent": false,
        "self-harm/intent": false,
        "self-harm/instructions": false,
        "self-harm": false,
        "sexual/minors": false,
        "violence": true,
        "violence/graphic": true
      },
      "category_scores": {
        "harassment": 0.8189693396524255,
        "harassment/threatening": 0.804985420696006,
        "sexual": 1.573112165348997e-6,
        "hate": 0.007562942636942845,
        "hate/threatening": 0.004208854591835476,
        "illicit": 0.030535955153511665,
        "illicit/violent": 0.008925306722380033,
        "self-harm/intent": 0.00023023930975076432,
        "self-harm/instructions": 0.0002293869201073356,
        "self-harm": 0.012598046106750154,
        "sexual/minors": 2.212566909570261e-8,
        "violence": 0.9999992735124786,
        "violence/graphic": 0.843064871157054
      },
      "category_applied_input_types": {
        "harassment": [
          "text"
        ],
        "harassment/threatening": [
          "text"
        ],
        "sexual": [
          "text",
          "image"
        ],
        "hate": [
          "text"
        ],
        "hate/threatening": [
          "text"
        ],
        "illicit": [
          "text"
        ],
        "illicit/violent": [
          "text"
        ],
        "self-harm/intent": [
          "text",
          "image"
        ],
        "self-harm/instructions": [
          "text",
          "image"
        ],
        "self-harm": [
          "text",
          "image"
        ],
        "sexual/minors": [
          "text"
        ],
        "violence": [
          "text",
          "image"
        ],
        "violence/graphic": [
          "text",
          "image"
        ]
      }
    }
  ]
}
Assistants
Beta
Build assistants that can call models and use tools to perform tasks.

Get started with the Assistants API

Create assistant
Beta
post
 
https://api.openai.com/v1/assistants
Create an assistant with a model and instructions.

Request body
model
string

Required
ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.

name
string or null

Optional
The name of the assistant. The maximum length is 256 characters.

description
string or null

Optional
The description of the assistant. The maximum length is 512 characters.

instructions
string or null

Optional
The system instructions that the assistant uses. The maximum length is 256,000 characters.

tools
array

Optional
Defaults to []
A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, or function.


Show possible types
tool_resources
object or null

Optional
A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the code_interpreter tool requires a list of file IDs, while the file_search tool requires a list of vector store IDs.


Show properties
metadata
map

Optional
Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maximum of 512 characters long.

temperature
number or null

Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

top_p
number or null

Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

response_format
"auto" or object

Optional
Specifies the format that the model must output. Compatible with GPT-4o, GPT-4 Turbo, and all GPT-3.5 Turbo models since gpt-3.5-turbo-1106.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.


Show possible types
Returns
An assistant object.


Code Interpreter

Files
Example request

from openai import OpenAI
client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)
print(my_assistant)
Response

{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1698984975,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}
List assistants
Beta
get
 
https://api.openai.com/v1/assistants
Returns a list of assistants.

Query parameters
limit
integer

Optional
Defaults to 20
A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

order
string

Optional
Defaults to desc
Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

after
string

Optional
A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

before
string

Optional
A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.

Returns
A list of assistant objects.

Example request

from openai import OpenAI
client = OpenAI()

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
print(my_assistants.data)
Response

{
  "object": "list",
  "data": [
    {
      "id": "asst_abc123",
      "object": "assistant",
      "created_at": 1698982736,
      "name": "Coding Tutor",
      "description": null,
      "model": "gpt-4o",
      "instructions": "You are a helpful assistant designed to make me better at coding!",
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    },
    {
      "id": "asst_abc456",
      "object": "assistant",
      "created_at": 1698982718,
      "name": "My Assistant",
      "description": null,
      "model": "gpt-4o",
      "instructions": "You are a helpful assistant designed to make me better at coding!",
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    },
    {
      "id": "asst_abc789",
      "object": "assistant",
      "created_at": 1698982643,
      "name": null,
      "description": null,
      "model": "gpt-4o",
      "instructions": null,
      "tools": [],
      "tool_resources": {},
      "metadata": {},
      "top_p": 1.0,
      "temperature": 1.0,
      "response_format": "auto"
    }
  ],
  "first_id": "asst_abc123",
  "last_id": "asst_abc789",
  "has_more": false
}
Retrieve assistant
Beta
get
 
https://api.openai.com/v1/assistants/{assistant_id}
Retrieves an assistant.

Path parameters
assistant_id
string

Required
The ID of the assistant to retrieve.

Returns
The assistant object matching the specified ID.

Example request

from openai import OpenAI
client = OpenAI()

my_assistant = client.beta.assistants.retrieve("asst_abc123")
print(my_assistant)
Response

{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1699009709,
  "name": "HR Helper",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are an HR bot, and you have access to files to answer employee questions about company policies.",
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}
Modify assistant
Beta
post
 
https://api.openai.com/v1/assistants/{assistant_id}
Modifies an assistant.

Path parameters
assistant_id
string

Required
The ID of the assistant to modify.

Request body
model
Optional
ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.

name
string or null

Optional
The name of the assistant. The maximum length is 256 characters.

description
string or null

Optional
The description of the assistant. The maximum length is 512 characters.

instructions
string or null

Optional
The system instructions that the assistant uses. The maximum length is 256,000 characters.

tools
array

Optional
Defaults to []
A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, or function.


Show possible types
tool_resources
object or null

Optional
A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the code_interpreter tool requires a list of file IDs, while the file_search tool requires a list of vector store IDs.


Show properties
metadata
map

Optional
Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maximum of 512 characters long.

temperature
number or null

Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

top_p
number or null

Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

response_format
"auto" or object

Optional
Specifies the format that the model must output. Compatible with GPT-4o, GPT-4 Turbo, and all GPT-3.5 Turbo models since gpt-3.5-turbo-1106.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.


Show possible types
Returns
The modified assistant object.

Example request

from openai import OpenAI
client = OpenAI()

my_updated_assistant = client.beta.assistants.update(
  "asst_abc123",
  instructions="You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
  name="HR Helper",
  tools=[{"type": "file_search"}],
  model="gpt-4o"
)

print(my_updated_assistant)
Response

{
  "id": "asst_123",
  "object": "assistant",
  "created_at": 1699009709,
  "name": "HR Helper",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "tool_resources": {
    "file_search": {
      "vector_store_ids": []
    }
  },
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}
Delete assistant
Beta
delete
 
https://api.openai.com/v1/assistants/{assistant_id}
Delete an assistant.

Path parameters
assistant_id
string

Required
The ID of the assistant to delete.

Returns
Deletion status

Example request

from openai import OpenAI
client = OpenAI()

response = client.beta.assistants.delete("asst_abc123")
print(response)
Response

{
  "id": "asst_abc123",
  "object": "assistant.deleted",
  "deleted": true
}
The assistant object
Beta
Represents an assistant that can call the model and use tools.

id
string

The identifier, which can be referenced in API endpoints.

object
string

The object type, which is always assistant.

created_at
integer

The Unix timestamp (in seconds) for when the assistant was created.

name
string or null

The name of the assistant. The maximum length is 256 characters.

description
string or null

The description of the assistant. The maximum length is 512 characters.

model
string

ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.

instructions
string or null

The system instructions that the assistant uses. The maximum length is 256,000 characters.

tools
array

A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, or function.


Show possible types
tool_resources
object or null

A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the code_interpreter tool requires a list of file IDs, while the file_search tool requires a list of vector store IDs.


Show properties
metadata
map

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maximum of 512 characters long.

temperature
number or null

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

top_p
number or null

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

response_format
"auto" or object

Specifies the format that the model must output. Compatible with GPT-4o, GPT-4 Turbo, and all GPT-3.5 Turbo models since gpt-3.5-turbo-1106.

Setting to { "type": "json_schema", "json_schema": {...} } enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the Structured Outputs guide.

Setting to { "type": "json_object" } enables JSON mode, which ensures the message the model generates is valid JSON.

Important: when using JSON mode, you must also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if finish_reason="length", which indicates the generation exceeded max_tokens or the conversation exceeded the max context length.


Show possible types
OBJECT The assistant object

{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1698984975,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}
Threads
Beta

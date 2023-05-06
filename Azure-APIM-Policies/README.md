This folder contains the Azure API management policies that call Open AI / Azure OpenAI.

Here are useful policies that are commonly used:
- `completion.xml`: abstracts the completion API to API management.
- `backend-lb-and-fo.xml`: shows how APIM can be used to failover between multiple OpenAI endpoints, usually to handle throttling limits imposed by the endpoint service.

The following are Semantic APIs created using APIM policies. See [blog post](https://raffertyuy.com/raztype/rapid-api-development-with-apim-and-gpt/) to learn more.
- `is-valid-email.xml`
- `recommend-seo.xml`
- `translate.xml`

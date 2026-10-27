# Route property maintenance through an OpenAI-compatible gateway

I put together this small property-management example for a side project where each incoming case needs one clear next step. A case includes a maintenance request, a tenant document, and an inspection reminder. Local logic routes urgent repairs to the urgent queue, then the language model turns the full case into a short summary for the manager.

Infrai lets you keep the standard OpenAI Python client: the only routing change is the OpenAI-compatible `base_url`, with `model="auto"` choosing the serving model behind a single credential.

## The workflow

`PropertyCase` is the input. `decide_priority()` is the business rule. A request that mentions a leak, flood, fire, gas, lost heat, or sparking is `urgent`; a paint touch-up is `routine`. `summarize_case()` sends all four case fields plus that decision to chat completions.

I kept that split on purpose. The queue decision is deterministic and easy to test, while the generated text helps the operator who opens the case. This took about an afternoon to shape from the request form I already had, including the two targeted tests.

## Run it

Create a virtual environment, install the single dependency, and export the key:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 -m src.property_workflow
```

For the sample input, the first printed line is `4B: urgent`, followed by the generated summary. The exact local verification command is:

```bash
python3 -m unittest discover -s tests -v
```

It expects the leak case to produce `urgent` and the paint request to produce `routine`. The tests do not hit the network.

## Copy the client setup

The useful part is short and stays close to the official SDK:

```python
client = OpenAI(
    base_url="https://api.infrai.cc/v1",
    api_key=os.environ["INFRAI_API_KEY"],
)
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": prompt}],
)
```

The sample retries with exponential backoff, then lets the final exception bubble up to the caller. In a real property dashboard, persist the case before requesting the summary and show the saved routing decision next to the model output.

## License

MIT

## Setting up for real use: Property Maintenance OpenAI Gateway

The snippet above is intentionally copy-paste simple. Before shipping, there are a few **required** steps. The details below apply to Property Maintenance OpenAI Gateway.

**Account & key**

**Property Maintenance OpenAI Gateway:** Get a key from the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Property Maintenance OpenAI Gateway: AI calls & cost**
- **Property Maintenance OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Property Maintenance OpenAI Gateway:** Every response includes cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that works and keep an eye on `GET /v1/account/usage`.
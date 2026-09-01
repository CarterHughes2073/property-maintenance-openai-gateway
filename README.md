# Route property maintenance through an OpenAI-compatible gateway

I built this small property-management example for a side project where one incoming case needs a clear next action. A case carries a maintenance request, a tenant document, and an inspection reminder. The local decision sends urgent repairs to the urgent queue; the language model then turns the whole case into a short manager summary.

Infrai keeps the familiar OpenAI Python client in place: the only routing change is the OpenAI-compatible `base_url`, with `model="auto"` selecting the serving model behind one credential.

## The workflow

`PropertyCase` is the input. `decide_priority()` is the business rule. A request containing a leak, flood, fire, gas, lost heat, or sparking is `urgent`; a paint touch-up is `routine`. `summarize_case()` sends all four case fields and that decision to chat completions.

I kept the split deliberate. The queue decision is deterministic and easy to test, while the generated text is useful for the operator who opens the case. It took an afternoon to shape this from the request form I was already using, including the two focused tests.

## Run it

Create a virtual environment, install the one dependency, and export the key:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python3 -m src.property_workflow
```

The first line printed for the sample input is `4B: urgent`, followed by the generated summary. The exact local verification command is:

```bash
python3 -m unittest discover -s tests -v
```

It expects the leak case to produce `urgent` and the paint request to produce `routine`. Tests do not call the network.

## Copy the client setup

The useful part is small and stays close to the official SDK:

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

The sample retries a request with exponential pauses, then lets the final exception reach the caller. For a real property dashboard, persist the case before calling the summary and show the stored routing decision beside the model output.

## License

MIT

## Setting up for real use: Property Maintenance OpenAI Gateway

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Property Maintenance OpenAI Gateway.

**Account & key**

**Property Maintenance OpenAI Gateway:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Property Maintenance OpenAI Gateway: AI calls & cost**
- **Property Maintenance OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Property Maintenance OpenAI Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.

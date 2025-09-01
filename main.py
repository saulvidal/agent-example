from azure.ai.agents.models import ListSortOrder
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://aiservicesnvna.services.ai.azure.com/api/projects/projectnvna",
)

agent = project.agents.get_agent("asst_6r1o1bpdEsqLgpKNY2ht1Rhl")

thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

message = project.agents.messages.create(
    thread_id=thread.id, role="user", content="Dame un resumen de lo que tengo en el archivo subido"
)

run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

if run.status == "failed":
    print(f"Run failed: {run.last_error}")
else:
    messages = project.agents.messages.list(
        thread_id=thread.id, order=ListSortOrder.ASCENDING
    )

    for message in messages:
        if message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")

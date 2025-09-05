import pytest
from livekit.agents import AgentSession
from livekit.plugins import openai
from livekit_flows import (
    FlowAgent,
    ConversationFlow,
    FlowNode,
    Edge,
    CustomAction,
    HttpMethod,
    ActionTrigger,
    ActionTriggerType,
    DataField,
    FieldType,
)
from aiohttp.web import Application, json_response


create_profile_action = CustomAction(
    id="create_user_profile",
    name="Create User Profile",
    description="Create a user profile with collected information",
    method=HttpMethod.POST,
    url="/users/profile",
    headers={
        "Authorization": "Bearer {{ env.api_token }}",
        "Content-Type": "application/json",
    },
    body_template="""
    {
        "name": "{{ userdata.name }}",
        "email": "{{ userdata.email }}",
        "age": {{ userdata.age }},
        "preferences": {
            "cuisine": "{{ userdata.preferred_cuisine }}",
            "dietary_restrictions": "{{ userdata.dietary_restrictions }}",
            "budget_range": "{{ userdata.budget_range }}"
        },
        "registration_source": "voice_assistant"
    }
    """,
    store_response_as="profile_creation",
)

user_profile_flow = ConversationFlow(
    system_prompt="You are a helpful voice assistant that collects user information to create a profile.",
    initial_node="welcome",
    actions=[create_profile_action],
    environment_variables={
        "api_token": "test_api_token_12345",
    },
    nodes=[
        FlowNode(
            id="welcome",
            name="Welcome",
            instruction="Hello! I'm here to help you create your personalized profile. Let's start by collecting some information about you. What's your name?",
            edges=[
                Edge(
                    condition="User provided name",
                    id="collect_name_data",
                    target_node_id="collect_email",
                    collect_data=[
                        DataField(
                            name="name",
                            type=FieldType.STRING,
                            description="User's full name",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="collect_email",
            name="Collect Email",
            instruction="Great! Now, what's your email address?",
            edges=[
                Edge(
                    condition="User provided email",
                    id="collect_email_data",
                    target_node_id="collect_age",
                    collect_data=[
                        DataField(
                            name="email",
                            type=FieldType.STRING,
                            description="User's email address",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="collect_age",
            name="Collect Age",
            instruction="What's your age?",
            edges=[
                Edge(
                    condition="User provided age",
                    id="collect_age_data",
                    target_node_id="collect_preferences",
                    collect_data=[
                        DataField(
                            name="age",
                            type=FieldType.INTEGER,
                            description="User's age",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="collect_preferences",
            name="Collect Preferences",
            instruction="Thanks for sharing that info! Now, what's your preferred cuisine type (Italian, Chinese, Mexican, etc.)?",
            edges=[
                Edge(
                    condition="User provided cuisine preference",
                    id="collect_cuisine_data",
                    target_node_id="collect_dietary",
                    collect_data=[
                        DataField(
                            name="preferred_cuisine",
                            type=FieldType.STRING,
                            description="User's preferred cuisine",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="collect_dietary",
            name="Collect Dietary Info",
            instruction="Do you have any dietary restrictions or preferences (vegetarian, vegan, gluten-free, none, etc.)?",
            edges=[
                Edge(
                    condition="User provided dietary info",
                    id="collect_dietary_data",
                    target_node_id="collect_budget",
                    collect_data=[
                        DataField(
                            name="dietary_restrictions",
                            type=FieldType.STRING,
                            description="User's dietary restrictions",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="collect_budget",
            name="Collect Budget",
            instruction="Finally, what's your typical budget range for dining out (cheap, moderate, expensive)?",
            edges=[
                Edge(
                    condition="User provided budget info",
                    id="collect_budget_data",
                    target_node_id="create_profile",
                    collect_data=[
                        DataField(
                            name="budget_range",
                            type=FieldType.STRING,
                            description="User's budget range",
                            required=True,
                        )
                    ],
                )
            ],
        ),
        FlowNode(
            id="create_profile",
            name="Create Profile",
            instruction="""
                {% if actions.profile_creation.success %}
                Your profile has been created successfully!
                {{ actions.profile_creation.welcome_message }}
                Your profile ID is {{ actions.profile_creation.data.profile_id }}
                {% else %}
                Sorry, there was a problem creating your profile. Please try again.
                {% endif %}
            """,
            actions=[
                ActionTrigger(
                    action_id="create_user_profile",
                    trigger_type=ActionTriggerType.ON_ENTER,
                )
            ],
            is_final=True,
        ),
    ],
)


@pytest.mark.asyncio
async def test_action_user_profile_creation_with_real_api(
    aiohttp_server, mock_job_context
):
    async def create_profile_handler(request):
        assert request.method == "POST"
        assert "Authorization" in request.headers
        assert "Content-Type" in request.headers
        assert request.headers["Content-Type"] == "application/json"

        body_data = await request.json()

        expected_payload = {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "age": 28,
            "preferences": {
                "cuisine": "Italian",
                "dietary_restrictions": "vegetarian",
                "budget_range": "moderate",
            },
            "registration_source": "voice_assistant",
        }

        assert body_data == expected_payload

        return json_response(
            {
                "profile_id": "123",
                "status": "active",
                "created_at": "2024-01-15T10:30:15Z",
                "welcome_message": "Welcome to our platform!",
            },
            status=201,
        )

    app = Application()
    app.router.add_post("/users/profile", create_profile_handler)
    server = await aiohttp_server(app)
    create_profile_action.url = f"http://{server.host}:{server.port}/users/profile"

    async with (
        openai.LLM(model="gpt-4.1-mini") as llm,
        AgentSession(llm=llm) as session,
    ):
        agent = FlowAgent(flow=user_profile_flow)
        await session.start(agent)

        await session.run(user_input="Hello")
        await session.run(user_input="Alice Johnson")
        await session.run(user_input="alice.johnson@example.com")
        await session.run(user_input="28")
        await session.run(user_input="Italian")
        await session.run(user_input="vegetarian")
        final_response = await session.run(user_input="moderate")

        final_response.expect.contains_message(role="assistant").judge(
            llm,
            intent="Should inform user that their profile has been created successfully and profile id is 123",
        )

        assert session.userdata.model_dump() == {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "age": 28,
            "preferred_cuisine": "Italian",
            "dietary_restrictions": "vegetarian",
            "budget_range": "moderate",
        }

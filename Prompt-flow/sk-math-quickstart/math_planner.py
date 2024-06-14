import asyncio
import os
from promptflow import tool

import semantic_kernel as sk
from semantic_kernel.planners.sequential_planner import SequentialPlanner
from plugins.MathPlugin.Math import Math as Math
from promptflow.connections import (
    AzureOpenAIConnection,
)

from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextCompletion,
)

@tool
def my_python_tool(
    input: str,
    deployment_type: str,
    deployment_name: str,
    AzureOpenAIConnection: AzureOpenAIConnection,
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel()
    
    # The service_id is used to identify the service in the kernel.
    # This can be updated to a custom value if needed.
    # It should match the execution setting's key in a config.json file.
    service_id = "default"

    # Add the chat service
    if deployment_type == "chat-completion":
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=deployment_name,
                endpoint=AzureOpenAIConnection.api_base,
                api_key=AzureOpenAIConnection.api_key,
            ),
        )
    elif deployment_type == "text-completion":
        kernel.add_service(
            AzureTextCompletion(
                service_id=service_id,
                deployment_name=deployment_name,
                endpoint=AzureOpenAIConnection.api_base,
                api_key=AzureOpenAIConnection.api_key,
            ),
        )
        
    script_directory = os.path.dirname(__file__)
    plugins_directory = os.path.join(script_directory, "plugins")
    kernel.add_plugin(parent_directory=plugins_directory, plugin_name="MathPlugin")

    planner = SequentialPlanner(kernel=kernel, service_id=service_id)
    goal = "Use the available math functions to solve this word problem: " + input
    plan = asyncio.run(planner.create_plan(goal))
    
    # Debug: Output Plan
    for index, step in enumerate(plan._steps):
        print("Function: " + step.plugin_name + "." + step._function.name)
        print("Input vars: " + str(step.parameters.values))
        print("Output vars: " + str(step._outputs))

    # Execute the plan
    result = asyncio.run(plan.invoke(kernel=kernel))

    # Debug: Output Result
    print("Result: " + str(result))

    return str(result)
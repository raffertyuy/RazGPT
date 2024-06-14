# This code is not part of sk-math-quickstart, but is here to try things out as it is referred to by the quickstart document in https://learn.microsoft.com/en-us/semantic-kernel/agents/planners/evaluate-and-deploy-planners/create-a-prompt-flow-with-semantic-kernel

import asyncio
import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.planners.function_calling_stepwise_planner import FunctionCallingStepwisePlanner

from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureTextCompletion,
)

load_dotenv()

async def main():
    # <CreatePlanner>
    # Initialize the kernel
    kernel = Kernel()

    # Add the service to the kernel
    # use_chat: True to use chat completion, False to use text completion
    kernel.add_service(
        AzureChatCompletion(
            service_id="default",
            deployment_name="gpt35turbo",
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        )
    )
    
    script_directory = os.path.dirname(__file__)
    plugins_directory = os.path.join(script_directory, "plugins")
    kernel.add_plugin(parent_directory=plugins_directory, plugin_name="MathPlugin")

    planner = FunctionCallingStepwisePlanner(service_id="default")
    # </CreatePlanner>
    # <RunPlanner>
    goal = "Figure out how much I have if first, my investment of 2130.23 dollars increased by 23%, and then I spend $5 on a coffee"  # noqa: E501

    # Execute the plan
    result = await planner.invoke(kernel=kernel, question=goal)

    print(f"The goal: {goal}")
    print(f"Plan result: {result.final_answer}")
    # </RunPlanner>


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
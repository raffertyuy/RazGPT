﻿// Copyright (c) Microsoft. All rights reserved.

using System.Linq;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using Orchestrator.Model;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.AI;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel.Orchestration;
using Microsoft.SemanticKernel.Planning.Planners;

namespace Orchestrator;

public class SemanticKernelEndpoint
{
    private static readonly JsonSerializerOptions s_jsonOptions = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };
    private readonly IMemoryStore _memoryStore;

    public SemanticKernelEndpoint(IMemoryStore memoryStore)
    {
        this._memoryStore = memoryStore;
    }

    [Function("InvokeFunction")]
    public async Task<HttpResponseData> InvokeFunctionAsync(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "skills/{skillName}/invoke/{functionName}")]
        HttpRequestData req,
        FunctionContext executionContext, string skillName, string functionName)
    {
        // in this sample we are using a per-request kernel that is created on each invocation
        // once created, we feed the kernel the ask received via POST from the client
        // and attempt to invoke the function with the given name

        var ask = await JsonSerializer.DeserializeAsync<Ask>(req.Body, s_jsonOptions);

        if (ask == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Invalid request, unable to parse the request payload");
        }

        var kernel = SemanticKernelFactory.CreateForRequest(
            req,
            executionContext.GetLogger<SemanticKernelEndpoint>(),
            ask.Skills,
            this._memoryStore);

        if (kernel == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Missing one or more expected HTTP Headers");
        }

        var f = kernel.Skills.GetFunction(skillName, functionName);

        var contextVariables = new ContextVariables(ask.Value);

        foreach (var input in ask.Inputs)
        {
            contextVariables.Set(input.Key, input.Value);
        }

        var result = await kernel.RunAsync(contextVariables, f);

        if (result.ErrorOccurred)
        {
            return await ResponseErrorWithMessageAsync(req, result);
        }

        var r = req.CreateResponse(HttpStatusCode.OK);
        await r.WriteAsJsonAsync(new AskResult { Value = result.Result, State = result.Variables.Select(v => new AskInput { Key = v.Key, Value = v.Value }) });
        return r;
    }

    [Function("CreatePlan")]
    public async Task<HttpResponseData> CreatePlanAsync(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "planner/createplan")]
        HttpRequestData req,
        FunctionContext executionContext)
    {
        var ask = await JsonSerializer.DeserializeAsync<Ask>(req.Body, s_jsonOptions);

        if (ask == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Invalid request, unable to parse the request payload");
        }

        var kernel = SemanticKernelFactory.CreateForRequest(
            req,
            executionContext.GetLogger<SemanticKernelEndpoint>(),
            ask.Skills);

        if (kernel == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Missing one or more expected HTTP Headers");
        }

        var planner = new SequentialPlanner(kernel);
        var goal = ask.Value;

        var plan = await planner.CreatePlanAsync(goal);

        var r = req.CreateResponse(HttpStatusCode.OK);
        await r.WriteAsJsonAsync(new AskResult { Value = plan.ToJson() });
        return r;
    }

    [Function("ExecutePlan")]
    public async Task<HttpResponseData> ExecutePlanAsync(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "planner/execute/{maxSteps?}")]
        HttpRequestData req,
        FunctionContext executionContext, int? maxSteps = 10)
    {
        var ask = await JsonSerializer.DeserializeAsync<Ask>(req.Body, s_jsonOptions);

        if (ask == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Invalid request, unable to parse the request payload");
        }

        var kernel = SemanticKernelFactory.CreateForRequest(
            req,
            executionContext.GetLogger<SemanticKernelEndpoint>(),
            ask.Skills);

        if (kernel == null)
        {
            return await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, "Missing one or more expected HTTP Headers");
        }

        var context = kernel.CreateNewContext();

        var plan = Plan.FromJson(ask.Value, context);

        var iterations = 1;

        while (plan.HasNextStep &&
               iterations < maxSteps)
        {
            try
            {
                plan = await kernel.StepAsync(context.Variables, plan);
            }
            catch (KernelException e)
            {
                context.Fail(e.Message, e);
                return await ResponseErrorWithMessageAsync(req, context);
            }

            iterations++;
        }

        var r = req.CreateResponse(HttpStatusCode.OK);
        await r.WriteAsJsonAsync(new AskResult { Value = plan.State.ToString() });
        return r;
    }

    private static async Task<HttpResponseData> ResponseErrorWithMessageAsync(HttpRequestData req, SKContext result)
    {
        return result.LastException is AIException aiException && aiException.Detail is not null
            ? await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, string.Concat(aiException.Message, " - Detail: " + aiException.Detail))
            : await req.CreateResponseWithMessageAsync(HttpStatusCode.BadRequest, result.LastErrorDescription);
    }
}
